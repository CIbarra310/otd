# Generated by Django 5.0.4 on 2024-11-21 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0039_driver_driver_hire_date_driver_job_classification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='is_favorite',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
