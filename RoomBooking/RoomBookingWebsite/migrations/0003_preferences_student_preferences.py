# Generated by Django 5.0.14 on 2025-04-24 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoomBookingWebsite', '0002_remove_administrator_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smoking', models.BooleanField(default=False)),
                ('drinking', models.BooleanField(default=False)),
                ('tidy', models.BooleanField(default=False)),
                ('sleeping', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='preferences',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_preferences', to='RoomBookingWebsite.preferences'),
        ),
    ]
