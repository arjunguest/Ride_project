# Generated by Django 5.0 on 2023-12-09 16:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.CharField(max_length=50)),
                ('pickup_location', models.CharField(max_length=50)),
                ('dropoff_location', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('on_going', 'On_going'), ('dropoff', 'Dropoff')], max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
