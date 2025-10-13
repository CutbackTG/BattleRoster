from django.urls import path
from . import views

urlpatterns = [
    path("", views.characters_view, name="characters"),
    path("update/<int:character_id>/", views.update_character, name="update_character"),
    path("delete/<int:character_id>/", views.delete_character, name="delete_character"),
    path("party/", views.party_view, name="party"),
    path("contact/", views.contact_view, name="contact"),
]
