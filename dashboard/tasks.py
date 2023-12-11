from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from time import sleep
import random

@shared_task
def update_ride_location(latitude=0, longitude=0):

    new_latitude = latitude + random.uniform(-0.05, 0.05)
    new_longitude = longitude + random.uniform(-0.05, 0.05)

    new_latitude = max(min(new_latitude, 90), -90)
    new_longitude = max(min(new_longitude, 180), -180)

    print(f"Updated location : Lat: {new_latitude}, Lon: {new_longitude}")