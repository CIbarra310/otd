# Generated by Django 5.0.4 on 2024-11-11 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0030_drivertimes_meal_penalty_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivertimes',
            name='meal_penalty_3',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
