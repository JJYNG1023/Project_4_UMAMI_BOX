from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    delivery_address = models.TextField(blank=True)
    delivery_notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username