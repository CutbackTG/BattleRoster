from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Party, Character


def home_view(request):
    """Landing page view."""
    return render(request, 'index.html')


def characters_view(request):
    """Show character list and allow limited character creation for guests."""
    user = request.user
    guest_mode = not user.is_authenticated

    # Guest users see demo characters (not saved to DB)
    if guest_mode:
        characters = []  # no stored characters
    else:
        characters = Character.objects.filter(player=user)

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")
        health = request.POST.get("health")
        mana = request.POST.get("mana")

        if guest_mode:
            messages.warning(request, "Login required to save your character.")
        else:
            if not all([name, level, health, mana]):
                messages.error(request, "All fields are required.")
            else:
                Character.objects.create(
                    name=name,
                    level=level,
                    health=health,
                    mana=mana,
                    player=user
                )
                messages.success(request, f"Character '{name}' created successfully!")
            return redirect("characters")

    return render(request, "characters.html", {
        "characters": characters,
        "guest_mode": guest_mode,
    })


def party_view(request):
    """Display the user's party info or show guest preview."""
    user = request.user
    guest_mode = not user.is_authenticated

    if guest_mode:
        messages.info(request, "Login to manage or join parties.")
        parties = Party.objects.all()[:3]  # show a few sample parties (or none)
    else:
        if hasattr(user, "role") and user.role == "dungeon_master":
            parties = Party.objects.filter(dungeon_master=user)
        else:
            parties = Party.objects.filter(members=user)

    # Only allow add/remove for logged-in Dungeon Masters
    if request.method == "POST" and not guest_mode:
        action = request.POST.get("action")
        party_id = request.POST.get("party_id")
        username = request.POST.get("username")

        try:
            party = Party.objects.get(id=party_id, dungeon_master=user)
        except Party.DoesNotExist:
            messages.error(request, "Party not found or permission denied.")
            return redirect("party")

        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect("party")

        if action == "add":
            party.members.add(target_user)
            messages.success(request, f"{username} added to {party.name}.")
        elif action == "remove":
            party.members.remove(target_user)
            messages.info(request, f"{username} removed from {party.name}.")
        return redirect("party")

    return render(request, "party.html", {
        "parties": parties,
        "guest_mode": guest_mode,
    })
