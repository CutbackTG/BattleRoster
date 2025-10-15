from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Character, Party
from django.contrib.auth import get_user_model

User = get_user_model()

# ------------------------------
# HOME PAGE
# ------------------------------
def index(request):
    """Homepage view."""
    return render(request, "index.html")


# ------------------------------
# CHARACTER PAGE
# ------------------------------
def characters_view(request):
    """
    View for creating and viewing characters.
    Anonymous users can still create characters,
    but characters won’t be tied to a registered user.
    """
    characters = None

    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user)
    else:
        characters = Character.objects.none()  # No saved characters for anonymous users

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level", 1)
        health = request.POST.get("health", 100)
        mana = request.POST.get("mana", 50)

        if name:
            if request.user.is_authenticated:
                Character.objects.create(
                    name=name,
                    level=level,
                    health=health,
                    mana=mana,
                    player=request.user,
                )
            else:
                # Create a character not linked to a registered user
                Character.objects.create(
                    name=name,
                    level=level,
                    health=health,
                    mana=mana,
                    player=None,
                )
            return redirect("characters")

    context = {
        "characters": characters,
    }
    return render(request, "characters.html", context)


# ------------------------------
# PARTY PAGE
# ------------------------------
@login_required
def party_view(request):
    """View to manage parties for logged-in users."""
    parties = Party.objects.filter(members=request.user) | Party.objects.filter(dungeon_master=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Party.objects.create(name=name, dungeon_master=request.user)
            return redirect("party")

    return render(request, "party.html", {"parties": parties})


# ------------------------------
# CONTACT PAGE
# ------------------------------
def contact_view(request):
    """Simple contact page view."""
    return render(request, "contact.html")
