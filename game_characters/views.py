from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character, Party, PartyCharacter
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


# ---------- Helpers ----------
def index_view(request):
    return render(request, "index.html")

def to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ---------- DM Party List ----------
@login_required
def dm_party_list(request):
    """Dungeon Master dashboard for managing parties."""
    user = request.user
    if not getattr(user, "is_dungeon_master", False):
        messages.error(request, "Only Dungeon Masters can manage parties.")
        return redirect("party")

    if request.method == "POST":
        if "create_party" in request.POST:
            name = request.POST.get("party_name")
            if name:
                Party.objects.create(name=name, dungeon_master=user)
                messages.success(request, f"Party '{name}' created successfully!")
                return redirect("dm_party_list")

        elif "delete_party" in request.POST:
            party_id = request.POST.get("party_id")
            party = get_object_or_404(Party, id=party_id, dungeon_master=user)
            messages.warning(request, f"Party '{party.name}' deleted.")
            party.delete()
            return redirect("dm_party_list")

    parties = Party.objects.filter(dungeon_master=user).order_by("name")
    return render(request, "dm_party_dashboard.html", {"parties": parties})


# ---------- Character Views ----------
def characters_view(request, pk=None):
    user = request.user
    is_dm = getattr(user, "is_dungeon_master", False)
    selected_player_id = request.GET.get("player")

    if user.is_authenticated:
        if is_dm:
            if selected_player_id and selected_player_id != "all":
                characters = Character.objects.filter(player__id=selected_player_id).order_by("name")
            else:
                characters = Character.objects.all().order_by("player__username", "name")
            players = User.objects.filter(game_characters__isnull=False).distinct().order_by("username")
        else:
            characters = Character.objects.filter(player=user).order_by("name")
            players = None
    else:
        characters = request.session.get("characters", [])
        players = None

    editing = None
    if pk is not None:
        if user.is_authenticated:
            if is_dm:
                editing = get_object_or_404(Character, pk=pk)
            else:
                editing = get_object_or_404(Character, pk=pk, player=user)
        else:
            if int(pk) < len(characters):
                editing = characters[int(pk)]
            else:
                messages.error(request, "Character not found.")
                return redirect("characters")

    results, total = [], None
    dice_form = DiceRollForm(request.POST or None)

    if request.method == "POST" and "roll_dice" in request.POST:
        if dice_form.is_valid():
            dice = [dice_form.cleaned_data.get(f"die{i}") for i in range(1, 4)]
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
            for k, v in fields.items():
                setattr(editing, k, v)
            editing.save()
            messages.success(request, f"Character '{fields['name']}' updated successfully!")
        else:
            Character.objects.create(player=user, **fields)
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
            "character": editing,
            "pk": pk,
            "dice_form": dice_form,
            "results": results,
            "total": total,
            "is_dm": is_dm,
            "players": players,
            "selected_player_id": selected_player_id,
        },
    )


@login_required
def character_delete(request, pk):
    user = request.user
    is_dm = getattr(user, "is_dungeon_master", False)
    if is_dm:
        character = get_object_or_404(Character, pk=pk)
    else:
        character = get_object_or_404(Character, pk=pk, player=user)

    character.delete()
    messages.success(request, f"Character '{character.name}' deleted successfully!")
    return redirect("characters")


# ---------- Party Views ----------
@login_required
def party_view(request):
    user = request.user

    if getattr(user, "is_dungeon_master", False):
        parties = Party.objects.filter(dungeon_master=user).order_by("name")
        if request.method == "POST":
            if "create_party" in request.POST:
                name = request.POST.get("party_name")
                if name:
                    Party.objects.create(name=name, dungeon_master=user)
                    messages.success(request, f"Party '{name}' created successfully!")
                    return redirect("party")
            elif "delete_party" in request.POST:
                party_id = request.POST.get("party_id")
                party = get_object_or_404(Party, id=party_id, dungeon_master=user)
                messages.warning(request, f"Party '{party.name}' deleted.")
                party.delete()
                return redirect("party")
        return render(request, "dm_party_dashboard.html", {"parties": parties})

    else:
        party = Party.objects.filter(members=user).first()
        if not party:
            messages.info(request, "You are not in a party yet.")
            return render(request, "party.html", {"party": None})

        characters = Character.objects.filter(player=user)
        selected_pc = PartyCharacter.objects.filter(party=party, player=user).first()
        member_characters = Character.objects.filter(player__in=party.members.all()).order_by("player__username", "name")

        context = {
            "party": party,
            "member_characters": member_characters,
            "selected_pc": selected_pc,
            "is_dm": False,
            "attr_list": [
                "health", "mana", "strength", "dexterity",
                "constitution", "intelligence", "wisdom", "charisma",
            ],
        }
        return render(request, "player_party_view.html", context)


@login_required
def party_select_character(request, pk):
    """Allow a player to select which of their characters to use in a party."""
    party = get_object_or_404(Party, pk=pk)
    user = request.user

    if not party.members.filter(id=user.id).exists():
        messages.error(request, "You are not a member of this party.")
        return redirect("party_detail", pk=party.pk)

    characters = Character.objects.filter(player=user)

    if request.method == "POST":
        char_id = request.POST.get("character_id")
        if not char_id:
            messages.error(request, "Please select a character.")
        else:
            character = get_object_or_404(Character, pk=char_id, player=user)
            PartyCharacter.objects.update_or_create(
                party=party, player=user, defaults={"character": character}
            )
            messages.success(request, f"{character.name} selected for {party.name}.")
            return redirect("party_detail", pk=party.pk)

    return render(request, "select_character.html", {"party": party, "characters": characters})


@login_required
def party_detail(request, pk):
    party = get_object_or_404(Party, pk=pk)
    user = request.user

    if user != party.dungeon_master and user not in party.members.all():
        messages.error(request, "You do not have permission to view this party.")
        return redirect("party")

    if user == party.dungeon_master:
        member_characters = Character.objects.filter(player__in=party.members.all()).order_by("player__username", "name")
        return render(
            request,
            "dm_party_characters.html",
            {
                "party": party,
                "member_characters": member_characters,
                "is_dm": True,
                "attr_list": [
                    "health", "mana", "strength", "dexterity",
                    "constitution", "intelligence", "wisdom", "charisma",
                ],
            },
        )

    selected_pc = PartyCharacter.objects.filter(party=party, player=user).first()
    characters = Character.objects.filter(player=user)
    member_characters = Character.objects.filter(player__in=party.members.all())

    return render(
        request,
        "player_party_view.html",
        {
            "party": party,
            "characters": characters,
            "selected_pc": selected_pc,
            "member_characters": member_characters,
            "is_dm": False,
            "attr_list": [
                "health", "mana", "strength", "dexterity",
                "constitution", "intelligence", "wisdom", "charisma",
            ],
        },
    )
