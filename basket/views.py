from django.shortcuts import render

def basket(request):
    """Display basket page"""
    return render(request, 'basket/basket.html')