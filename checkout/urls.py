from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/<int:order_id>/', views.checkout_success, name='checkout_success'),
    path('delivery-date/<int:order_id>/', views.delivery_date, name='delivery_date'),
]