# Generated by Django 5.0.4 on 2024-07-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0005_alter_runrequest_run_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driver_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
