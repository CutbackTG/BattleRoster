from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Character, Party

def home_view(request):
    return render(request, 'index.html')


def characters_view(request):
    """
    Allows guests to create ONE character (stored in session).
    Logged-in users can create unlimited characters tied to their account.
    """
    characters = []
    
    # If user is logged in, load their characters from DB
    if request.user.is_authenticated:
        characters = Character.objects.filter(player=request.user)
    else:
        # For guests, load characters stored in session
        characters = request.session.get("guest_characters", [])

    # Handle form submissions
    if request.method == "POST":
        name = request.POST.get("name")
        char_class = request.POST.get("class")
        level = request.POST.get("level")

        # Guest logic
        if not request.user.is_authenticated:
            guest_characters = request.session.get("guest_characters", [])
            if len(guest_characters) >= 1:
                # Too many guest characters – trigger modal
                messages.error(request, "Creating more than one character requires an account.")
                return redirect("characters")
            
            # Add guest character to session
            new_character = {"name": name, "char_class": char_class, "level": level}
            guest_characters.append(new_character)
            request.session["guest_characters"] = guest_characters
            request.session.modified = True

            messages.success(request, f"Temporary character '{name}' created!")
            return redirect("characters")

        # Logged-in user logic
        else:
            Character.objects.create(
                name=name,
                char_class=char_class,
                level=level,
                player=request.user
            )
            messages.success(request, f"Character '{name}' created successfully!")
            return redirect("characters")

    return render(request, "characters.html", {"characters": characters})


@login_required
def party_view(request):
    """
    Shows the party for the logged-in user (Player or Dungeon Master).
    """
    user = request.user
    parties = Party.objects.filter(dungeon_master=user) if user.role == "dungeon_master" else Party.objects.filter(members=user)
    return render(request, "party.html", {"parties": parties})


def contact_view(request):
    return render(request, "contact.html")

@login_required
def party_player_view(request):
    """
    View for regular players to see their party and characters.
    """
    user = request.user
    parties = Party.objects.filter(members=user)
    return render(request, 'party_player.html', {'parties': parties})


@login_required
def party_dm_view(request):
    """
    View for Dungeon Masters to manage their party members.
    """
    user = request.user
    parties = Party.objects.filter(dungeon_master=user)
    return render(request, 'party_dm.html', {'parties': parties})
