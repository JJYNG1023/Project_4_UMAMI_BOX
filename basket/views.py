from django.shortcuts import render


"""Display basket page"""


def basket(request):
    return render(request, 'basket/basket.html')
