from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

# Create your views here.

@login_required
def profile(request):
    return render(request, 'profiles/profile.html')

@login_required
def edit_profile(request):
    
    user_profile, created =UserProfile.objects.get_or_create(user=request.user)

    if request.method=='POST':
        if 'delete_account' in request.POST:
            request.user.delete()
            messages.success(request, ' Your account has been deleted.')
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
    return render(request, 'profiles/saved_meals.html')