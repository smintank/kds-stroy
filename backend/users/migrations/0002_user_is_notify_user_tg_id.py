# Generated by Django 5.0.1 on 2024-04-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_notify",
            field=models.BooleanField(default=False, verbose_name="Уведомлять"),
        ),
        migrations.AddField(
            model_name="user",
            name="tg_id",
            field=models.CharField(
                blank=True, max_length=50, verbose_name="Telegram ID"
            ),
        ),
    ]