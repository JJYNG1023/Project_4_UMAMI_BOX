from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile(request):
    return render(request, 'profiles/profile.html')

@login_required
def edit_profile(request):
    return render(request, 'profiles/edit_profile.html')

@login_required
def order_history(request):
    return render(request, 'profiles/order_history.html')

@login_required
def saved_meals(request):
    return render(request, 'profiles/saved_meals.html')