# Generated by Django 5.0.4 on 2024-10-23 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transportation', '0018_picturecars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picturecars',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]