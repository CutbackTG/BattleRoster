from django.urls import path
from . import views

urlpatterns = [
    path("", views.characters_view, name="characters"),  # main /characters/
    path("party/", views.party_view, name="party"),
    path("contact/", views.contact_view, name="contact"),
    path("characters/update/<int:row_number>/", views.update_character, name="update_character"),
    path("characters/delete/<int:row_number>/", views.delete_character, name="delete_character"),
]
