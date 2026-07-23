from django.db import models
from django_countries.fields import CountryField

from profiles.models import UserProfile
from shop.models import Product


class Order(models.Model):
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    street_address_1 = models.CharField(max_length=80)
    street_address_2 = models.CharField(max_length=80, blank=True)
    postcode = models.CharField(max_length=20)
    town_or_city = models.CharField(max_length=80)
    country = CountryField(blank_label='Country')
    delivery_notes = models.TextField(blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    delivery_time = models.TimeField(null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stripe_pid = models.CharField(max_length=254, unique=True, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default='pending')
    confirmation_email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
    

