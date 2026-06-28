from django.urls import path
from . import views

urlpatterns = [
    path('', views.basket, name='view_basket')
]
