from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    avatar = models.ImageField("Фото профиля", upload_to="avatars/",
                               default="avatars/default.png")
    email = models.EmailField("Электронная почта", unique=True)
    is_email_verified = models.BooleanField(default=False)
    phone_number = PhoneNumberField("Номер телефона", unique=True)
    is_phone_verified = models.BooleanField(default=False)
    address = models.ForeignKey(
        "orders.Address",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Адрес проживания",
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
