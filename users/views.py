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
    ChangeEmailForm,
    ChangePhoneNumberForm,
    UserRegistrationForm,
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


def phone_verification(request):
    phone_number = request.session['phone_number']

    if request.method == 'POST':
        pincode = request.session['pincode']
        print(request.POST.get('pincode'))
        print(pincode)
        if pincode and pincode == request.POST.get('pincode'):
            new_user = User.objects.get(phone_number=phone_number)
            new_user.is_active = True
            new_user.is_phone_verified = True
            new_user.save()

            # send_verification_email(request, form)
            return render(request, "registration/registration_done.html",
                          {"new_user": new_user})
        else:
            return render(request, 'registration/phone_verification_form.html',
                          {'error': 'Не верный пин-код! Попробуйте еще раз!'})
    else:
        request.session['pincode'] = call_and_get_pin(phone_number)
        return render(request, 'registration/phone_verification_form.html')


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

# class ChangeEmailView(UpdateView):
#     model = User
#     form_class = ChangeEmailForm
#     template_name = "registration/change_email.html"
#     success_url = reverse_lazy("profile")


# class ChangePhoneNumberView(UpdateView):
#     model = User
#     form_class = ChangePhoneNumberForm
#     template_name = "registration/change_phone_number.html"
#     success_url = reverse_lazy("profile")
