from django.urls import path
from . import views

urlpatterns = [
    path('', views.characters_view, name='characters'),
    path('add/', views.add_character, name='add_character'),
    path('edit/<int:character_id>/', views.edit_character, name='edit_character'),
    path('delete/<int:character_id>/', views.delete_character, name='delete_character'),

    path('party/', views.party_view, name='party'),
    path('contact/', views.contact_view, name='contact'),
]
