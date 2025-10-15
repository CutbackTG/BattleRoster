from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Character


def index_view(request):
    """Render the homepage."""
    return render(request, "index.html")


def party_view(request):
    """Render the party page."""
    return render(request, "party.html")


@login_required
def characters_view(request):
    """Display user's characters and handle creation."""
    characters = Character.objects.filter(player=request.user).order_by("name")

    if request.method == "POST":
        # Safely convert numeric fields to integers
        def get_int(field_name, default):
            try:
                return int(request.POST.get(field_name, default) or default)
            except ValueError:
                return default

        character = Character.objects.create(
            player=request.user,
            name=request.POST.get("name", "").strip(),
            level=get_int("level", 1),
            race=request.POST.get("race", "").strip(),
            class_type=request.POST.get("class_type", "").strip(),
            health=get_int("health", 100),
            mana=get_int("mana", 50),
            strength=get_int("strength", 10),
            dexterity=get_int("dexterity", 10),
            constitution=get_int("constitution", 10),
            intelligence=get_int("intelligence", 10),
            wisdom=get_int("wisdom", 10),
            charisma=get_int("charisma", 10),
            equipment=request.POST.get("equipment", ""),
            weapons=request.POST.get("weapons", ""),
            spells=request.POST.get("spells", ""),
        )

        messages.success(request, f"Character '{character.name}' created successfully!")
        return redirect("characters")

    return render(request, "characters.html", {"characters": characters})


@login_required
def character_update(request, pk):
    """Edit an existing character."""
    character = get_object_or_404(Character, pk=pk, player=request.user)

    if request.method == "POST":
        def get_int(field_name, default):
            try:
                return int(request.POST.get(field_name, default) or default)
            except ValueError:
                return default

        character.name = request.POST.get("name", "").strip()
        character.level = get_int("level", 1)
        character.race = request.POST.get("race", "").strip()
        character.class_type = request.POST.get("class_type", "").strip()
        character.health = get_int("health", 100)
        character.mana = get_int("mana", 50)
        character.strength = get_int("strength", 10)
        character.dexterity = get_int("dexterity", 10)
        character.constitution = get_int("constitution", 10)
        character.intelligence = get_int("intelligence", 10)
        character.wisdom = get_int("wisdom", 10)
        character.charisma = get_int("charisma", 10)
        character.equipment = request.POST.get("equipment", "")
        character.weapons = request.POST.get("weapons", "")
        character.spells = request.POST.get("spells", "")
        character.save()

        messages.success(request, f"Character '{character.name}' updated successfully!")
        return redirect("characters")

    return render(request, "character_edit.html", {"character": character})


@login_required
def character_delete(request, pk):
    """Delete a character."""
    character = get_object_or_404(Character, pk=pk, player=request.user)
    character.delete()
    messages.success(request, f"Character '{character.name}' deleted successfully!")
    return redirect("characters")
