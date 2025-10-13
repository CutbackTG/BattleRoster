from django.urls import path
from . import views

urlpatterns = [
    # Home and main character management
    path('', views.characters_view, name='characters'),

    # Party management
    path('party/', views.party_view, name='party'),

    # Contact page
    path('contact/', views.contact_view, name='contact'),

    # Character actions
    path('characters/update/<int:row_number>/', views.update_character, name='update_character'),
    path('characters/delete/<int:row_number>/', views.delete_character, name='delete_character'),
]
