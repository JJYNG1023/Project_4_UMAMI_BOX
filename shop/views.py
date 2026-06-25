from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product

# Create your views here.
"""Display the shop category landing page."""
def shop(request):
    return render(request, 'shop/shop.html')

"""Display the selected category shop products"""
def shop_items(request):
    category = request.GET.get('category', 'all')
    cuisine = request.GET.get('cuisine')
    dietary = request.GET.get('dietary')
    sort = request.GET.get('sort')
    query = request.GET.get('q')
    
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
    
    # Category filter
    if category != 'all':
        products=products.filter(category__name=category)

    # Cuisine filter using tags
    if cuisine :
        products = products.filter(tag__name=cuisine)

    # Cuisine dietary using tags
    if dietary:
        products = products.filter(tag__name=dietary)

    # If filter
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        )

    # Search Filter
    if sort == 'cooking_time' :
        products = products.order_by('cooking_time')

    elif sort == 'price_low_high' :
        products = products.order_by('price')

    elif sort == 'price_high_low' :
        products = products.order_by('-price')

    products = products.distinct()
    
    context = {
        'products' : products,
        'category': category,
        'category_title': selected_category['title'],
        'category_description': selected_category['description'],
        'current_cuisine': cuisine,
        'current_dietary': dietary,
        'current_sort': sort,
        'search_query': query,
    }

    return render(request, 'shop/shop_items.html', context)

"""Display a single product detail page."""
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    ingredients_list=[]
    if product.ingredients:
        ingredients_list = [item.strip() for item in product.ingredients.split(',')]

    related_products = Product.objects.exclude(pk=product.pk)[:5]

    context = {
        'product': product,
        'ingredients_list':ingredients_list,
        'related_products': related_products,
    }
    
    return render(request, 'shop/product_detail.html', context)
