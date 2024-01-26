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
    order_id = models.IntegerField()
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    authorized_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )
    address = models.ForeignKey(Address, on_delete=models.PROTECT)

    def __str__(self):
        return self.order_id, self.name, self.phone

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
