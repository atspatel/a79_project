# Generated by Django 5.1.4 on 2024-12-08 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_app', '0005_remove_presentation_ppt_content_presentationslide'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentationslide',
            name='images',
        ),
    ]