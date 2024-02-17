import uuid

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'Регионы'


class City(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'населенный пункт'
        verbose_name_plural = 'Населенные пункты'


class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса'


class Order(models.Model):
    ORDER_STATUS = (
        ('REGISTERED', 'Зарегистрирована'),
        ('PROCESSED', 'В работе'),
        ('COMPLETED', 'Завершена'),
        ('CANCELED', 'Отменена'),
    )

    order_id = models.IntegerField()
    first_name = models.CharField("Имя", max_length=150,
                                  blank=False, null=False)
    phone_number = models.CharField("Номер телефона", max_length=18,
                                    blank=False, null=False)
    comment = models.TextField("Комментарий", blank=True, null=True)
    created_at = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    status = models.CharField(
        "Статус", choices=ORDER_STATUS, default='REGISTERED', max_length=20
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        verbose_name="Авторизованный пользователь",
        blank=True, null=True
    )
    address = models.TextField(verbose_name="Адрес", blank=True, null=True)
    # address = models.ForeignKey(
    #     Address, on_delete=models.SET_NULL, blank=True, null=True
    # )
    photo = models.ImageField('Фото', upload_to='post_images', blank=True)

    def __str__(self):
        return self.order_id, self.first_name, self.phone_number

    def save(self, *args, **kwargs):
        is_unique = False
        while not is_unique:
            unique_order_number = str(uuid.uuid1())[:8].upper()
            unique_order_number = f"№{unique_order_number}"
            if not Order.objects.filter(order_id=unique_order_number).exists():
                is_unique = True
                self.order_id = unique_order_number
                super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'Заявки'

