from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
"""Display the shop category landing page."""
def shop(request):
    return render(request, 'shop/shop.html')

"""Display the selected category shop products"""
def shop_items(request):
    category = request.GET.get('category', 'meal_kits')
    
    category_content = {
        'all': {
            'title': 'All Products',
            'description': 'Explore our full range of meal kits, ready meals and signature sauces.',
        },
        'meal_kits': {
            'title': 'Meal Kits',
            'description': 'Pre-portioned ingredients and signature sauces delivered together, making it easy to cook restaurant-inspired Asian meals at home.',
        },
        'ready_meals': {
            'title': 'Ready Meals',
            'description': 'Freshly prepared Asian meals, ready to heat and enjoy in minutes. Perfect for busy days without compromising on flavour.',
        },
        'signature_sauces': {
            'title': 'Signature Sauces',
            'description': 'Rich, flavour-packed homemade sauces crafted to bring authentic Asian taste to your everyday cooking.',
        },
    }

    selected_category = category_content.get(category, category_content['all'])

    products = Product.objects.all()
    if category != 'all':
        products=products.filter(category__name=category)

    context = {
        'products' : products,
        'category': category,
        'category_title': selected_category['title'],
        'category_description': selected_category['description'],
    }

    return render(request, 'shop/shop_items.html', context)

"""Display a single product detail page."""
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'shop/product_detail.html', context)
