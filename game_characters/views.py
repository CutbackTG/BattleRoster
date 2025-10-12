from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Party, Character


def home_view(request):
    """Landing page view."""
    return render(request, 'index.html')


@login_required
def characters_view(request):
    """Display a list of all characters belonging to the logged-in user."""
    characters = Character.objects.filter(owner=request.user)
    return render(request, 'characters.html', {"characters": characters})


@login_required
def party_view(request):
    """Display and manage the user's party information."""
    user = request.user

    # Determine if user is DM or player
    if hasattr(user, "role") and user.role == "dungeon_master":
        parties = Party.objects.filter(dungeon_master=user)
        is_dm = True
    else:
        parties = Party.objects.filter(members=user)
        is_dm = False

    # Handle POST actions
    if request.method == "POST":
        action = request.POST.get("action")

        # 🎲 Create new party (for DMs)
        if action == "create_party" and is_dm:
            name = request.POST.get("name")
            campaign_name = request.POST.get("campaign_name")

            if not name or not campaign_name:
                messages.error(request, "Both party name and campaign name are required.")
            else:
                party = Party.objects.create(
                    name=name,
                    campaign_name=campaign_name,
                    dungeon_master=user
                )
                messages.success(request, f"Party '{party.name}' created successfully!")
            return redirect("party")

        # 🧍 Add or remove members (for DMs)
        elif action in ["add", "remove"] and is_dm:
            party_id = request.POST.get("party_id")
            username = request.POST.get("username")

            try:
                party = Party.objects.get(id=party_id, dungeon_master=user)
            except Party.DoesNotExist:
                messages.error(request, "Party not found or you are not the Dungeon Master.")
                return redirect("party")

            try:
                target_user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, f"User '{username}' does not exist.")
                return redirect("party")

            if action == "add":
                if target_user in party.members.all():
                    messages.warning(request, f"{username} is already a member of {party.name}.")
                else:
                    party.members.add(target_user)
                    messages.success(request, f"{username} added to {party.name}.")
            elif action == "remove":
                if target_user not in party.members.all():
                    messages.warning(request, f"{username} is not in this party.")
                else:
                    party.members.remove(target_user)
                    messages.success(request, f"{username} removed from {party.name}.")
            return redirect("party")

        else:
            messages.error(request, "Invalid action or insufficient permissions.")
            return redirect("party")

    # Render the party management page
    return render(request, "party.html", {
        "parties": parties,
        "is_dm": is_dm,
    })
