from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """Display checkout page and handle delivery details form"""

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            # Later this will save the order and continue to Stripe/payment
            messages.success(request, 'Delivery details saved. Continue to payment.')

            # Temporary redirect for now
            return redirect(reverse('checkout'))
        else:
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

    template = 'checkout/checkout.html'

    context = {
        'order_form': order_form,
    }

    return render(request, template, context)