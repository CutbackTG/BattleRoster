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
    characters = Character.objects.filter(player=request.user).order_by('name')

    if request.method == "POST":
        # Create new character
        name = request.POST.get("name")
        level = request.POST.get("level") or 1
        race = request.POST.get("race")
        class_type = request.POST.get("class_type")
        health = request.POST.get("health") or 100
        mana = request.POST.get("mana") or 50
        strength = request.POST.get("strength") or 10
        dexterity = request.POST.get("dexterity") or 10
        constitution = request.POST.get("constitution") or 10
        intelligence = request.POST.get("intelligence") or 10
        wisdom = request.POST.get("wisdom") or 10
        charisma = request.POST.get("charisma") or 10
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
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            wisdom=wisdom,
            charisma=charisma,
            equipment=equipment,
            weapons=weapons,
            spells=spells,
        )
        messages.success(request, f"Character '{name}' created successfully!")
        return redirect("characters")

    return render(request, "characters.html", {"characters": characters})
    

@login_required
def character_update(request, pk):
    """Edit an existing character."""
    character = get_object_or_404(Character, pk=pk, player=request.user)

    if request.method == "POST":
        character.name = request.POST.get("name")
        character.level = request.POST.get("level") or 1
        character.race = request.POST.get("race")
        character.class_type = request.POST.get("class_type")
        character.health = request.POST.get("health") or 100
        character.mana = request.POST.get("mana") or 50
        character.strength = request.POST.get("strength") or 10
        character.dexterity = request.POST.get("dexterity") or 10
        character.constitution = request.POST.get("constitution") or 10
        character.intelligence = request.POST.get("intelligence") or 10
        character.wisdom = request.POST.get("wisdom") or 10
        character.charisma = request.POST.get("charisma") or 10
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
