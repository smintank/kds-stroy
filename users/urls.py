from django.urls import path

from users.views import (
    ProfileView,
    ProfileEditView,
    ChangePhoneNumberView,
    PhoneVerificationView
)

app_name = "users"

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("phone_verification/",
         PhoneVerificationView.as_view(),
         name="phone_verification"),
    path("change_phone_number/",
         ChangePhoneNumberView.as_view(),
         name="change_phone_number"),
]
