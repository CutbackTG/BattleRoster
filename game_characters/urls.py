from django.urls import path
from .views import characters_view, character_delete

urlpatterns = [
    path('', characters_view, name='characters'),                 # list / create
    path('<int:pk>/', characters_view, name='characters_edit'),   # edit
    path('<int:pk>/delete/', character_delete, name='character_delete'),  # delete
]
