from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from verify_email.email_handler import send_verification_email

from users.forms import (
    UserEditForm,
    ChangeEmailForm,
    ChangePhoneNumberForm,
    UserRegistrationForm,
)
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home:home")


class MyLoginView(LoginView):

    template_name = "registration/login.html"
    success_url = reverse_lazy("home:home")


class MyLogoutView(LogoutView):
    template_name = "registration/logged_out.html"
    next_page = reverse_lazy("home:home")


class ProfileView(DetailView):
    model = User
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(self.model, pk=self.request.user.pk)
        return context


class ProfileEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "registration/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.pk)


class ChangePasswordView(PasswordChangeView):
    template_name = "registration/change_password.html"
    success_url = reverse_lazy("profile")


class ChangeEmailView(UpdateView):
    model = User
    form_class = ChangeEmailForm
    template_name = "registration/change_email.html"
    success_url = reverse_lazy("profile")


class ChangePhoneNumberView(UpdateView):
    model = User
    form_class = ChangePhoneNumberForm
    template_name = "registration/change_phone_number.html"
    success_url = reverse_lazy("profile")


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = send_verification_email(request, user_form)
            return render(
                request,
                "registration/registration_done.html",
                {"new_user": new_user}
            )
        return render(
            request,
            "registration/registration_form.html",
            {"user_form": user_form}
        )
    else:
        user_form = UserRegistrationForm()
        return render(
            request,
            "registration/registration_form.html",
            {"user_form": user_form}
        )
