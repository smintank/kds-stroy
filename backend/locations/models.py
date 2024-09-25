from django.db import models

from orders.utils import get_full_city


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
    district = models.ForeignKey(District, on_delete=models.CASCADE,
                                 verbose_name="Район")
    is_district_shown = models.BooleanField(default=True,
                                            verbose_name="Показывать район?")
    type = models.ForeignKey(CityType, on_delete=models.CASCADE,
                             verbose_name="Тип")
    name = models.CharField(max_length=255, verbose_name="Название")
    is_active = models.BooleanField(default=True, verbose_name="Отображать")
    latitude = models.FloatField(default=45.03333, verbose_name="Широта")
    longitude = models.FloatField(default=38.98333, verbose_name="Долгота")

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
