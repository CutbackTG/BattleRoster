from django.urls import path
from . import views

app_name = 'game_characters'  # Optional, useful for namespacing reverses

urlpatterns = [
    path('', views.home_view, name='home'),            # Home page
    path('characters/', views.characters_view, name='characters'),
    path('party/', views.party_view, name='party'),
    path('signup-login/', views.signup_login_view, name='signup_login'),
    path('contact/', views.contact_view, name='contact'),
]
