from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Character, Party


def home_view(request):
    """Landing page view."""
    return render(request, "index.html")


def characters_view(request):
    """
    Displays the character list and handles both guest and user character creation.
    Guests’ characters are session-based (temporary).
    """

    user = request.user
    guest_mode = not user.is_authenticated

    # Get characters for authenticated users
    if not guest_mode:
        characters = Character.objects.filter(player=user)
    else:
        # Retrieve temporary guest characters from session
        characters = request.session.get("guest_characters", [])

    if request.method == "POST":
        # Extract all form fields
        data = {
            "name": request.POST.get("name"),
            "race": request.POST.get("race"),
            "char_class": request.POST.get("char_class"),
            "background": request.POST.get("background"),
            "alignment": request.POST.get("alignment"),
            "level": request.POST.get("level", 1),
            "strength": request.POST.get("strength", 10),
            "dexterity": request.POST.get("dexterity", 10),
            "constitution": request.POST.get("constitution", 10),
            "intelligence": request.POST.get("intelligence", 10),
            "wisdom": request.POST.get("wisdom", 10),
            "charisma": request.POST.get("charisma", 10),
            "traits": request.POST.get("traits"),
            "ideals": request.POST.get("ideals"),
            "bonds": request.POST.get("bonds"),
            "flaws": request.POST.get("flaws"),
            "equipment": request.POST.get("equipment"),
            "weapons": request.POST.get("weapons"),
            "spells": request.POST.get("spells"),
            "notes": request.POST.get("notes"),
        }

        if not data["name"]:
            messages.error(request, "Character must have a name.")
            return redirect("characters")

        if guest_mode:
            # Save to session
            guest_chars = request.session.get("guest_characters", [])
            guest_chars.append(data)
            request.session["guest_characters"] = guest_chars
            messages.info(request, f"Temporary character '{data['name']}' created.")
        else:
            # Save to DB
            Character.objects.create(player=user, **data)
            messages.success(request, f"Character '{data['name']}' saved to your account.")

        return redirect("characters")

    return render(
        request,
        "characters.html",
        {"characters": characters, "guest_mode": guest_mode},
    )


@login_required
def party_view(request):
    """Display or manage parties."""
    user = request.user

    if user.role == "dungeon_master":
        parties = Party.objects.filter(dungeon_master=user)
    else:
        parties = Party.objects.filter(members=user)

    return render(request, "party.html", {"parties": parties})


def contact_view(request):
    """Contact page."""
    return render(request, "contact.html")
