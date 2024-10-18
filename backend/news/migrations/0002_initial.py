# Generated by Django 5.0.1 on 2024-08-08 13:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("news", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="news",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор",
            ),
        ),
        migrations.AddField(
            model_name="news",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="news.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AddField(
            model_name="newsphoto",
            name="news",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="news.news",
            ),
        ),
    ]
