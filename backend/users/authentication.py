import re

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailPhoneUsernameBackend(ModelBackend):

    @staticmethod
    def _get_user_by_field(field_name, field_value):
        try:
            return User.objects.get(**{field_name: field_value})
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return

        match username:
            case _ if re.search(r"^\+7 \(\d{3}\) \d{3}\-\d{2}\-\d{2}$|^\+\d{9,15}$", username):
                phone_number = re.sub(r"\D", "", username)
                user = self._get_user_by_field("phone_number", phone_number)
            case _ if re.search(r"\S+@[\w.-]+\.\w+", username):
                user = self._get_user_by_field("email", username.lower())
            case _:
                return

        if user is not None and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        return self._get_user_by_field("id", user_id)
