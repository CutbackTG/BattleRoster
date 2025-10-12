from django.urls import path
from . import views

urlpatterns = [
    path('', views.characters_view, name='characters'),
    path('party/', views.party_view, name='party'),
    path('party/player/', views.party_player_view, name='party-player'),
    path('party/dm/', views.party_dm_view, name='party-dm'),
    path('contact/', views.contact_view, name='contact'),
]
