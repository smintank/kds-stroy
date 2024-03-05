from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    DetailView,
    FormView,
)
from verify_email.email_handler import send_verification_email

from orders.models import Order
from users.forms import (
    UserForm,
    ChangeEmailForm,
    ChangePhoneNumberForm,
    UserRegistrationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(FormView):
    template_name = 'registration/registration_form.html'
    form_class = UserRegistrationForm
    success_url = '/registration_done/'

    def form_valid(self, form):
        new_user = send_verification_email(self.request, form)
        return render(
            self.request,
            "registration/registration_done.html",
            {"new_user": new_user}
        )


class ProfileView(DetailView):
    model = User
    template_name = "registration/profile.html"
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(self.model,
                                               pk=self.request.user.pk)
        context["form"] = self.form_class(instance=context["profile"])
        context['orders'] = Order.objects.filter(phone_number=self.request.user.phone_number)
        return context


class ProfileEditView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "registration/profile_edit.html"
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
