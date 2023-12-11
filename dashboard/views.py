from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from django.utils import timezone

from django.db import models
import json
from rest_framework import generics

from django.contrib.auth import get_user_model

from dashboard.models import RideUser, RideDetails, DriverDetails

from dashboard.tasks import update_ride_location

from dashboard.serializers import RegisterSerializer, LoginSerializer, CreateRideSerializer, RideDetailsSerializer, RideStatusUpdatesSerializer

# Create your views here.

class RegisterApi(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'payload':serializer.data, 'message':"User registered successfully"}, status = status.HTTP_200_OK)
            else:
                return Response({'status':403, 'errors': serializer.errors,'message':"Error registering user"})
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    api_view = ['POST']
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return Response({'payload':serializer.data,'message':"Login successfully"}, status = status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials.'}, status = status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': ' Please fill vaild data'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class CreateRideView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRideSerializer

    def post(self, request, format=None):
        try:

            serializer = CreateRideSerializer(data = request.data)
            if serializer.is_valid():
                driver = DriverDetails.objects.get(id = serializer.validated_data['driver'])
                ride = RideDetails.objects.create(
                    rider = request.user,
                    driver = driver,
                    pickup_location = serializer.validated_data['pickup_location'],
                    dropoff_location = serializer.validated_data['dropoff_location'],
                )
                ride.save()

            return Response({'payload':serializer.data,'message':"Ride created successfully"}, status = status.HTTP_201_CREATED)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class RideDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RideDetailsSerializer

    def get(self, request, format=None):
        try:
            user = request.user
            last_ride = RideDetails.objects.filter(rider = user ).last()
            if last_ride:
                serializer = RideDetailsSerializer(last_ride)
                return Response({'payload':serializer.data,'message':"Current ride details"}, status = status.HTTP_200_OK)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)

class ListAllRideView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RideDetailsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
         ride_list = RideDetails.objects.filter(rider = self.request.user)
         return ride_list
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data)
            return response_data
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class UpdateRideStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RideDetails.objects.all()
    serializer_class = RideStatusUpdatesSerializer
    lookup_field = 'pk'

class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, driver_id, ride_request_id,origin_latitude,origin_longitude):
        try:
            driver = DriverDetails.objects.get(id=driver_id)
            ride_request = RideDetails.objects.get(id=ride_request_id)
            latitude = float(origin_latitude)
            longitude = float(origin_longitude)
            ride_request.status = 'started'
            driver.status = 'unavailable'
            ride_request.save()
            driver.save()
            update_ride_location.delay(latitude, longitude)
            return Response({'message':" Ride Accepted"}, status = status.HTTP_200_OK)
        except Exception as e:
            print("Error--------:",str(e))
            return Response({'message': str(e)}, status = status.HTTP_400_BAD_REQUEST)