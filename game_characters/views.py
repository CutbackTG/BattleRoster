from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Character, Party

# ----------------------------------------
# Homepage
# ----------------------------------------
def home_view(request):
    return render(request, 'index.html')


# ----------------------------------------
# Characters page
# ----------------------------------------
@login_required
def characters_view(request):
    """Display all characters for the current user."""
    characters = Character.objects.filter(player=request.user)
    return render(request, 'characters.html', {'characters': characters})


# ----------------------------------------
# Contact page
# ----------------------------------------
def contact_view(request):
    return render(request, 'contact.html')


# ----------------------------------------
# Party redirector — sends user to correct view
# ----------------------------------------
@login_required
def party_view(request):
    """Redirect the user to their role-specific party page."""
    user = request.user
    if hasattr(user, 'role') and user.role == 'dungeon_master':
        return redirect('party-dm')
    else:
        return redirect('party-player')


# ----------------------------------------
# Player Party Page
# ----------------------------------------
@login_required
def party_player_view(request):
    """
    Show the player's current party and allow them to manage or request to join.
    """
    try:
        party = Party.objects.get(members=request.user)
    except Party.DoesNotExist:
        party = None

    context = {
        'party': party,
        'is_dungeon_master': hasattr(request.user, 'role') and request.user.role == 'dungeon_master'
    }
    return render(request, 'party_player.html', context)


# ----------------------------------------
# Dungeon Master Party Page
# ----------------------------------------
@login_required
def party_dm_view(request):
    """
    Show the Dungeon Master's controlled party and allow CRUD operations on members.
    """
    if not hasattr(request.user, 'role') or request.user.role != 'dungeon_master':
        messages.error(request, "You must be a Dungeon Master to access this page.")
        return redirect('party-player')

    parties = Party.objects.filter(dungeon_master=request.user)
    context = {
        'parties': parties,
        'is_dungeon_master': True
    }
    return render(request, 'party_dm.html', context)
