# Generated by Django 5.0.1 on 2024-02-26 18:03

import orders.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_remove_order_photo_order_cost_order_discount_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "заказ", "verbose_name_plural": "Заказы"},
        ),
        migrations.AlterModelOptions(
            name="orderphoto",
            options={
                "verbose_name": "фото заказа",
                "verbose_name_plural": "Фото заказов",
            },
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Зарегистрирован", "Registered"),
                    ("В работе", "Processed"),
                    ("Завершен", "Completed"),
                    ("Отменен", "Canceled"),
                ],
                default="Зарегистрирован",
                max_length=20,
                verbose_name="Статус",
            ),
        ),
        migrations.AlterField(
            model_name="orderphoto",
            name="photo",
            field=models.ImageField(
                upload_to=orders.models.get_upload_path, verbose_name="Фото"
            ),
        ),
    ]