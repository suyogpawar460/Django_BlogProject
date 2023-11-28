from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def registerView(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get('username')
            messages.success(request, f"Account has been created successfully for {username} !!")
            return redirect('login')
        else:
            username = request.POST.get('username')
            messages.warning(request, f"Account not created for {username} !!")
            return redirect('register')
    else:
        form = UserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)


@login_required
def profileView(request):
    if request.method == 'POST':
        user_update = UserUpdateForm(request.POST, instance=request.user)
        profile_update = ProfileUpdateForm(request.POST, request.FILES,
                                           instance=request.user.profile)
        if user_update.is_valid() and profile_update.is_valid():
            user_update.save()
            profile_update.save()
            messages.success(request, f"Your Profile has been updated successfully !!")
            return redirect('profile')
    else:
        user_update = UserUpdateForm(instance=request.user)
        profile_update = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'user_update': user_update,
            'profile_update': profile_update
        }
        return render(request, 'users/profile.html', context)
