# Generated by Django 4.1.13 on 2024-08-09 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='areaBaseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('areacode', models.CharField(max_length=10)),
                ('sigungucode', models.CharField(max_length=10)),
                ('cat3', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=50)),
                ('mapx', models.CharField(max_length=50)),
                ('mapy', models.CharField(max_length=50)),
                ('addr1', models.CharField(max_length=50)),
                ('firstimage', models.CharField(max_length=100)),
                ('overview', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'areaBaseList',
            },
        ),
        migrations.CreateModel(
            name='areaCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'areaCode',
            },
        ),
        migrations.CreateModel(
            name='categoryCode1',
            fields=[
                ('_id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('rnum', models.IntegerField()),
            ],
            options={
                'db_table': 'categoryCode1',
            },
        ),
        migrations.CreateModel(
            name='categoryCode2',
            fields=[
                ('_id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('cat1_code', models.CharField(max_length=10)),
                ('rnum', models.IntegerField()),
            ],
            options={
                'db_table': 'categoryCode2',
            },
        ),
        migrations.CreateModel(
            name='categoryCode3',
            fields=[
                ('_id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('cat2_code', models.CharField(max_length=10)),
                ('rnum', models.IntegerField()),
            ],
            options={
                'db_table': 'categoryCode3',
            },
        ),
        migrations.CreateModel(
            name='cityDistrict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=10)),
                ('areacode', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'cityDistrict',
            },
        ),
    ]
