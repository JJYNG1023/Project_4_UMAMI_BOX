from django.shortcuts import render

# Create your views here.
def checkout(request):
    """Display checkout page"""
    return render(request, 'checkout/checkout.html')