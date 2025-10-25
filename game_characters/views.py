from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Character, Party, PartyCharacter
import random
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

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


# ---------- Party Management ----------
def party_remove_member(request, pk):
    """Allow any party member (including DM) to remove another."""
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

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

    return redirect("party_detail", pk=party.pk)


def party_invite(request, pk):
    """Allow any party member or DM to invite others."""
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

    party = get_object_or_404(Party, pk=pk)

    if request.user not in party.members.all() and request.user != party.dungeon_master:
        messages.error(request, "You must be a member of this party to invite others.")
        return redirect("party_detail", pk=party.pk)

    if request.method == "POST":
        username = request.POST.get("username")
        if not username:
            messages.warning(request, "Please enter a username.")
            return redirect("party_detail", pk=party.pk)

        try:
            invited_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"User '{username}' does not exist.")
            return redirect("party_detail", pk=party.pk)

        if invited_user in party.members.all():
            messages.info(request, f"{invited_user.username} is already in the party.")
        else:
            party.members.add(invited_user)
            messages.success(request, f"{invited_user.username} has been added to the party!")

    return redirect("party_detail", pk=party.pk)


# ---------- Dungeon Master Party List ----------
def dm_party_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

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


# ---------- Character View ----------
def characters_view(request, pk=None):
    """
    Guests can open and try character creation, but must sign up to save or use party features.
    """
    user = request.user
    is_authenticated = user.is_authenticated

    # Handle both boolean field and method
    is_dm_attr = getattr(user, "is_dungeon_master", False)
    is_dm = is_dm_attr() if callable(is_dm_attr) else is_dm_attr

    selected_player_id = request.GET.get("player")

    # Character Query Logic
    if is_authenticated:
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
        characters = []
        players = None

    # Character Editing Logic
    editing = None
    if pk is not None and is_authenticated:
        if is_dm:
            editing = get_object_or_404(Character, pk=pk)
        else:
            editing = get_object_or_404(Character, pk=pk, player=user)

    results, total = [], None
    dice_form = DiceRollForm(request.POST or None)

    if request.method == "POST":
        if not is_authenticated:
            messages.warning(
                request,
                "This feature is available to members only — why not sign up for a free account?"
            )
            return redirect("signup_login")

        if "roll_dice" in request.POST:
            if dice_form.is_valid():
                dice = [dice_form.cleaned_data.get(f"die{i}") for i in range(1, 4)]
                dice = [int(d) for d in dice if d]
                results = [random.randint(1, d) for d in dice]
                total = sum(results)
        else:
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
                if is_dm or editing.player == user:
                    for k, v in fields.items():
                        setattr(editing, k, v)
                    editing.save()
                    messages.success(request, f"Character '{fields['name']}' updated successfully!")
                else:
                    messages.error(request, "You don't have permission to edit this character.")
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


# ---------- Delete Character ----------
def character_delete(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

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
def party_view(request):
    user = request.user

    if not user.is_authenticated:
        messages.warning(
            request,
            "This feature is available to members only — why not sign up for a free account?"
        )
        return redirect("signup_login")

    is_dm = (
        user.is_dungeon_master()
        if callable(getattr(user, "is_dungeon_master", None))
        else getattr(user, "is_dungeon_master", False)
    )

    if is_dm:
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
        member_characters = Character.objects.filter(
            player__in=party.members.all()
        ).order_by("player__username", "name")

        return render(
            request,
            "player_party_view.html",
            {
                "party": party,
                "member_characters": member_characters,
                "selected_pc": selected_pc,
                "is_dm": False,
                "attr_list": [
                    "health", "mana", "strength", "dexterity",
                    "constitution", "intelligence", "wisdom", "charisma",
                ],
            },
        )


def party_select_character(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

    party = get_object_or_404(Party, pk=pk)
    user = request.user

    if not party.members.filter(id=user.id).exists():
        messages.error(request, "You are not a member of this party.")
        return redirect("party_detail", pk=party.pk)

    characters = Character.objects.filter(player=user)
    selected_pc = PartyCharacter.objects.filter(party=party, player=user).first()

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

    return render(
        request,
        "party_select_character.html",
        {"party": party, "characters": characters, "selected_pc": selected_pc},
    )


def party_detail(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "This feature is available to members only — why not sign up for a free account?")
        return redirect("signup_login")

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


# ---------- Contact View ----------
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not name or not email or not message:
            messages.error(request, "Please fill in all fields before submitting.")
            return redirect("contact")

        admin_subject = f"BattleRoster Contact - {name}"
        admin_message = (
            f"📨 New message received via the BattleRoster contact form:\n\n"
            f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )

        user_subject = "Thanks for contacting BattleRoster!"
        user_message = (
            f"Hi {name},\n\n"
            "Thanks for reaching out to the BattleRoster team.\n"
            "We’ve received your message and will get back to you as soon as possible.\n\n"
            "Your Message:\n"
            f"{message}\n\n"
            "— The BattleRoster Team ⚔️"
        )

        try:
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, ["tylerworth.media@gmail.com"], fail_silently=False)
            send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=True)
            messages.success(request, "Your message has been sent successfully! Check your inbox for confirmation.")
        except BadHeaderError:
            messages.error(request, "Invalid header detected. Please try again.")
        except Exception:
            messages.error(request, "Something went wrong while sending your message. Please try again later or email us directly.")

        return redirect("contact")

    return render(request, "contact.html")
