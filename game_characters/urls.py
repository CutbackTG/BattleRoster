from django.urls import path
from . import views

urlpatterns = [
    # Characters listing (default for /characters/)
    path('', views.characters_view, name='characters'),
    # Party management (for DMs and players)
    path('party/', views.party_view, name='party'),
    path('contact/', views.contact_view, name='contact'),
]
