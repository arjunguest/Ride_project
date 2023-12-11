from django.urls import path
from dashboard import views
from django.conf import settings

app_name = 'dashboard'

urlpatterns = [
    path('registration/',views.RegisterApi.as_view(), name='register_user'),
    path('login/',views.LoginView.as_view(), name='login_user'),
    path('logout/',views.LogoutView.as_view(), name='logout_user'),
    path('createride/',views.CreateRideView.as_view(), name='create_ride'),
    path('ridedetails/',views.RideDetailsView.as_view(), name='ride_details'),
    path('allride/',views.ListAllRideView.as_view(), name='all_ride'),
    path('updatestatus/<int:pk>',views.UpdateRideStatusView.as_view(), name='update_ride_status'),
    path('driver/<int:driver_id>/accept/<int:ride_request_id>/latitude/<str:origin_latitude>/longitude/<str:origin_longitude>', views.AcceptRideView.as_view(), name='driver_accept'),
]