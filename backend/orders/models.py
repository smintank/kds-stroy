import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "регион"
        verbose_name_plural = "Регионы"


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

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
        REGISTERED = "Зарегистрирован"
        PROCESSED = "В работе"
        COMPLETED = "Завершен"
        CANCELED = "Отменен"

    order_id = models.IntegerField("Номер заказа")
    first_name = models.CharField("Имя", max_length=150)
    phone_number = models.CharField("Номер телефона", max_length=18)
    comment = models.TextField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    status = models.CharField(
        "Статус", choices=Status.choices, default=Status.REGISTERED, max_length=20
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Авторизованный пользователь",
        blank=True,
        null=True,
    )
    cost = models.IntegerField("Итоговая стоимость", blank=True, null=True)
    discount = models.IntegerField("Скидка", default=0)
    is_discount = models.BooleanField("Скидка", default=False)

    address = models.TextField(verbose_name="Адрес", blank=True, null=True)
    # address = models.ForeignKey(
    #     Address, on_delete=models.SET_NULL, blank=True, null=True

    def __str__(self):
        return f"Заказ №{self.order_id}"

    def save(self, *args, **kwargs):
        is_unique = False
        while not is_unique:
            unique_order_number = str(uuid.uuid1().int)[:8]
            if not Order.objects.filter(order_id=unique_order_number).exists():
                is_unique = True
                self.order_id = unique_order_number
                super().save(*args, **kwargs)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"


def get_upload_path(instance, filename):
    _, file_extension = os.path.splitext(filename)
    path = os.path.join("order_photos", str(instance.order.order_id))
    return os.path.join(path, f"photo{file_extension}")


class OrderPhoto(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    photo = models.ImageField("Фото", upload_to=get_upload_path)

    def __str__(self):
        return f"Фото заказа №{self.order.order_id}"

    class Meta:
        verbose_name = "фото заказа"
        verbose_name_plural = "Фото заказов"