from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Include your game_characters app URLs
    path('', include('game_characters.urls')),  # Home and main app views

    # Include account management app URLs
    path('accounts/', include('accounts.urls')),

    # Optional: sheets app
    path('sheets/', include('sheets.urls')),

    # Serve static HTML templates safely (no namespace issues)
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact_page'),
    path('signup-login/', TemplateView.as_view(template_name='signup-login.html'), name='signup_login_page'),
]
