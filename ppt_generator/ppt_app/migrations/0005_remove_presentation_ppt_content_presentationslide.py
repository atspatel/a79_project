# Generated by Django 5.1.4 on 2024-12-08 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppt_app', '0004_presentation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentation',
            name='ppt_content',
        ),
        migrations.CreateModel(
            name='PresentationSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('layout_id', models.IntegerField(choices=[(0, 'Title Slide'), (1, 'Title and Content'), (2, 'Section Header'), (3, 'Two Content'), (4, 'Comparison'), (5, 'Title Only'), (6, 'Blank'), (7, 'Content with Caption'), (8, 'Picture with Caption'), (9, 'Title and Vertical Text'), (10, 'Vertical Title and Text')], default=0)),
                ('layout_name', models.CharField(choices=[('0', 'Title Slide'), ('1', 'Title and Content'), ('2', 'Section Header'), ('3', 'Two Content'), ('4', 'Comparison'), ('5', 'Title Only'), ('6', 'Blank'), ('7', 'Content with Caption'), ('8', 'Picture with Caption'), ('9', 'Title and Vertical Text'), ('10', 'Vertical Title and Text')], default='Title Slide', max_length=50)),
                ('content', models.JSONField(default=list)),
                ('index', models.PositiveIntegerField()),
                ('images', models.JSONField(default=dict)),
                ('presentation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='ppt_app.presentation')),
            ],
        ),
    ]
