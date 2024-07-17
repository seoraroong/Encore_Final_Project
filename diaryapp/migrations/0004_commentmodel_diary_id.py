# Generated by Django 4.1.13 on 2024-07-16 09:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diaryapp", "0003_commentmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="commentmodel",
            name="diary_id",
            field=models.ManyToManyField(
                related_name="diary_comments", to="diaryapp.aiwritemodel"
            ),
        ),
    ]
