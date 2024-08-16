import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailPhoneUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None

        if bool(
            re.search(r"^\+7 \(\d{3}\) \d{3}\-\d{2}\-\d{2}$|^\+\d{9,15}$",
                      username)
        ):
            username = re.sub(r"\D", "", username)
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        elif bool(re.search(r"\S+@[\w.-]+\.\w+", username)):
            # Check if the input is an email address
            try:
                user = User.objects.get(email=username.lower())
            except User.DoesNotExist:
                return None
        else:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
