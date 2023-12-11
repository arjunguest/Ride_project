from django.contrib import admin
from dashboard.models import RideUser, RideDetails, DriverDetails
# Register your models here.

admin.site.register(RideUser),
admin.site.register(RideDetails),
admin.site.register(DriverDetails),
