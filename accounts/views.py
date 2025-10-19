from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_login_view(request):
    active_tab = "signup"

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            active_tab = "signup"
            form = CustomUserCreationForm(request.POST)
            login_form = CustomAuthenticationForm()
            if form.is_valid():
                user = form.save()
                messages.success(request, "Account created successfully! Please log in.")
                return redirect("signup_login")
            else:
                messages.error(request, "Sign-up failed. Please correct the errors below.")

        elif action == "login":
            active_tab = "login"
            login_form = CustomAuthenticationForm(request, data=request.POST)
            form = CustomUserCreationForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Login failed. Check your username/password.")

        else:
            form = CustomUserCreationForm()
            login_form = CustomAuthenticationForm()
    else:
        form = CustomUserCreationForm()
        login_form = CustomAuthenticationForm()

    request.session["active_tab"] = active_tab

    return render(request, "signup_login.html", {
        "form": form,
        "login_form": login_form,
    })

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("signup_login")
