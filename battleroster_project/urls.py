from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('game_characters.urls')),  # Home and character-related routes
    path('accounts/', include('accounts.urls')),  # Signup/Login
    path('sheets/', include('sheets.urls')),  # Optional: character sheets app

    # Direct static HTML pages (for pages not handled by app views)
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('characters/', TemplateView.as_view(template_name='characters.html'), name='characters_page'),
    path('party/', TemplateView.as_view(template_name='party.html'), name='party'),
    path('signup-login/', TemplateView.as_view(template_name='signup-login.html'), name='signup_login'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
]
