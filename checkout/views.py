import json
from decimal import Decimal

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from shop.models import Product
from .forms import OrderForm, DeliveryDateForm
from .models import Order, OrderLineItem
import stripe
from .utils import send_order_confirmation_email

def checkout(request):
    """Display checkout page and create order from delivery details"""

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
            return redirect(reverse('view_basket'))

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

            messages.success(request, 'Delivery details saved.')
            return redirect(reverse('delivery_date', args=[order.id]))

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
                }
            except AttributeError:
                pass

        order_form = OrderForm(initial=initial_data)

    context = {
        'order_form': order_form,
    }

    return render(request, 'checkout/checkout.html', context)


def delivery_date(request, order_id):
    """Allow user to choose delivery date, time and delivery notes"""

    order = get_object_or_404(Order, id=order_id)

    if request.user.is_authenticated:
        if order.user_profile and order.user_profile != request.user.userprofile:
            messages.error(request, 'You do not have permission to edit this order.')
            return redirect(reverse('shop_items'))

    if request.method == 'POST':
        form = DeliveryDateForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            messages.success(request, 'Delivery date saved.')

            return redirect(reverse('payment', args=[order.id]))

        messages.error(request, 'Please check your delivery date and time.')

    else:
        form = DeliveryDateForm(instance=order)

    context = {
        'form': form,
        'order': order,
    }

    return render(request, 'checkout/delivery_date.html', context)

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user.is_authenticated:
        if order.user_profile and order.user_profile !=request.user.userprofile:
            messages.error(request,'you do not have permission to pay for this order.')
            return redirect(reverse('shop_items'))
    
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key

    if request.method == 'POST':
        payment_intent_id = request.POST.get('payment_intent_id')

        if payment_intent_id:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            if payment_intent.status == 'succeeded':
                order.stripe_pid = payment_intent.id
                order.payment_status = 'paid'
                order.save()

                send_order_confirmation_email(order)

                messages.success(request, 'Payment Successful')
                return redirect(reverse('checkout_success', args=[order.id]))
        
        messages.error(request,'Payment could not be confirmed')
        return redirect(reverse('payment', args=[order.id]))

    stripe_total = int(order.grand_total * Decimal('100'))

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency='gbp',
        metadata={
            'order_id': order.id,
        }
    )

    context = {
        'order': order,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/payment.html', context)

def checkout_success(request, order_id):
    """Display checkout success page and clear basket"""

    order = get_object_or_404(Order, id=order_id)

    return render(request, 'checkout/checkout_success.html', {
        'order': order,
    })