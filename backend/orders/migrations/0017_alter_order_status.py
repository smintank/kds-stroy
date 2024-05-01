# Generated by Django 5.0.1 on 2024-05-01 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0016_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Зарегистрирован", "🟨 Зарегистрирован"),
                    ("В работе", "🟦 В работе"),
                    ("Завершен", "🟩 Завершен"),
                    ("Отменен", "🟥 Отменен"),
                ],
                default="Зарегистрирован",
                max_length=20,
                verbose_name="Статус",
            ),
        ),
    ]
