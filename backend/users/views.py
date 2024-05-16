import logging

from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, FormView, UpdateView

from kds_stroy.settings import MEDIA_URL, PHONE_VERIFICATION_TIME_LIMIT
from orders.models import Order, OrderPhoto
from users.forms import (ChangePhoneNumberForm, PhoneVerificationForm,
                         UserForm, UserRegistrationForm)

from .models import PhoneVerification
from .utils import (call_api_process, is_limited, is_numbers_amount_limit,
                    is_phone_change_limit, phone_validation_prepare)

User = get_user_model()

logger = logging.getLogger(__name__)


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


class ChangePhoneNumberView(FormView):
    model = User
    form_class = ChangePhoneNumberForm
    template_name = "pages/change_phone_number.html"

    def get_queryset(self):
        return self.model.objects.get(pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        if is_phone_change_limit(request.user.phone_number_change_date):
            return render(
                request,
                "registration/phone_verification_limit.html",
                {"limit": "time_limit"},
            )
        if is_numbers_amount_limit(request.user):
            return render(
                request,
                "registration/phone_verification_limit.html",
                {"limit": "number_limit"},
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
        context["is_attempt_limit"] = self.kwargs.get("is_attempt_limit",
                                                      False)
        return context

    def get(self, request, *args, **kwargs):
        last_request_obj = get_object_or_404(
            self.model, id=request.session.get("request_id")
        )
        is_repeat = True if request.GET.get("repeat_call") == "true" else False

        if is_repeat or not last_request_obj.pincode:
            call_api_process(last_request_obj,
                             last_request_obj.pincode or None)
            countdown = int(PHONE_VERIFICATION_TIME_LIMIT)
            if is_repeat:
                return JsonResponse({"countdown": countdown})
        else:
            countdown = is_limited(last_request_obj, kwargs)

        self.kwargs["pincode"] = last_request_obj.pincode
        self.kwargs["countdown"] = countdown
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
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
                phone_number=new_phone_number
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

        return render(
            self.request, "account/registration_done.html", {"new_user": user}
        )

    def form_invalid(self, form):
        last_call_obj = get_object_or_404(
            self.model, id=self.request.session.get("request_id")
        )
        self.kwargs["countdown"] = is_limited(last_call_obj, self.kwargs)
        form.cleaned_data["pincode"] = ""
        return super().form_invalid(form)


class ProfileView(DetailView):
    model = User
    template_name = "account/account.html"
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(self.model,
                                               pk=self.request.user.pk)
        context["form"] = self.form_class(instance=context["profile"])

        orders_with_photos = Order.objects.filter(
            phone_number=self.request.user.phone_number
        ).prefetch_related(
            Prefetch(
                "orderphoto_set",
                queryset=OrderPhoto.objects.all(),
                to_attr="photos"
            )
        )
        context["orders"] = orders_with_photos
        context["MEDIA_URL"] = MEDIA_URL
        return context


class ProfileEditView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "pages/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(self.model,
                                               pk=self.request.user.pk)
        context["form"] = self.form_class(instance=context["profile"])
        return context

    def form_valid(self, form):
        if "phone_number" in form.changed_data:
            form.changed_data.remove("phone_number")
        if "email" in form.changed_data:
            user = form.save(commit=False)
            user.is_email_verified = False
        return super().form_valid(form)
