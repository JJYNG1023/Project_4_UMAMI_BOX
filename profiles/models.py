from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    street_address_1 = models.CharField(max_length=80 , blank=True)
    street_address_2 = models.CharField(max_length=80 , blank=True)
    postcode = models.CharField(max_length=20 ,blank=True)
    town_or_city = models.CharField(max_length=80, blank=True)
    country = CountryField(blank_label='Country', null=True ,blank=True)
    delivery_notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

#update or create user profile    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()