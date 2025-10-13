from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Party, Character
from .google_sheets import get_gsheet


def home_view(request):
    """Landing page view."""
    return render(request, 'index.html')


def characters_view(request):
    """
    Display the user's characters.
    Allow logged-in users to add characters directly from this page.
    """
    user = request.user
    guest_mode = not user.is_authenticated

    # Guests see no saved characters
    if guest_mode:
        characters = []
    else:
        characters = Character.objects.filter(player=user)

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")
        health = request.POST.get("health")
        mana = request.POST.get("mana")

        # Validation
        if not all([name, level, health, mana]):
            messages.error(request, "All fields are required.")
            return redirect("characters")

        if guest_mode:
            messages.warning(request, "Please log in to save characters.")
            return redirect("signup_login")

        # Create the new character
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


@login_required
def update_character(request, row_number):
    """Update a character’s details."""
    sheet = get_gsheet("Characters")

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level")
        health = request.POST.get("health")
        mana = request.POST.get("mana")

        sheet.update(f"A{row_number}:D{row_number}", [[name, level, health, mana]])
        messages.success(request, "Character updated successfully.")
        return redirect("characters")


@login_required
def delete_character(request, row_number):
    """Delete a character by its row number in the Google Sheet."""
    sheet = get_gsheet("Characters")
    sheet.delete_rows(row_number)
    messages.success(request, "Character deleted.")
    return redirect("characters")


def party_view(request):
    """Display parties depending on the user’s role."""
    user = request.user
    guest_mode = not user.is_authenticated

    if guest_mode:
        messages.info(request, "Login to manage or join parties.")
        parties = Party.objects.all()[:3]
    else:
        if hasattr(user, "role") and user.role == "dungeon_master":
            parties = Party.objects.filter(dungeon_master=user)
        else:
            parties = Party.objects.filter(members=user)

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


def contact_view(request):
    """Render the contact page."""
    return render(request, "contact.html")
