# Generated by Django 5.0.14 on 2025-04-26 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomBookingWebsite', '0009_merge_20250425_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='building_name',
            field=models.CharField(default='error', max_length=100),
        ),
    ]
