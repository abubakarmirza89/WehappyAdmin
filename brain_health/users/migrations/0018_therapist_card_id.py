# Generated by Django 4.1.9 on 2023-05-16 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0017_appointment"),
    ]

    operations = [
        migrations.AddField(
            model_name="therapist",
            name="card_id",
            field=models.CharField(default=13, max_length=25),
            preserve_default=False,
        ),
    ]
