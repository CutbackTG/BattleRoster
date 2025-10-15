from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


def signup_login_view(request):
    """
    Handles both user signup and login in a single view with tabs.
    """
    if request.method == "POST":
        action = request.POST.get("action")
        request.session['active_tab'] = request.POST.get("active_tab", "signup")

        # ----------- SIGNUP -----------
        if action == "signup":
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            is_dm = request.POST.get("is_dm") == "on"

            # Password match check
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect("signup_login")

            # Password validation
            try:
                validate_password(password1)
            except ValidationError as e:
                messages.error(request, " ".join(e.messages))
                return redirect("signup_login")

            # Check for existing username/email
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect("signup_login")
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect("signup_login")

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            # If your User model has 'role' or 'is_dm', set it
            if hasattr(user, "role"):
                user.role = "dungeon_master" if is_dm else "player"
                user.save()

            # Log in new user
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("characters")

        # ----------- LOGIN -----------
        elif action == "login":
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("characters")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("signup_login")

    # GET request or fallback
    return render(request, "signup_login.html")


def logout_view(request):
    """
    Logs out the user and redirects to signup/login page.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("signup_login")
