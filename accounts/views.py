from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character

def index_view(request):
    return render(request, "index.html")

# Helper to safely convert numeric values
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def characters_view(request, pk=None):
    """
    List characters, create new ones, or edit existing ones.
    If pk is provided, we're editing that character.
    """
    editing = None

    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    # If pk is provided, fetch the character for editing
    if pk is not None:
        if request.user.is_authenticated:
            editing = get_object_or_404(Character, pk=pk, player=request.user)
        else:
            if int(pk) >= len(characters):
                messages.error(request, "Character not found.")
                return redirect("characters")
            editing = characters[int(pk)]

    if request.method == "POST":
        # Collect form data
        numeric_fields = ["level", "health", "mana", "strength", "dexterity",
                          "constitution", "intelligence", "wisdom", "charisma"]
        string_fields = ["name", "race", "class_type", "equipment", "weapons", "spells"]

        data = {}
        for field in numeric_fields:
            data[field] = to_int(request.POST.get(field, ""), getattr(editing, field, 0) if editing and request.user.is_authenticated else 0)
        for field in string_fields:
            data[field] = request.POST.get(field, "").strip()

        if editing:  # Update existing character
            if request.user.is_authenticated:
                for key, value in data.items():
                    setattr(editing, key, value)
                editing.save()
            else:
                characters[int(pk)].update(data)
                request.session["characters"] = characters
            messages.success(request, f"Character '{data['name']}' updated successfully!")
        else:  # Create new character
            if request.user.is_authenticated:
                Character.objects.create(player=request.user, **data)
            else:
                # Limit guest users to 1 character
                if len(characters) >= 1:
                    messages.info(request, "Please sign up or log in to create additional characters.")
                    return redirect("/accounts/signup_login/?next=/characters/")
                characters.append(data)
                request.session["characters"] = characters
            messages.success(request, f"Character '{data['name']}' created successfully!")

        return redirect("characters")

    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(request, "characters.html", {
        "characters": characters,
        "attributes": attributes,
        "editing": editing,
        "pk": pk
    })

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
