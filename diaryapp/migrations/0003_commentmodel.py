# Generated by Django 4.1.13 on 2024-07-16 08:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diaryapp", "0002_alter_aiwritemodel_emotion_diaryplanmodel"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentModel",
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
                ("comment_id", models.CharField(max_length=255, unique=True)),
                ("user_email", models.EmailField(max_length=254)),
                ("comment", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
