# Generated by Django 5.1.4 on 2024-12-08 00:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='num_slides',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)]),
        ),
    ]