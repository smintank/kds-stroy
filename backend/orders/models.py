from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from orders.utils import get_full_city, get_unique_uid, get_upload_path

User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "регион"
        verbose_name_plural = "Регионы"


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "район"
        verbose_name_plural = "Районы"


class CityType(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тип населенного пункта"
        verbose_name_plural = "Типы населенных пунктов"


class City(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    is_district_shown = models.BooleanField(default=True)
    type = models.ForeignKey(CityType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    latitude = models.FloatField(default=45.03333)
    longitude = models.FloatField(default=38.98333)

    def __str__(self):
        return get_full_city(self)

    def short_name(self):
        return f"{self.type.short_name} {self.name}"

    class Meta:
        verbose_name = "населенный пункт"
        verbose_name_plural = "Населенные пункты"


class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "Адреса"


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
