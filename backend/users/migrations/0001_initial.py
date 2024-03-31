# Generated by Django 5.0.1 on 2024-03-30 12:45

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Обязательное поле",
                        max_length=150,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Отчество"
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        default="avatars/default.png",
                        upload_to="avatars/",
                        verbose_name="Фото профиля",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Обязательное поле",
                        max_length=254,
                        unique=True,
                        verbose_name="Электронная почта",
                    ),
                ),
                (
                    "is_email_verified",
                    models.BooleanField(
                        default=False, verbose_name="Email подтвержден"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        help_text="Обязательное поле",
                        max_length=18,
                        unique=True,
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "phone_number_change_date",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Последняя дата изменения номера телефона",
                    ),
                ),
                (
                    "is_phone_verified",
                    models.BooleanField(
                        default=False, verbose_name="Телефон подтвержден"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания аккаунта"
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(auto_now=True, verbose_name="Последний вход"),
                ),
                (
                    "address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="orders.address",
                        verbose_name="Адрес проживания",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "Пользователи",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="PhoneVerification",
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
                    "phone_number",
                    models.CharField(max_length=18, verbose_name="Номер телефона"),
                ),
                (
                    "pincode",
                    models.CharField(
                        blank=True, max_length=4, null=True, verbose_name="Пин-код"
                    ),
                ),
                (
                    "last_call",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Время последнего запроса звонка",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "запрос на подтверждение телефона",
                "verbose_name_plural": "Запросы на подтверждение телефона",
            },
        ),
    ]
