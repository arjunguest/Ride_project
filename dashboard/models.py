from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager

from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

ROLE_CHOICES = (
    ("user", "User"),
    ("driver", "Driver"),
    ("admin", "Admin"),
)

class RideUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.role = "admin"
        user.is_staff = True
        user.save(using=self._db)
        return user

class RideUser(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length = 20, choices = ROLE_CHOICES, default = 'user')
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = RideUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
DIVER_STATUS = (
    ('available', 'Available'),
    ("unavailable", "Unavailable"),
)
class DriverDetails(models.Model):
    driver = models.CharField(max_length=50)
    status = models.CharField(max_length = 20, choices = DIVER_STATUS, default='available')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.driver

STATUS = (
    ('pending', 'Pending'),
    ("started", "Started"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
)

class RideDetails(models.Model):
    rider = models.ForeignKey(RideUser, on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverDetails, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=50)
    dropoff_location = models.CharField(max_length=50)
    status = models.CharField(max_length = 20, choices = STATUS, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.rider.name

