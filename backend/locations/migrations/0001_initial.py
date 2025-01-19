# Generated by Django 5.0.8 on 2025-01-19 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_district_shown",
                    models.BooleanField(default=True, verbose_name="Показывать район?"),
                ),
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Отображать"),
                ),
                (
                    "latitude",
                    models.FloatField(default=45.03333, verbose_name="Широта"),
                ),
                (
                    "longitude",
                    models.FloatField(default=38.98333, verbose_name="Долгота"),
                ),
            ],
            options={
                "verbose_name": "населенный пункт",
                "verbose_name_plural": "Населенные пункты",
            },
        ),
        migrations.CreateModel(
            name="CityType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "тип населенного пункта",
                "verbose_name_plural": "Типы населенных пунктов",
            },
        ),
        migrations.CreateModel(
            name="District",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("short_name", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "район",
                "verbose_name_plural": "Районы",
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "регион",
                "verbose_name_plural": "Регионы",
            },
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="locations.city"
                    ),
                ),
            ],
            options={
                "verbose_name": "адрес",
                "verbose_name_plural": "Адреса",
            },
        ),
        migrations.AddField(
            model_name="city",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="locations.citytype",
                verbose_name="Тип",
            ),
        ),
        migrations.AddField(
            model_name="city",
            name="district",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="locations.district",
                verbose_name="Район",
            ),
        ),
        migrations.AddField(
            model_name="district",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="locations.region"
            ),
        ),
    ]
