# Generated by Django 5.0.4 on 2024-10-23 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_production_code'),
        ('transportation', '0015_driver_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Vehicle',
            new_name='Equipment',
        ),
        migrations.CreateModel(
            name='DriverDailyRundown',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('drivers', models.ManyToManyField(to='transportation.driver')),
                ('equipment', models.ManyToManyField(to='transportation.equipment')),
                ('production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.production')),
            ],
        ),
    ]