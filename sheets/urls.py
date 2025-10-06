from django.urls import path
from . import views

urlpatterns = [
    path('api/characters/', views.characters_api, name='characters_api'),
]
# project urls.py
from django.urls import include, path

urlpatterns = [
    # ... other routes
    path('', include('sheets.urls')),
]
