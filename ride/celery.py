# yourprojectname/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ride.settings')

# create a Celery instance and configure it using the settings from Django
app = Celery('ride')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-location': {
        'task': 'dashboard.tasks.update_ride_location',
        'schedule': crontab(minute='*/1'),
    },
}
