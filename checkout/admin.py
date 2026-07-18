from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'date',
        'order_total',
        'delivery_fee',
        'grand_total',
    )

    fields = (
        'user_profile',
        'full_name',
        'email',
        'phone_number',
        'street_address_1',
        'street_address_2',
        'postcode',
        'town_or_city',
        'country',
        'delivery_notes',
        'date',
        'order_total',
        'delivery_fee',
        'grand_total',
    )

    list_display = (
        'id',
        'full_name',
        'date',
        'order_total',
        'delivery_fee',
        'grand_total',
    )

    ordering = ('-date',)