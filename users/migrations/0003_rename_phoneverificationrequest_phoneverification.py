# Generated by Django 5.0.1 on 2024-03-14 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_phoneverificationrequest"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PhoneVerificationRequest",
            new_name="PhoneVerification",
        ),
    ]
