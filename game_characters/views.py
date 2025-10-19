from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character

def index_view(request):
    return render(request, "index.html")

# Helper to safely convert numeric fields
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

# List/create/update characters
def characters_view(request, pk=None):
    # Get user characters or session characters
    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    editing = None
    if pk is not None:
        if request.user.is_authenticated:
            editing = get_object_or_404(Character, pk=pk, player=request.user)
        else:
            if int(pk) < len(characters):
                editing = characters[int(pk)]
            else:
                messages.error(request, "Character not found.")
                return redirect("characters")

    if request.method == "POST":
        fields = {
            "name": request.POST.get("name", "").strip(),
            "level": to_int(request.POST.get("level"), 1),
            "race": request.POST.get("race", "").strip(),
            "class_type": request.POST.get("class_type", "").strip(),
            "health": to_int(request.POST.get("health"), 100),
            "mana": to_int(request.POST.get("mana"), 50),
            "strength": to_int(request.POST.get("strength"), 10),
            "dexterity": to_int(request.POST.get("dexterity"), 10),
            "constitution": to_int(request.POST.get("constitution"), 10),
            "intelligence": to_int(request.POST.get("intelligence"), 10),
            "wisdom": to_int(request.POST.get("wisdom"), 10),
            "charisma": to_int(request.POST.get("charisma"), 10),
            "equipment": request.POST.get("equipment", "").strip(),
            "weapons": request.POST.get("weapons", "").strip(),
            "spells": request.POST.get("spells", "").strip(),
        }

        if editing:  # Update existing character
            if request.user.is_authenticated:
                for k, v in fields.items():
                    setattr(editing, k, v)
                editing.save()
            else:
                characters[int(pk)] = fields
                request.session["characters"] = characters
            messages.success(request, f"Character '{fields['name']}' updated successfully!")
        else:  # Create new character
            if request.user.is_authenticated:
                Character.objects.create(player=request.user, **fields)
                messages.success(request, f"Character '{fields['name']}' created successfully!")
            else:
                if len(characters) >= 1:
                    messages.info(request, "Sign up or log in to create more characters.")
                    return redirect("/accounts/signup_login/?next=/characters/")
                characters.append(fields)
                request.session["characters"] = characters
                messages.success(request, f"Character '{fields['name']}' created successfully!")

        return redirect("characters")

    # List of attributes for template
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(
        request,
        "characters.html",
        {
            "characters": characters,
            "attributes": attributes,
            "editing": editing,
            "pk": pk,
        }
    )

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

# New: party_view to show all characters in a party
def party_view(request):
    if request.user.is_authenticated:
        party_characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        party_characters = request.session.get("characters", [])

    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

    return render(
        request,
        "party.html",
        {
            "party_characters": party_characters,
            "attributes": attributes,
        }
    )
