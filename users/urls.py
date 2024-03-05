from django.urls import path

from users.views import (
    ProfileView,
    ProfileEditView,
    # ChangePasswordView,
    # ChangeEmailView,
    # ChangePhoneNumberView
)

app_name = "users"

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    # path(
    #     "profile/change-email/",
    #     ChangeEmailView.as_view(),
    #     name="change_email"
    # ),
    # path(
    #     "profile/change-phone/",
    #     ChangePhoneNumberView.as_view(),
    #     name="change_phone_number",
    # ),
]
