from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def signup_login_view(request):
    """
    Handles both sign-up and login in a single view.
    Uses hidden 'action' field in the form to distinguish.
    """
    active_tab = "signup"  # default active tab

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            active_tab = "signup"
            form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if form.is_valid():
                user = form.save()
                messages.success(request, "Account created successfully! Please log in.")
                # Optionally, you can log the user in immediately:
                # login(request, user)
                return redirect("signup_login")
            else:
                messages.error(request, "Sign-up failed. Please correct the errors below.")

        elif action == "login":
            active_tab = "login"
            login_form = AuthenticationForm(request, data=request.POST)
            form = UserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("/")  # or use LOGIN_REDIRECT_URL
            else:
                messages.error(request, "Login failed. Check your username/password.")

        else:
            # fallback
            form = UserCreationForm()
            login_form = AuthenticationForm()
    else:
        # GET request
        form = UserCreationForm()
        login_form = AuthenticationForm()

    # store the active tab in session so your template can highlight it
    request.session["active_tab"] = active_tab

    return render(request, "signup_login.html", {
        "form": form,
        "login_form": login_form,
    })


def logout_view(request):
    """Logs out the user and redirects to signup/login page"""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("signup_login")
