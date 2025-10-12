from django.shortcuts import render

# --- Core Page Views ---

def home_view(request):
    return render(request, 'index.html')

def characters_view(request):
    return render(request, 'characters.html')

def party_view(request):
    return render(request, 'party.html')

def signup_login_view(request):
    return render(request, 'signup-login.html')

def contact_view(request):
    return render(request, 'contact.html')


# --- Character Management (placeholders for now) ---

def character_list(request):
    """Display all characters."""
    return render(request, 'characters.html')

def character_create(request):
    """Create a new character (placeholder)."""
    return render(request, 'characters.html')

def character_detail(request, character_id=None):
    """Display details for a specific character."""
    return render(request, 'characters.html')
