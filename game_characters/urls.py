from django.urls import path
from . import views

urlpatterns = [
    # ✅ Character pages (expand as needed)
    path('list/', views.characters_view, name='character_list'),
    path('create/', views.character_create, name='character_create'),  # Add a new character
    path('<int:pk>/', views.character_detail, name='character_detail'),# View one character
    path('<int:pk>/edit/', views.character_edit, name='character_edit'), # Edit a character
    path('<int:pk>/delete/', views.character_delete, name='character_delete'), # Delete a character
]
