# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

def signup_login_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        request.session['active_tab'] = request.POST.get("active_tab", "signup")

        if action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            is_dm = request.POST.get("is_dm") == "on"

            # Basic password match check
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect("signup_login")

            # Validate password using Django validators
            try:
                validate_password(password1)
            except ValidationError as e:
                messages.error(request, "; ".join(e.messages))
                return redirect("signup_login")

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect("signup_login")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect("signup_login")

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Set additional field if exists
            if hasattr(user, "is_dm"):
                user.is_dm = is_dm
                user.save()

            # Automatically log the user in
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("characters")

        elif action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("characters")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("signup_login")

    # GET request or fallback
    return render(request, "signup_login.html")
