from django.urls import path
from .views import characters_view, character_delete
from . import views

urlpatterns = [
    # Character management
    path('', views.characters_view, name='characters'),
    path('<int:pk>/', views.characters_view, name='characters_edit'),
    path('<int:pk>/delete/', views.character_delete, name='character_delete'),

    # Party system
    path('party/', views.party_view, name='party'),
    path('party/<int:pk>/', views.party_detail, name='party_detail'),
    path('party/<int:pk>/invite/', views.party_invite, name='party_invite'),
    path('party/<int:pk>/remove-member/', views.party_remove_member, name='party_remove_member'),
    path('party/<int:pk>/select-character/', views.party_select_character, name='party_select_character'),

    # Dungeon Master dashboard
    path('dm/parties/', views.dm_party_list, name='dm_party_list'),
]
