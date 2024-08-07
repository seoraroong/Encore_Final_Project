<<<<<<<< HEAD:Jpage/migrations/02_initial.py
========
# Generated by Django 4.1.13 on 2024-07-26 01:31

>>>>>>>> 8718befd92fb8d19c10e55ea27e956adb04fd59d:diaryapp/migrations/0007_wishlist.py
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diaryapp", "0006_alter_aiwritemodel_diarytitle_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Wishlist",
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
                ("user_email", models.EmailField(max_length=254)),
                ("place", models.CharField(max_length=2000)),
                ("added_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "unique_together": {("user_email", "place")},
            },
        ),
    ]