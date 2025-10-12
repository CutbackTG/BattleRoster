from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def signup_login_view(request):
    """Combined Sign-up and Log-in page."""
    if request.method == "POST":
        action = request.POST.get("action")

        # --- SIGNUP ---
        if action == "signup":
            username = request.POST.get("username")
            password = request.POST.get("password")
            role = request.POST.get("role")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect("signup-login")

        # --- LOGIN ---
        elif action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, "signup-login.html")


def logout_view(request):
    """Logs out the user."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")
