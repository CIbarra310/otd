# Generated by Django 5.0.4 on 2024-10-24 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0025_alter_driver_assigned_trailer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='equipment_type_1',
            field=models.CharField(choices=[('truck', 'Truck'), ('trailer', 'Trailer')], max_length=150, null=True),
        ),
    ]