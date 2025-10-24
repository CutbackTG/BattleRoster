from django.urls import path
from .views import characters_view, character_delete
from . import views

urlpatterns = [
    path('', characters_view, name='characters'),                 # list / create
    path('<int:pk>/', characters_view, name='characters_edit'),   # edit
    path('<int:pk>/delete/', character_delete, name='character_delete'),  # delete
    path("party/<int:pk>/", views.party_detail, name="party_detail"),
    path("party/<int:pk>/invite/", views.party_invite, name="party_invite"),
    # path("party/invite/accept/<str:token>/", views.party_invite_accept, name="party_invite_accept"),
    # path("party/invite/decline/<str:token>/", views.party_invite_decline, name="party_invite_decline"),
    path("party/<int:pk>/remove-member/", views.party_remove_member, name="party_remove_member"),
    path("party/<int:pk>/select-character/", views.party_select_character, name="party_select_character"),
]
