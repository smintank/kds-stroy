from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    DetailView,
)
from verify_email.email_handler import send_verification_email

from users.forms import (
    UserForm,
    ChangeEmailForm,
    ChangePhoneNumberForm,
    UserRegistrationForm,
)
from django.contrib.auth import get_user_model

User = get_user_model()


# class MyLoginView(LoginView):
#     template_name = "registration/login.html"
#     success_url = reverse_lazy("home")


# class MyLogoutView(LogoutView):
#     template_name = "registration/logged_out.html"
#     next_page = reverse_lazy("home")


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
