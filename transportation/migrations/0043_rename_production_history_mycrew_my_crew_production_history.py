# Generated by Django 5.0.4 on 2024-11-23 03:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0042_remove_mycrew_favorite_drivers_productionhistory_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mycrew',
            old_name='production_history',
            new_name='my_crew_production_history',
        ),
    ]