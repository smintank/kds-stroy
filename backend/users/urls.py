from django.urls import path

from users.views import (
    ChangePhoneNumberView,
    PhoneVerificationView,
    ProfileView
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path(
        "phone_verification/",
        PhoneVerificationView.as_view(),
        name="phone_verification",
    ),
    path(
        "change_phone_number/",
        ChangePhoneNumberView.as_view(),
        name="change_phone_number",
    ),
]
