from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character, Party
import random
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

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

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def characters_view(request, pk=None):
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

    results = []
    total = None
    dice_form = DiceRollForm(request.POST or None)

    if request.method == "POST" and "roll_dice" in request.POST:
        if dice_form.is_valid():
            dice = [dice_form.cleaned_data.get(f'die{i}') for i in range(1, 4)]
            dice = [int(d) for d in dice if d]
            results = [random.randint(1, d) for d in dice]
            total = sum(results)

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

        if editing:
            if request.user.is_authenticated:
                for k, v in fields.items():
                    setattr(editing, k, v)
                editing.save()
            else:
                characters[int(pk)] = fields
                request.session["characters"] = characters
            messages.success(request, f"Character '{fields['name']}' updated successfully!")
        else:
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
        },
    )

# ---------- Party Views ----------

@login_required
def party_view(request):
    """Show player's party or DM dashboard."""
    user = request.user

    # 🔸 If Dungeon Master, show DM dashboard
    if hasattr(user, "is_dungeon_master") and user.is_dungeon_master:
        parties = Party.objects.filter(dungeon_master=user).order_by("name")

        if request.method == "POST" and "create_party" in request.POST:
            name = request.POST.get("party_name")
            if name:
                Party.objects.create(name=name, dungeon_master=user)
                messages.success(request, f"Party '{name}' created successfully!")
                return redirect("party")

        if request.method == "POST" and "delete_party" in request.POST:
            party_id = request.POST.get("party_id")
            party = get_object_or_404(Party, id=party_id, dungeon_master=user)
            messages.warning(request, f"Party '{party.name}' deleted.")
            party.delete()
            return redirect("party")

        return render(request, "dm_party_dashboard.html", {"parties": parties})

    # 🔸 Otherwise, regular player
    party = Party.objects.filter(members=user).first()
    characters = Character.objects.filter(player=user)

    return render(request, "party.html", {
        "party": party,
        "characters": characters,
    })

@login_required
def party_remove_member(request, pk):
    """Allow any party member (including DM) to remove another."""
    party = get_object_or_404(Party, pk=pk)

    if request.user not in party.members.all() and request.user != party.dungeon_master:
        messages.error(request, "You must be a member of this party to make changes.")
        return redirect("party")

    if request.method == "POST":
        member_id = request.POST.get("member_id")
        member_to_remove = party.members.filter(id=member_id).first()
        if not member_to_remove:
            messages.warning(request, "That member was not found in this party.")
        elif member_to_remove == request.user:
            messages.warning(request, "You cannot remove yourself.")
        else:
            party.members.remove(member_to_remove)
            messages.success(request, f"{member_to_remove.username} has been removed from the party.")

    return redirect("party")

@login_required
def party_invite(request, pk):
    """Allow any party member or DM to invite others."""
    party = get_object_or_404(Party, pk=pk)

    if request.user not in party.members.all() and request.user != party.dungeon_master:
        messages.error(request, "You must be a member of this party to invite others.")
        return redirect("party")

    if request.method == "POST":
        username = request.POST.get("username")
        if not username:
            messages.warning(request, "Please enter a username.")
            return redirect("party")

        try:
            invited_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect("party")

        if invited_user in party.members.all():
            messages.info(request, f"{invited_user.username} is already in the party.")
        else:
            party.members.add(invited_user)
            messages.success(request, f"{invited_user.username} has been added to the party!")

    return redirect("party")
