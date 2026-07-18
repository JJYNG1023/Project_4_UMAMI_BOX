import json
from decimal import Decimal

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from shop.models import Product
from .forms import OrderForm
from .models import OrderLineItem
import stripe
from django.conf import settings

def checkout(request):
    """Display checkout page and create order"""

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        basket_data = request.POST.get('basket_data')

        if not basket_data:
            messages.error(request, "There's nothing in your basket.")
            return redirect(reverse('shop_items'))

        try:
            basket = json.loads(basket_data)
        except json.JSONDecodeError:
            messages.error(request, "There was a problem reading your basket.")
            return redirect(reverse('basket'))

        if not basket:
            messages.error(request, "There's nothing in your basket.")
            return redirect(reverse('shop_items'))

        if order_form.is_valid():
            order = order_form.save(commit=False)

            if request.user.is_authenticated:
                order.user_profile = request.user.userprofile

            order.save()

            order_total = Decimal('0.00')

            for item in basket:
                product = get_object_or_404(Product, id=item['id'])
                quantity = int(item['quantity'])
                lineitem_total = product.price * quantity

                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    lineitem_total=lineitem_total
                )

                order_total += lineitem_total

            delivery_fee = Decimal('3.99')
            grand_total = order_total + delivery_fee

            order.order_total = order_total
            order.delivery_fee = delivery_fee
            order.grand_total = grand_total
            order.save()

            messages.success(request, 'Order created successfully.')
            return redirect(reverse('checkout_success', args=[order.id]))

        messages.error(request, 'Please check your delivery details.')

    else:
        initial_data = {}

        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile

                initial_data = {
                    'full_name': profile.full_name,
                    'email': request.user.email,
                    'phone_number': profile.phone_number,
                    'street_address_1': profile.street_address_1,
                    'street_address_2': profile.street_address_2,
                    'postcode': profile.postcode,
                    'town_or_city': profile.town_or_city,
                    'country': profile.country,
                    'delivery_notes': profile.delivery_notes,
                }
            except AttributeError:
                pass

        order_form = OrderForm(initial=initial_data)
        
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe.api_key = stripe_secret_key

    # Temporary example amount while testing
    # Later this should come from the basket total
    intent = stripe.PaymentIntent.create(
        amount=3999,
        currency="gbp",
    )

    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_id):
    """Display checkout success page and clear basket"""
    return render(request, 'checkout/checkout_success.html', {
        'order_id': order_id,
    })