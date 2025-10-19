from django.urls import path
from . import views

urlpatterns = [
    path('', views.characters_view, name='characters'),
    path('<int:pk>/', views.characters_view, name='edit_character'),
    path('delete/<int:pk>/', views.character_delete, name='delete_character'),
    path('party/', views.party_view, name='party'),
]
