# Generated by Django 4.1.9 on 2023-05-17 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0018_therapist_card_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="therapist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedback_therapist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
