from django.urls import path
from . import views

urlpatterns = [
    path("", views.characters_view, name="characters"),
    path("edit/<int:pk>/", views.character_update, name="character_update"),
    path("delete/<int:pk>/", views.character_delete, name="character_delete"),
    path("party/", views.party_view, name="party"),
]
