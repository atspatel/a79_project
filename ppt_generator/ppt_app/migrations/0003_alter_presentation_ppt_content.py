# Generated by Django 5.1.4 on 2024-12-08 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_app', '0002_presentation_num_slides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentation',
            name='ppt_content',
            field=models.JSONField(default=dict),
        ),
    ]
