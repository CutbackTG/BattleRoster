from django.urls import path
from . import views

urlpatterns = [
    # List and create characters
    path('', views.characters_view, name='characters'),

    # Edit a character
    path('edit/<int:pk>/', views.characters_view, name='character_update'),

    # Delete a character
    path('delete/<int:pk>/', views.character_delete, name='character_delete'),
]
