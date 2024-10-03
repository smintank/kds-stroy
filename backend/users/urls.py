from django.urls import path

from users.views import (
    ChangePhoneNumberView,
    ChangeEmailView,
    ChangeEmailDoneView,
    PhoneVerificationView,
    ProfileView,
    EmailVerificationView,
    EmailVerificationFailedView,
    EmailVerificationSuccessView,
    DeleteProfileView,
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("delete/", DeleteProfileView.as_view(), name="delete_profile"),
    path("phone_verification/", PhoneVerificationView.as_view(), name="phone_verification"),
    path("change_phone_number/", ChangePhoneNumberView.as_view(), name="change_phone_number"),
    path('change-email', ChangeEmailView.as_view(), name='change_email'),
    path('change-email-done', ChangeEmailDoneView.as_view(), name='change_email_done'),
    path('verify-email/success', EmailVerificationSuccessView.as_view(), name='email_verification_success'),
    path('verify-email/fail', EmailVerificationFailedView.as_view(), name='email_verification_failed'),
    path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
]
