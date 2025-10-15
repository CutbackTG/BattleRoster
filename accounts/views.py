from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db import IntegrityError
from game_characters.models import Character

# ✅ Use the active custom user model
User = get_user_model()


def signup_login_view(request):
    """
    Handles both signup and login on the same page.
    Also checks for any guest-created character and saves it to the user upon login.
    """

    if request.method == "POST":
        action = request.POST.get("action")
        request.session['active_tab'] = action  # remember which tab was used

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
                # ✅ Use custom user model
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)

                # Clear tab memory after success
                request.session.pop('active_tab', None)

                messages.success(request, "Account created successfully! You are now logged in.")
                return redirect("characters")
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

                request.session.pop('active_tab', None)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("characters")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("signup_login")

    # -------------------- GET REQUEST --------------------
    return render(request, "signup_login.html")


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("home")
