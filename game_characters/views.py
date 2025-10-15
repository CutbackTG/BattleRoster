from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Character

def index_view(request):
    """Render the homepage."""
    return render(request, "index.html")

def party_view(request):
    return render(request, 'party.html')

@login_required
def characters_view(request):
    """Display user's characters and handle creation."""

    # Define the attributes list to pass to the template
    attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    characters = Character.objects.filter(player=request.user).order_by('name')

    if request.method == "POST":
        # Create new character
        name = request.POST.get("name")
        level = request.POST.get("level") or 1
        race = request.POST.get("race")
        class_type = request.POST.get("class_type")
        health = request.POST.get("health") or 100
        mana = request.POST.get("mana") or 50

        # Grab attribute values dynamically from POST
        attr_values = {attr.lower(): int(request.POST.get(attr.lower(), 10)) for attr in attributes}

        equipment = request.POST.get("equipment", "")
        weapons = request.POST.get("weapons", "")
        spells = request.POST.get("spells", "")

        Character.objects.create(
            player=request.user,
            name=name,
            level=level,
            race=race,
            class_type=class_type,
            health=health,
            mana=mana,
            **attr_values,  # unpack Strength/Dexterity/etc.
            equipment=equipment,
            weapons=weapons,
            spells=spells,
        )
        messages.success(request, f"Character '{name}' created successfully!")
        return redirect("characters")

    return render(request, "characters.html", {"characters": characters, "attributes": attributes})
