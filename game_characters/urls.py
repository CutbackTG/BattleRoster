from django.urls import path
from . import views

urlpatterns = [
    # List & create characters
    path("", views.characters_view, name="characters"),

    # Edit a character
    path("edit/<int:pk>/", views.character_update, name="character_update"),

    # Delete a character
    path("delete/<int:pk>/", views.character_delete, name="character_delete"),

    # Party page
    path("party/", views.party_view, name="party"),
]
