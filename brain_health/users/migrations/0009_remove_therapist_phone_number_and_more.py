# Generated by Django 4.1.9 on 2023-05-15 12:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_user_is_therapist_therapist"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="therapist",
            name="phone_number",
        ),
        migrations.RemoveField(
            model_name="therapist",
            name="profile_picture",
        ),
    ]
