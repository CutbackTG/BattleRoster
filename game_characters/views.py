from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character

# Home page
def index_view(request):
    return render(request, "index.html")

# Party page
def party_view(request):
    return render(request, "party.html")

# List/create characters
def characters_view(request):
    # Determine current characters
    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    if request.method == "POST":
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

        if request.user.is_authenticated:
            # Authenticated users can create freely
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
        else:
            # Anonymous users: only allow one character
            if len(characters) >= 1:
                messages.info(request, "Please sign up or log in to create additional characters.")
                return redirect("/accounts/signup_login/?next=/characters/")

            temp_char = {
                "name": name,
                "level": level,
                "race": race,
                "class_type": class_type,
                "health": health,
                "mana": mana,
                "strength": strength,
                "dexterity": dexterity,
                "constitution": constitution,
                "intelligence": intelligence,
                "wisdom": wisdom,
                "charisma": charisma,
                "equipment": equipment,
                "weapons": weapons,
                "spells": spells,
            }
            characters.append(temp_char)
            request.session["characters"] = characters

        messages.success(request, f"Character '{name}' created successfully!")
        return redirect("characters")

    return render(request, "characters.html", {"characters": characters})

# Update a character
def character_update(request, pk):
    if request.user.is_authenticated:
        character = get_object_or_404(Character, pk=pk, player=request.user)
    else:
        characters = request.session.get("characters", [])
        if int(pk) >= len(characters):
            messages.error(request, "Character not found.")
            return redirect("characters")
        character = characters[int(pk)]

    if request.method == "POST":
        fields = ["name", "level", "race", "class_type", "health", "mana",
                  "strength", "dexterity", "constitution", "intelligence",
                  "wisdom", "charisma", "equipment", "weapons", "spells"]
        for field in fields:
            value = request.POST.get(field)
            if value:
                if request.user.is_authenticated:
                    setattr(character, field, value)
                else:
                    character[field] = value

        if request.user.is_authenticated:
            character.save()
        else:
            characters[int(pk)] = character
            request.session["characters"] = characters

        messages.success(request, f"Character '{character['name'] if not request.user.is_authenticated else character.name}' updated successfully!")
        return redirect("characters")

    return render(request, "character_update.html", {"character": character, "pk": pk})

# Delete a character
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
