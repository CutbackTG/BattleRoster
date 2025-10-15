from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Character, Party
User = get_user_model()



def home_view(request):
    """Landing page view."""
    return render(request, 'index.html')


def characters_view(request):
    """Character creation and list view."""
    user = request.user
    guest_mode = not user.is_authenticated

    if request.method == "POST":
        name = request.POST.get("name")
        level = request.POST.get("level", 1)
        race = request.POST.get("race")
        class_type = request.POST.get("class_type")
        strength = request.POST.get("strength", 10)
        dexterity = request.POST.get("dexterity", 10)
        constitution = request.POST.get("constitution", 10)
        intelligence = request.POST.get("intelligence", 10)
        wisdom = request.POST.get("wisdom", 10)
        charisma = request.POST.get("charisma", 10)
        equipment = request.POST.get("equipment")
        weapons = request.POST.get("weapons")
        spells = request.POST.get("spells")

        if not name:
            messages.error(request, "Character name is required.")
        else:
            if guest_mode:
                messages.info(request, "Guest character created (not saved).")
            else:
                Character.objects.create(
                    name=name,
                    level=level,
                    race=race,
                    class_type=class_type,
                    strength=strength,
                    dexterity=dexterity,
                    constitution=constitution,
                    intelligence=intelligence,
                    wisdom=wisdom,
                    charisma=charisma,
                    equipment=equipment,
                    weapons=weapons,
                    spells=spells,
                    player=user
                )
                messages.success(request, f"Character '{name}' created successfully!")

        return redirect("characters")

    characters = Character.objects.filter(player=user) if user.is_authenticated else []
    return render(request, "characters.html", {"characters": characters, "guest_mode": guest_mode})


def party_view(request):
    """Display the user's party info or show guest preview."""
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

    return render(request, "party.html", {"parties": parties, "guest_mode": guest_mode})


def contact_view(request):
    """Render the contact page."""
    return render(request, "contact.html")
