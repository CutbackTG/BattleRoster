from django.urls import path
from . import views

urlpatterns = [
    # Character pages (expand as needed)
    path('list/', views.characters_view, name='character_list'),
]
