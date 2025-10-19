from django.urls import path
from . import views

app_name = 'game_characters'

urlpatterns = [
    # List and create characters
    path('', views.characters_view, name='characters'),

    # Edit an existing character (characters_view handles editing when pk is provided)
    path('edit/<int:pk>/', views.characters_view, name='character_update'),

    # Delete a character
    path('delete/<int:pk>/', views.character_delete, name='character_delete'),
]
