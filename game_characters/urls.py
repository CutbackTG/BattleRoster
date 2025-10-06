from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('characters/', include('game_characters.urls')),
    path('sheets/', include('sheets.urls')),
    # Serve your existing HTML files
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('characters.html', TemplateView.as_view(template_name='characters.html'), name='characters_page'),
    path('contact.html', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('party.html', TemplateView.as_view(template_name='party.html'), name='party'),
    path('signup-login.html', TemplateView.as_view(template_name='signup-login.html'), name='signup_login'),
]