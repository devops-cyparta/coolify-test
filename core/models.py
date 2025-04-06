from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils import timezone
# from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import Q
from django.conf import settings

# Level Model 
class Level(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    img = models.ImageField(upload_to='levels/imgs/')
    def __str__(self):
        return self.name 
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a new user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    DAILY_TARGET = (
        ('15mins', '15 mins'),
        ('30mins', '30 mins'),
        ('1hour', '1 hour'),
        ('2hours', '2 hours'),
        ('4hours', '4 hours'),
        ('8hours', '8 hours'),
        ('16hours', '16 hours'),
        ('24hours', '24 hours'),
    )
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(max_length=20, unique=True)
    points = models.PositiveIntegerField(default=0) 
    current_level = models.ForeignKey(Level, on_delete=models.SET_NULL, related_name='current_level', null=True, blank=True)
    next_level = models.ForeignKey(Level, on_delete=models.SET_NULL, related_name='next_level', null=True, blank=True)
    daily_target = models.CharField(max_length=10, choices=DAILY_TARGET) 
    country = CountryField(blank=True, null=True)
    achieved_daily_target = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    def __str__(self):
        return self.email


class Customer(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_customer')
    image = models.ImageField(upload_to='pic', default='Default_Avatar/Avatar.png')

    def __str__(self):
        return self.user.first_name
    

