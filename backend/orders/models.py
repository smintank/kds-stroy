from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City
from orders.utils import get_unique_uid, get_upload_path

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        REGISTERED = "Зарегистрирован", _("🟥 Зарегистрирован")
        PROCESSED = "В работе", _("🟨 В работе")
        COMPLETED = "Завершен", _("🟩 Завершен")
        CANCELED = "Отменен", _("⬛️ Отменен")

    order_id = models.IntegerField("Номер заказа")
    first_name = models.CharField("Имя", max_length=150)
    phone_number = models.CharField("Номер телефона", max_length=18)
    comment = models.TextField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)
    status = models.CharField(
        "Статус", choices=Status.choices, default=Status.REGISTERED,
        max_length=20
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Зарегистрированный пользователь",
        blank=True,
        null=True,
    )
    cost = models.FloatField(
        "Стоимость в руб.",
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10000000.0)
        ]
    )
    final_cost = models.FloatField(
        "Итог в руб.",
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10000000.0)
        ]
    )
    discount = models.IntegerField(
        "Скидка в %",
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    address = models.TextField(verbose_name="Адрес", blank=True, null=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, verbose_name="Населенный пункт",
        blank=True, null=True
    )

    def __str__(self):
        return f"Заказ №{self.order_id}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = get_unique_uid(Order)
        self.final_cost = round(self.cost - self.cost / 100 * self.discount, 2)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"


class OrderPhoto(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    photo = models.ImageField("Фото", upload_to=get_upload_path)

    def __str__(self):
        return f"Фото заказа №{self.order.order_id}"

    class Meta:
        verbose_name = "фото заказа"
        verbose_name_plural = "Фото заказов"
