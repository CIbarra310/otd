# Generated by Django 5.0.4 on 2024-11-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_location_shoot_date_location_shoot_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='shoot_day',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
