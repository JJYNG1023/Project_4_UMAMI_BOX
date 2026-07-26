from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('items/', views.shop_items, name='shop_items'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
]
