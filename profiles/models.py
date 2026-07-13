from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    street_address_1 = models.CharField(max_length=80 , blank=True)
    street_address_2 = models.CharField(max_length=80 , blank=True)
    postcode = models.CharField(max_length=20, null=False ,blank=True)
    town_or_city = models.CharField(max_length=80, null=True, blank=True)
    country = CountryField(max_length=80, null=True ,blank=True)
    delivery_notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username