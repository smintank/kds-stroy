# Generated by Django 5.0.1 on 2024-02-18 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_id",
            field=models.CharField(max_length=20, verbose_name="Номер заказа"),
        ),
    ]