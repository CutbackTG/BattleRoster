from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_login_view(request):
    """
    Combined view for user signup and login.
    """
    signup_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'signup':
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, "Signup successful!")
                next_url = request.GET.get('next', reverse('characters'))
                return redirect(next_url)
            else:
                messages.error(request, "Signup failed. Please correct the errors below.")

        elif action == 'login':
            login_form = CustomAuthenticationForm(data=request.POST)
            if login_form.is_valid():
                login(request, login_form.get_user())
                messages.success(request, "Login successful!")
                next_url = request.GET.get('next', reverse('characters'))
                return redirect(next_url)
            else:
                messages.error(request, "Login failed. Please check your credentials.")

    context = {
        'signup_form': signup_form,
        'login_form': login_form,
    }
    return render(request, 'signup_login.html', context)


def logout_view(request):
    """
    Log out the current user.
    """
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')
