# Generated by Django 5.0.14 on 2025-04-26 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomBookingWebsite', '0006_building_bathroom_type_building_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='gender',
            field=models.CharField(choices=[('men', 'men'), ('women', 'women'), ('coed', 'coed')], default='-', max_length=50),
        ),
    ]
