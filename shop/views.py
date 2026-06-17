from django.shortcuts import render

# Create your views here.
"""Display the shop category landing page."""
def shop(request):
    return render(request, 'shop/shop.html')

"""Display the selected category shop products"""
def shop_items(request):
    return render(request, 'shop/shop_items.html')

"""Display a single product detail page."""
def product_detail(request):
    return render(request,'product_detail.html')