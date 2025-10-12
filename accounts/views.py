from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import re


def signup_login_view(request):
    """
    Handles both sign-up and log-in from one page.
    Includes password strength and confirmation validation.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'player')

        # Handle SIGN-UP
        if action == 'signup':
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken. Please choose another.')
                return redirect('signup-login')

            # Validate password match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('signup-login')

            # Validate password strength
            if not validate_password_strength(password):
                messages.error(
                    request,
                    'Password must be at least 12 characters long and include uppercase, lowercase, numbers, and special characters.'
                )
                return redirect('signup-login')

            # Create user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('signup-login')

        # Handle LOG-IN
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
    """Logs out the current user and redirects to home."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# 🔒 Password validation helper
def validate_password_strength(password):
    """
    Ensures the password meets strong security criteria:
    - At least 12 characters
    - Includes uppercase, lowercase, number, and special character
    """
    if len(password) < 12:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True
