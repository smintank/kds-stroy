import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, DeleteView

from kds_stroy.settings import PHONE_VERIFICATION_TIME_LIMIT, PINCODE_INPUT_LIMIT
from users.messages import OLD_MAIL_CHANGING_TEXT, OLD_MAIL_CHANGING_SUBJECT
from orders.models import Order, OrderPhoto
from users.forms import (ChangePhoneNumberForm, PhoneVerificationForm,
                         UserForm, UserRegistrationForm, ChangeEmailForm)

from .models import PhoneVerification
from .utils.base import (call_api_process, get_countdown, is_numbers_amount_limit, send_email_message,
                         is_phone_change_limit, phone_validation_prepare, send_verification_email, token_generator)
from .utils.phone_number import clean_phone_number

User = get_user_model()

logger = logging.getLogger(__name__)


class ProfileView(LoginRequiredMixin, FormView):
    model = User
    template_name = "account/account.html"
    success_url = reverse_lazy("users:profile")
    form_class = UserForm

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context["profile"] = user

        city = user.city or ""
        context["form"] = self.form_class(instance=user, initial={
            "phone_number": user.formatted_phone_number, "city": str(city)
        })

        context["orders"] = Order.objects.filter(
            phone_number=user.phone_number
        ).order_by("-created_at").prefetch_related(
            Prefetch("orderphoto_set", queryset=OrderPhoto.objects.all(), to_attr="photos")
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class RegistrationView(FormView):
    template_name = "account/register.html"
    form_class = UserRegistrationForm
    success_url = "/registration_done/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        phone_validation_prepare(
            phone_number=form.cleaned_data["phone_number"],
            session=self.request.session,
            user=user,
        )
        return redirect("users:phone_verification")


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "account/delete_account.html"
    success_url = reverse_lazy('home')

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, id=self.request.user.id)


class ChangePhoneNumberView(LoginRequiredMixin, FormView):
    model = User
    form_class = ChangePhoneNumberForm
    template_name = "account/change_phone_number.html"

    def get_queryset(self):
        return self.model.objects.get(pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        if is_phone_change_limit(request.user.phone_number_change_date):
            return render(
                request,
                "account/phone_verification_limit.html",
                {"limit": "time_limit", **self.get_context_data(**kwargs)},
            )
        if is_numbers_amount_limit(request.user):
            return render(
                request,
                "account/phone_verification_limit.html",
                {"limit": "number_limit", **self.get_context_data(**kwargs)},
            )
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        phone_validation_prepare(
            phone_number=form.cleaned_data["phone_number"],
            session=self.request.session,
            user=user,
        )
        self.request.session["old_phone_number"] = user.phone_number
        return redirect("users:phone_verification")


class PhoneVerificationView(FormView):
    model = PhoneVerification
    template_name = "account/phone_verification_form.html"
    form_class = PhoneVerificationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["countdown"] = self.kwargs.get("countdown", 0)
        context["pincode_limit"] = self.kwargs.get("pincode_limit", False)
        context["is_attempt_limit"] = self.kwargs.get("is_attempt_limit", False)
        return context

    def get(self, request, *args, **kwargs):
        last_call_obj = get_object_or_404(self.model, id=request.session.get("request_id"))
        is_repeat = request.GET.get("repeat_call") == "true"

        if is_repeat or not last_call_obj.pincode:
            call_api_process(last_call_obj, last_call_obj.pincode or None)
            countdown = int(PHONE_VERIFICATION_TIME_LIMIT)
            if is_repeat:
                last_call_obj.attempts_amount = 0
                last_call_obj.save()
                return JsonResponse({"countdown": countdown})
        else:
            countdown = get_countdown(last_call_obj, kwargs)

        self.kwargs["pincode"] = last_call_obj.pincode
        self.kwargs["countdown"] = countdown
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        last_call_obj = get_object_or_404(self.model, id=self.request.session.get("request_id"))
        if last_call_obj.attempts_amount + 1 >= int(PINCODE_INPUT_LIMIT):
            form.add_error("pincode", "Вы исчерпали все попытки ввода пин-кода!")
            return self.form_invalid(form)

        new_phone_number = self.request.session.get("phone_number")
        old_phone_number = self.request.session.get("old_phone_number")
        pincode = form.cleaned_data.get("pincode")

        if old_phone_number:
            user = get_object_or_404(User, phone_number=old_phone_number)
            if not self.model.verify_code(user, new_phone_number, pincode):
                form.add_error("pincode", "Неверный код. Попробуйте ещё раз!")
                return self.form_invalid(form)
            user.phone_number = new_phone_number
            user.phone_number_change_date = timezone.now()
            Order.objects.filter(phone_number=old_phone_number).update(
                phone_number=clean_phone_number(new_phone_number)
            )
            del self.request.session["old_phone_number"]
        else:
            user = get_object_or_404(User, phone_number=new_phone_number)
            if not self.model.verify_code(user, new_phone_number, pincode):
                form.add_error("pincode", "Неверный код. Попробуйте ещё раз!")
                return self.form_invalid(form)
        user.is_active = True
        user.is_phone_verified = True
        user.save()
        del self.request.session["phone_number"]

        if not user.is_authenticated:
            send_verification_email(self.request, user)
            return render(self.request, "account/registration_done.html",
                          {"new_user": user, **self.get_context_data(**self.kwargs)})

        return render(self.request, "account/change_phone_number_done.html",
                      {**self.get_context_data(**self.kwargs)})

    def form_invalid(self, form):
        last_call_obj = get_object_or_404(self.model, id=self.request.session.get("request_id"))

        if last_call_obj.attempts_amount + 1 >= int(PINCODE_INPUT_LIMIT):
            self.kwargs["pincode_limit"] = True
        last_call_obj.attempts_amount += 1
        last_call_obj.save()
        self.kwargs["countdown"] = get_countdown(last_call_obj, self.kwargs)
        # form.cleaned_data["pincode"] = ""
        return super().form_invalid(form)


class ChangeEmailView(LoginRequiredMixin, FormView):
    model = User
    form_class = ChangeEmailForm
    template_name = "account/change_email.html"
    success_url = reverse_lazy("users:change_email_done")

    def get_queryset(self):
        return self.model.objects.get(pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        old_email = request.user.email
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_verified = False
            user.save()

            send_email_message(OLD_MAIL_CHANGING_SUBJECT,
                               OLD_MAIL_CHANGING_TEXT.format(email=user.email),
                               old_email)
            send_verification_email(request, user)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EmailVerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return redirect('users:email_verification_success')
        else:
            return redirect('users:email_verification_failed')
