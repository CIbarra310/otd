# Generated by Django 5.0.4 on 2024-11-13 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0031_drivertimes_meal_penalty_3'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivertimes',
            name='times_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]