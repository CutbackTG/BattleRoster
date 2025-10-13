from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from game_characters.models import Character


def signup_login_view(request):
    """
    Handles both signup and login on the same page.
    Also checks for any guest-created character and saves it to the user upon login.
    """

    if request.method == "POST":
        action = request.POST.get("action")

        # -------------------- SIGNUP --------------------
        if action == "signup":
            username = request.POST.get("username")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            # Validation checks
            if not username or not password1 or not password2:
                messages.error(request, "All fields are required.")
                return redirect("signup_login")

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect("signup_login")

            if len(password1) < 12:
                messages.error(request, "Password must be at least 12 characters long.")
                return redirect("signup_login")

            if not any(char.isdigit() for char in password1) or not any(char.isalpha() for char in password1):
                messages.error(request, "Password must contain both letters and numbers.")
                return redirect("signup_login")

            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                messages.success(request, "Account created successfully! You are now logged in.")
                return redirect("party")
            except IntegrityError:
                messages.error(request, "That username is already taken.")
                return redirect("signup_login")

        # -------------------- LOGIN --------------------
        elif action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # If guest created a temporary character, attach it
                temp = request.session.pop("temp_character", None)
                if temp:
                    Character.objects.create(
                        name=temp["name"],
                        level=temp["level"],
                        health=temp["health"],
                        mana=temp["mana"],
                        player=user,
                    )
                    messages.success(request, f"Your character '{temp['name']}' has been saved to your account!")

                messages.success(request, f"Welcome back, {username}!")
                next_page = request.GET.get("next", "party")
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("signup_login")

    # -------------------- GET REQUEST --------------------
    return render(request, "signup-login.html")


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")
