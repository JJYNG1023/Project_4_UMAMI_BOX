from django.shortcuts import render
from shop.models import Product


# Create your views here.
def index(request):
    recommended_products = Product.objects.filter(is_available=True)[:5]

    context = {
        'recommended_products': recommended_products,
    }

    return render(request, 'home/index.html', context)


def how_it_works(request):
    """Display the how UMAMI BOX works page."""
    return render(request, 'home/how_it_works.html')


def sustainability(request):
    """Display the sustainability page."""
    return render(request, 'home/sustainability.html')


def about_us(request):
    """Display the about us page."""
    return render(request, 'home/about_us.html')
