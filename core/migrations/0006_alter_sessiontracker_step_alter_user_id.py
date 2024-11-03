# Generated by Django 5.1.2 on 2024-11-03 16:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_otpcode_attempts_otpcode_is_verified_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sessiontracker",
            name="step",
            field=models.CharField(
                choices=[
                    ("register", "Register"),
                    ("reset", "Reset Password"),
                    ("code_sent", "Code Sent"),
                    ("code_verified", "Code Verified"),
                    ("active", "Active"),
                ],
                default="register",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
