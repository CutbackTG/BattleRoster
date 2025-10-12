# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def signup_login_view(request):
    """
    Handles both sign-up and log-in from one page.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'player')

        if action == 'signup':
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken.')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                return redirect('signup-login')

        elif action == 'login':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'signup-login.html')


def logout_view(request):
    """
    Logs out the current user and shows confirmation.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return render(request, "logout.html")
