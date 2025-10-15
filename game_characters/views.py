from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Character

def index_view(request):
    return render(request, "index.html")

@login_required
def character_update(request, pk):
    attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
    character = get_object_or_404(Character, pk=pk, player=request.user)

    if request.method == "POST":
        character.name = request.POST.get("name")
        character.level = request.POST.get("level") or 1
        character.race = request.POST.get("race")
        character.class_type = request.POST.get("class_type")
        character.health = request.POST.get("health") or 100
        character.mana = request.POST.get("mana") or 50

        # Update attributes dynamically
        for attr in attributes:
            setattr(character, attr.lower(), int(request.POST.get(attr.lower(), 10)))

        character.equipment = request.POST.get("equipment", "")
        character.weapons = request.POST.get("weapons", "")
        character.spells = request.POST.get("spells", "")
        character.save()
        messages.success(request, f"Character '{character.name}' updated successfully!")
        return redirect("characters")

    return render(request, "character_edit.html", {"character": character, "attributes": attributes})

@login_required
def character_delete(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    character.delete()
    messages.success(request, f"Character '{character.name}' deleted successfully!")
    return redirect("characters")
