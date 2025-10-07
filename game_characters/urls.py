from django.urls import path
from . import views as game_views

urlpatterns = [
    path('', game_views.home_view, name='home'),  # Home page
    path('characters/', game_views.characters_view, name='characters'),
    path('party/', game_views.party_view, name='party'),
    path('signup-login/', game_views.signup_login_view, name='signup_login'),
    path('contact/', game_views.contact_view, name='contact'),
]
