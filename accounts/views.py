from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Character

# -----------------------------
# Index view
# -----------------------------
def index_view(request):
    return render(request, "index.html")

# -----------------------------
# Helper to safely convert numeric values
# -----------------------------
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# -----------------------------
# Character management
# -----------------------------
def characters_view(request, pk=None):
    editing = None

    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    if pk is not None:
        if request.user.is_authenticated:
            editing = get_object_or_404(Character, pk=pk, player=request.user)
        else:
            if int(pk) >= len(characters):
                messages.error(request, "Character not found.")
                return redirect("characters")
            editing = characters[int(pk)]

    if request.method == "POST":
        numeric_fields = ["level", "health", "mana", "strength", "dexterity",
                          "constitution", "intelligence", "wisdom", "charisma"]
        string_fields = ["name", "race", "class_type", "equipment", "weapons", "spells"]

        data = {}
        for field in numeric_fields:
            data[field] = to_int(request.POST.get(field, ""), getattr(editing, field, 0) if editing and request.user.is_authenticated else 0)
        for field in string_fields:
            data[field] = request.POST.get(field, "").strip()

        if editing:  # Update existing
            if request.user.is_authenticated:
                for key, value in data.items():
                    setattr(editing, key, value)
                editing.save()
            else:
                characters[int(pk)].update(data)
                request.session["characters"] = characters
            messages.success(request, f"Character '{data['name']}' updated successfully!")
        else:  # Create new
            if request.user.is_authenticated:
                Character.objects.create(player=request.user, **data)
            else:
                if len(characters) >= 1:
                    messages.info(request, "Please sign up or log in to create additional characters.")
                    return redirect("/accounts/signup_login/?next=/characters/")
                characters.append(data)
                request.session["characters"] = characters
            messages.success(request, f"Character '{data['name']}' created successfully!")

        return redirect("characters")

    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(request, "characters.html", {
        "characters": characters,
        "attributes": attributes,
        "editing": editing,
        "pk": pk
    })

def character_delete(request, pk):
    if request.user.is_authenticated:
        character = get_object_or_404(Character, pk=pk, player=request.user)
        character.delete()
    else:
        characters = request.session.get("characters", [])
        if int(pk) < len(characters):
            characters.pop(int(pk))
            request.session["characters"] = characters
    messages.success(request, "Character deleted successfully!")
    return redirect("characters")

# -----------------------------
# Signup / Login
# -----------------------------
def signup_login_view(request):
    if request.method == 'POST':
        if 'signup' in request.POST:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Signup successful!")
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(request, "Signup failed. Please check the form.")
        elif 'login' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                messages.success(request, "Login successful!")
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(request, "Login failed. Please check your credentials.")
    else:
        form = UserCreationForm()

    return render(request, 'accounts/signup_login.html', {'form': form})

# -----------------------------
# Logout
# -----------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/')
