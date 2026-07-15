from django.contrib import admin
from .models import UserProfile, SavedMeal
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(SavedMeal)