# Generated by Django 5.0.4 on 2024-10-24 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0024_remove_driver_assigned_vehicle_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='assigned_trailer',
            field=models.ManyToManyField(limit_choices_to={'equipment_type_1': 'trailer'}, related_name='assigned_trailer', to='transportation.equipment'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='assigned_truck',
            field=models.ManyToManyField(limit_choices_to={'equipment_type_1': 'truck'}, related_name='assigned_truck', to='transportation.equipment'),
        ),
    ]
