from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character

# Home page
def index_view(request):
    return render(request, "index.html")

# Party page
def party_view(request):
    return render(request, "party.html")

# Helper: safely convert numeric values
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# List/create characters
def characters_view(request):
    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        level = to_int(request.POST.get("level"), 1)
        race = request.POST.get("race", "").strip()
        class_type = request.POST.get("class_type", "").strip()
        health = to_int(request.POST.get("health"), 100)
        mana = to_int(request.POST.get("mana"), 50)
        strength = to_int(request.POST.get("strength"), 10)
        dexterity = to_int(request.POST.get("dexterity"), 10)
        constitution = to_int(request.POST.get("constitution"), 10)
        intelligence = to_int(request.POST.get("intelligence"), 10)
        wisdom = to_int(request.POST.get("wisdom"), 10)
        charisma = to_int(request.POST.get("charisma"), 10)
        equipment = request.POST.get("equipment", "").strip()
        weapons = request.POST.get("weapons", "").strip()
        spells = request.POST.get("spells", "").strip()

        if request.user.is_authenticated:
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
            # Guest: limit to 1 character
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

    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(request, "characters.html", {"characters": characters, "attributes": attributes})


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
        numeric_fields = ["level", "health", "mana", "strength", "dexterity",
                          "constitution", "intelligence", "wisdom", "charisma"]
        string_fields = ["name", "race", "class_type", "equipment", "weapons", "spells"]

        for field in numeric_fields + string_fields:
            value = request.POST.get(field, "").strip()
            if field in numeric_fields:
                value = to_int(value, getattr(character, field, 0) if request.user.is_authenticated else character.get(field, 0))
            if value != "":
                if request.user.is_authenticated:
                    setattr(character, field, value)
                else:
                    character[field] = value

        if request.user.is_authenticated:
            character.save()
        else:
            characters[int(pk)] = character
            request.session["characters"] = characters

        name = character.name if request.user.is_authenticated else character["name"]
        messages.success(request, f"Character '{name}' updated successfully!")
        return redirect("characters")

    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(request, "character_update.html", {"character": character, "pk": pk, "attributes": attributes})



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
