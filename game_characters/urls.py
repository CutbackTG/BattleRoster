from django.urls import path
from . import views

urlpatterns = [
    # Character Views
    path("", views.characters_view, name="characters"),
    path("<int:pk>/", views.characters_view, name="character_edit"),
    path("delete/<int:pk>/", views.character_delete, name="character_delete"),

    # Party Views
    path("party/", views.party_view, name="party"),
    path("party/<int:pk>/", views.party_detail, name="party_detail"),
    path("party/<int:pk>/remove/", views.party_remove_member, name="party_remove_member"),
    path("party/<int:pk>/invite/", views.party_invite, name="party_invite"),
    path("party/<int:pk>/select/", views.party_select_character, name="party_select_character"),

    # Dungeon Master Dashboard
    path("dm/parties/", views.dm_party_list, name="dm_party_list"),

    # contact email
    path("contact/", views.contact_view, name="contact"),
]
