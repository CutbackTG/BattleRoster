from django.shortcuts import render

# Home page view
def home_view(request):
    return render(request, 'index.html')

# Characters page
def characters_view(request):
    return render(request, 'characters.html')

# Party page
def party_view(request):
    return render(request, 'party.html')

# Sign-up / Log-in page
def signup_login_view(request):
    return render(request, 'signup-login.html')

# Contact page
def contact_view(request):
    return render(request, 'contact.html')
