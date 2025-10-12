from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re


def password_is_strong(password):
    """
    Check that the password is at least 12 characters long,
    includes uppercase, lowercase, a digit, and a special character.
    """
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$")
    return bool(pattern.match(password))


def signup_login_view(request):
    """
    Combined signup and login view with server-side validation.
    """
    if request.method == "POST":
        if "signup" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            is_dm = request.POST.get("is_dm") == "on"

            # Check for existing username
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is already taken.")
                return redirect("signup-login")

            # Password match check
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect("signup-login")

            # Password strength check
            if not password_is_strong(password1):
                messages.error(
                    request,
                    "Password too weak — must be at least 12 characters long and include uppercase, lowercase, numbers, and symbols."
                )
                return redirect("signup-login")

            # Create new user
            user = User.objects.create_user(username=username, password=password1, email=email)
            user.save()

            # If DM, add to Dungeon Master group or tag (future expansion)
            if is_dm:
                user.is_staff = True
                user.save()

            messages.success(request, f"Account created successfully! Welcome, {user.username}. You can now log in.")
            return redirect("signup-login")

        elif "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("signup-login")

    return render(request, "signup_login.html")


def logout_view(request):
    """
    Logs out the current user and redirects to home.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")
