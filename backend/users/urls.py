from django.urls import path
from django.views.generic import TemplateView

from users.views import (
    ChangePhoneNumberView,
    PhoneVerificationView,
    ProfileView,
    EmailVerificationView,
    EmailVerificationFailedView,
    EmailVerificationSuccessView,
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("phone_verification/", PhoneVerificationView.as_view(), name="phone_verification"),
    path("change_phone_number/", ChangePhoneNumberView.as_view(), name="change_phone_number"),
    path('verify-email/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('verify-email/success', EmailVerificationSuccessView.as_view(), name='email_verification_success'),
    path('verify-email/fail', EmailVerificationFailedView.as_view(), name='email_verification_failed')
]
