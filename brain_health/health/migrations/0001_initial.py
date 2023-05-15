# Generated by Django 4.1.9 on 2023-05-14 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Mood",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("score", models.IntegerField()),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Therapist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=20)),
                ("profile_picture", models.ImageField(upload_to="therapist_profiles/")),
                ("degrees", models.TextField()),
                ("certifications", models.TextField()),
                ("hourly_rate", models.DecimalField(decimal_places=2, max_digits=6)),
                ("is_available", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Suggestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("suggestion_text", models.TextField()),
                ("is_specific_to_age_group", models.BooleanField(default=False)),
                ("is_specific_to_gender", models.BooleanField(default=False)),
                (
                    "mood",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="suggestion", to="health.mood"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Relative",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=20)),
                ("is_app_user", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relative",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("message_text", models.TextField()),
                ("is_urgent", models.BooleanField(default=False)),
                ("mood", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="health.mood")),
                (
                    "relative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="message", to="health.relative"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("location", models.CharField(max_length=200)),
                ("reason", models.CharField(max_length=200)),
                ("therapist", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="health.therapist")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="appointment",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
