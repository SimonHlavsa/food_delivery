from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="customer")

class RestaurantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type="restaurant")

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email musí být vyplněn')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):

    USER_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
    )
    user_type = models.CharField(max_length=20, choices=USER_CHOICES)

    email = models.EmailField(unique=True)
    restaurant_name = models.CharField(max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)    

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserProfileManager()
    customer = CustomerManager()
    restaurant = RestaurantManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        if self.user_type == "restaurant":
            return self.restaurant_name
        else:
            return self.email




