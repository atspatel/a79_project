# Generated by Django 5.1.4 on 2024-12-08 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_app', '0003_alter_presentation_ppt_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
    ]
