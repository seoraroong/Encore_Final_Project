# Generated by Django 4.1.13 on 2024-07-26 03:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diaryapp", "0007_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="diaryplanmodel",
            name="destination",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
