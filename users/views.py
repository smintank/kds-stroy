import logging
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    DetailView,
    FormView,
)
from verify_email.email_handler import send_verification_email

from kds_stroy import settings
from orders.models import Order, OrderPhoto
from .utils import call_and_get_pin
from users.forms import (
    UserForm,
    ChangePhoneNumberForm,
    UserRegistrationForm,
    PhoneVerificationForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)


class RegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = UserRegistrationForm
    success_url = '/registration_done/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.request.session['phone_number'] = form.cleaned_data['phone_number']
        return redirect('users:phone_verification')


class ChangePhoneNumberView(FormView):
    model = User
    form_class = ChangePhoneNumberForm
    template_name = "pages/change_phone_number.html"

    def get_queryset(self):
        return self.model.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        old_phone_number = self.request.user.phone_number
        self.request.session['old_phone_number'] = old_phone_number
        self.request.session['phone_number'] = form.cleaned_data['phone_number']
        return redirect('users:phone_verification')


class PhoneVerificationView(FormView):
    template_name = 'registration/phone_verification_form.html'
    form_class = PhoneVerificationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phone_number'] = self.request.session.get('phone_number')
        return context

    def get(self, request, *args, **kwargs):
        phone_number = self.request.session.get('phone_number')
        pincode = call_and_get_pin(phone_number)
        self.request.session['pincode'] = pincode
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_phone_number = self.request.session.get('phone_number')
        pincode = self.request.session.get('pincode')

        if pincode and pincode == form.cleaned_data['pincode']:
            old_phone_number = self.request.session.get('old_phone_number')
            if old_phone_number:
                user = get_object_or_404(User, phone_number=old_phone_number)
                user.phone_number = new_phone_number
                Order.objects.filter(phone_number=old_phone_number).update(
                    phone_number=new_phone_number
                )
                del self.request.session['old_phone_number']
            else:
                user = get_object_or_404(User, phone_number=new_phone_number)
            user.is_active = True
            user.is_phone_verified = True
            user.save()

            return render(self.request, "registration/registration_done.html",
                          {"new_user": user})
        else:
            form.add_error('pincode', 'Неверный пин-код! Попробуйте еще раз!')
            return self.form_invalid(form)


class ProfileView(DetailView):
    model = User
    template_name = "pages/profile.html"
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
            Prefetch('orderphoto_set', queryset=OrderPhoto.objects.all(),
                     to_attr='photos')
        )
        context['orders'] = orders_with_photos
        context['MEDIA_URL'] = settings.MEDIA_URL
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
        if 'phone_number' in form.changed_data:
            form.changed_data.remove('phone_number')
        if 'email' in form.changed_data:
            user = form.save(commit=False)
            user.is_active = False
            updated_user = send_verification_email(self.request, form)
            return render(
                self.request,
                "registration/email_change_done.html",
                {"updated_user": updated_user}
            )
        else:
            return super().form_valid(form)
