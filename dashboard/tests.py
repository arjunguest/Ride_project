from django.test import TestCase
from django.contrib.auth import get_user_model
from dashboard.models import RideDetails, DriverDetails
from rest_framework.test import APIClient
from rest_framework import status

class RideDetailsModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(email='rider1@gmail.com', password='testpass')
        self.user2 = DriverDetails.objects.create(driver='driver1', status= 'available')
        self.ride = RideDetails.objects.create(
            rider=self.user1,
            driver=self.user2,
            pickup_location='Location A',
            dropoff_location='Location B',
            status='pending'
        )
    def test_ride_model(self):
        self.assertEqual(self.ride.rider, self.user1)
        self.assertEqual(self.ride.driver, self.user2)
        self.assertEqual(self.ride.pickup_location, 'Location A')
        self.assertEqual(self.ride.dropoff_location, 'Location B')
        self.assertEqual(self.ride.status, 'pending')
        self.assertIsNotNone(self.ride.created_at)

class RideDetailsAPITest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(email='rider1', password='testpass')
        self.user2 = DriverDetails.objects.create(driver='driver1', status= 'available')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_create_ride(self):
        url = '/createride/'
        data = {
            'rider': self.user1.id,
            'driver': self.user2.id,
            'pickup_location': 'Location A',
            'dropoff_location': 'Location B',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideDetails.objects.count(), 1)

    def test_get_ride_details(self):
        ride = RideDetails.objects.create(
            rider=self.user1,
            driver=self.user2,
            pickup_location='Location A',
            dropoff_location='Location B',
            status='pending'
        )
        url = f'/ridedetails/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['payload']['rider'], self.user1.id)
        self.assertEqual(response.data['payload']['driver'], self.user2.id)
        # Add more assertions based on your specific data

    def test_list_rides(self):
        RideDetails.objects.create(
            rider=self.user1,
            driver=self.user2,
            pickup_location='Location A',
            dropoff_location='Location B',
        )
        url = '/allride/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)