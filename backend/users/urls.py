from django.urls import path
from django.views.generic import TemplateView

from users.views import (
    ChangePhoneNumberView,
    ChangeEmailView,
    PhoneVerificationView,
    ProfileView,
    EmailVerificationView,
    DeleteProfileView,
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("delete/", DeleteProfileView.as_view(), name="delete_profile"),
    path("phone-verification/", PhoneVerificationView.as_view(), name="phone_verification"),
    path("change-phone-number/", ChangePhoneNumberView.as_view(), name="change_phone_number"),
    path('change-email', ChangeEmailView.as_view(), name='change_email'),
    path('change-email-done', TemplateView.as_view(template_name='account/change_email_done.html'),
         name='change_email_done'),
    path('verify-email/success', TemplateView.as_view(template_name='account/email_verification_success.html'),
         name='email_verification_success'),
    path('verify-email/fail', TemplateView.as_view(template_name='account/email_verification_failed.html'),
         name='email_verification_failed'),
    path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
]
