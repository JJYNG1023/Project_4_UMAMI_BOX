from django.shortcuts import render
from shop.models import Product

# Create your views here.
def index(request):
    recommended_products = Product.objects.filter(is_available=True)[:5]

    context = {
        'recommended_products': recommended_products,
    }

    return render(request, 'home/index.html', context)