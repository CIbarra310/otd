# Generated by Django 5.0.4 on 2024-11-23 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0040_driver_is_favorite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycrew',
            name='my_crew_driver_hire_date',
        ),
        migrations.AddField(
            model_name='mycrew',
            name='favorite_drivers',
            field=models.ManyToManyField(blank=True, related_name='my_crews', to='transportation.driver'),
        ),
    ]
