from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm
from django.db.models import Q
from shop.models import Product, Category
from .models import SavedMeal

# Create your views here.

@login_required
def profile(request):
    return render(request, 'profiles/profile.html')

@login_required
def edit_profile(request):
    
    user_profile, created =UserProfile.objects.get_or_create(user=request.user)

    if request.method=='POST':
        
        if 'delete_account' in request.POST:
            user = request.user
            logout(request)
            user.delete()

            messages.success(request, 'Your account has been deleted.')
            return redirect('account_login')
        
        form = UserProfileForm(
            request.POST,
            instance= user_profile,
            user=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(request,'Profile updated successfully.')
            return redirect('edit_profile')
    else:
        form = UserProfileForm (
            instance = user_profile,
            user=request.user
        )


    context = {
        'form': form,
    }

    return render(request, 'profiles/edit_profile.html', context)

@login_required
def order_history(request):
    return render(request, 'profiles/order_history.html')

@login_required
def saved_meals(request):
    saved_products = Product.objects.filter(
        savedmeal__user=request.user
    )

    search_query = request.GET.get('q')
    selected_category = request.GET.get('category')

    if search_query:
        saved_products = saved_products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if selected_category:
        saved_products = saved_products.filter(
            category__name=selected_category
        )

    categories = Category.objects.all()

    context = {
        'saved_products': saved_products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': selected_category,
    }

    return render(request, 'profiles/saved_meals.html', context)


@login_required
def toggle_saved_meal(request, product_id):
    """Save or remove a product from the user's saved meals."""

    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        saved_meal, created = SavedMeal.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            saved_meal.delete()
            saved = False
        else:
            saved = True

        return JsonResponse({
            'saved': saved,
            'product_name': product.name,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)