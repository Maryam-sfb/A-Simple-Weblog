# Generated by Django 3.1.2 on 2021-03-28 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_auto_20210326_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=120, unique=True),
        ),
    ]