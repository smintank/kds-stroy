# Generated by Django 5.0.1 on 2024-04-09 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_alter_city_district_alter_city_type"),
    ]

    operations = [
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
                (
                    "short_name",
                    models.CharField(
                        default=models.CharField(max_length=255), max_length=255
                    ),
                ),
            ],
            options={
                "verbose_name": "тип населенного пункта",
                "verbose_name_plural": "Типы населенных пунктов",
            },
        ),
        migrations.AddField(
            model_name="district",
            name="short_name",
            field=models.CharField(
                default=models.CharField(max_length=255), max_length=255
            ),
        ),
        migrations.AlterField(
            model_name="city",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="orders.citytype"
            ),
        ),
    ]
