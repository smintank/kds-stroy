# Generated by Django 5.0.1 on 2024-05-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0005_alter_news_photos"),
    ]

    operations = [
        migrations.AlterField(
            model_name="newsphoto",
            name="photo",
            field=models.ImageField(upload_to="news_photos/"),
        ),
    ]
