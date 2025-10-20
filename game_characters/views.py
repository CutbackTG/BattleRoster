from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character
import random
from django import forms

# ---------- Dice Roller Setup ----------

DICE_CHOICES = [
    (3, 'D3'),
    (4, 'D4'),
    (6, 'D6'),
    (7, 'D7'),
    (8, 'D8'),
    (10, 'D10'),
    (12, 'D12'),
    (20, 'D20'),
]

class DiceRollForm(forms.Form):
    die1 = forms.ChoiceField(choices=DICE_CHOICES, required=False)
    die2 = forms.ChoiceField(choices=DICE_CHOICES, required=False)
    die3 = forms.ChoiceField(choices=DICE_CHOICES, required=False)


# ---------- Main Views ----------

def index_view(request):
    return render(request, "index.html")

# Helper to safely convert numeric fields
def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# List/create/update characters + dice roller
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

    # ---------- Dice Roller Logic ----------
    results = []
    total = None
    dice_form = DiceRollForm(request.POST or None)

    if request.method == "POST" and "roll_dice" in request.POST:
        if dice_form.is_valid():
            dice = [dice_form.cleaned_data.get(f'die{i}') for i in range(1, 4)]
            dice = [int(d) for d in dice if d]
            results = [random.randint(1, d) for d in dice]
            total = sum(results)

    # ---------- Character Save/Update Logic ----------
    elif request.method == "POST":
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

    # ---------- Context for Template ----------
    attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    return render(
        request,
        "characters.html",
        {
            "characters": characters,
            "attributes": attributes,
            "editing": editing,
            "pk": pk,
            "dice_form": dice_form,
            "results": results,
            "total": total,
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


# Party view (show all characters in user's party)
def party_view(request):
    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user).order_by('name')
    else:
        characters = request.session.get("characters", [])

    return render(request, "party.html", {"characters": characters})
