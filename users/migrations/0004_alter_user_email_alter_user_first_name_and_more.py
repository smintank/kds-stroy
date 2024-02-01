# Generated by Django 5.0.1 on 2024-02-01 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_email_alter_user_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                help_text="(Обязательное поле)",
                max_length=254,
                unique=True,
                verbose_name="Электронная почта",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                help_text="(Обязательное поле)", max_length=150, verbose_name="Имя"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                help_text="(Обязательное поле)",
                max_length=18,
                unique=True,
                verbose_name="Номер телефона",
            ),
        ),
    ]
