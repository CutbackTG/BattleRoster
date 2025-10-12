from django.urls import path
from . import views

urlpatterns = [
    path('', views.characters_view, name='characters'),
    path('party/', views.party_view, name='party'),
    path('contact/', views.contact_view, name='contact'),
    path('signup-login/', views.signup_login_view, name='signup-login'),
]