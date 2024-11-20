# Generated by Django 5.0.4 on 2024-11-16 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0036_equipment_vendor_invoice'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='vendor_address_1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='vendor_address_2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='vendor_city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='vendor_state',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='equipment',
            name='vendor_zip',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
