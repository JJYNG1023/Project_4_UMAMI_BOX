from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('orders/', views.order_history, name='order_history'),
    path('saved-meals/', views.saved_meals, name='saved_meals'),
    path('toggle-saved-meal/<int:product_id>/', views.toggle_saved_meal, name='toggle_saved_meal'),
]