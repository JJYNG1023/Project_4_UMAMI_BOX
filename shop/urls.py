from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='shop'),
    path('items/', views.shop_items, name='shop_items'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
