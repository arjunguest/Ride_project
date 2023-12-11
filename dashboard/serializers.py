from rest_framework import serializers
from dashboard.models import RideUser, RideDetails, DriverDetails
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideUser
        fields = ('id', 'name', 'email', 'password','role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        rideUser = RideUser(**validated_data)
        rideUser.set_password(password)
        rideUser.save()
        return rideUser

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    

class CreateRideSerializer(serializers.ModelSerializer):
    driver = serializers.ChoiceField(choices=[])
    class Meta:
        model = RideDetails
        fields = ( 'pickup_location', 'dropoff_location', 'driver')
    
    def __init__(self, *args, **kwargs):
        super(CreateRideSerializer, self).__init__(*args, **kwargs)

        true_instances = DriverDetails.objects.filter(status='available')

        # Update the choices for the specific field
        self.fields['driver'].choices = [(obj.id, str(obj)) for obj in true_instances]

    


class RideDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideDetails
        fields = '__all__'

class RideStatusUpdatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideDetails
        fields = ['status']