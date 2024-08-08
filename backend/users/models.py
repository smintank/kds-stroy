import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils.phone_number import clean_phone_number, format_phone_number


class User(AbstractUser):
    first_name = models.CharField(
        "Имя", max_length=150, blank=False, null=False,
        help_text="Обязательное поле"
    )
    middle_name = models.CharField("Отчество", max_length=150, blank=True)
    avatar = models.ImageField(
        "Фото профиля", upload_to="avatars/", default="avatars/default.png"
    )
    email = models.EmailField(
        "Электронная почта", unique=True, help_text="Обязательное поле"
    )
    is_email_verified = models.BooleanField("Email подтвержден", default=False)
    phone_number = models.CharField(
        "Номер телефона", max_length=18, unique=True,
        help_text="Обязательное поле"
    )
    phone_number_change_date = models.DateTimeField(
        "Последняя дата изменения номера телефона", auto_now_add=True
    )
    is_phone_verified = models.BooleanField("Телефон подтвержден",
                                            default=False)
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Город проживания",
    )
    address = models.ForeignKey(
        "locations.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Адрес проживания",
    )
    is_notify = models.BooleanField(
        "Уведомлять о новых заказах", default=False,
        help_text="Отметьте, если пользователь должен получать уведомления "
                  "о новых заказах"
    )
    tg_id = models.CharField(
        "Telegram", max_length=50,
        blank=True, help_text="Укажите Telegram ID в формате 123456789"
    )

    date_joined = models.DateTimeField("Дата создания аккаунта",
                                       auto_now_add=True)
    last_login = models.DateTimeField("Последний вход", auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "username", "phone_number"]

    def save(self, *args, **kwargs):
        if self.phone_number:
            self.phone_number = clean_phone_number(self.phone_number)
        if not self.id:
            is_unique = False
            while not is_unique:
                unique_username = str(uuid.uuid1())[:10]
                unique_username = f"User-{unique_username}"
                if not User.objects.filter(username=unique_username).exists():
                    is_unique = True
                    self.username = unique_username
        super().save(*args, **kwargs)

    @property
    def formatted_phone_number(self):
        return format_phone_number(self.phone_number)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"


class PhoneVerification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    phone_number = models.CharField("Номер телефона", max_length=18)
    pincode = models.CharField("Пин-код", max_length=4, blank=True, null=True)
    last_call = models.DateTimeField(
        "Время последнего запроса звонка", blank=True, null=True
    )
    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number}: {self.pincode}"

    @classmethod
    def verify_code(cls, user, phone_number, pincode):
        try:
            cls.objects.get(user=user, phone_number=phone_number,
                            pincode=pincode)
            return True
        except cls.DoesNotExist:
            return False

    class Meta:
        verbose_name = "запрос на подтверждение телефона"
        verbose_name_plural = "Запросы на подтверждение телефона"
