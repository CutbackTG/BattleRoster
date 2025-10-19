from django.urls import path
from .views import signup_login_view, logout_view
from game_characters import views as game_views

urlpatterns = [
    path("signup_login/", signup_login_view, name="signup_login"),
    path("logout/", logout_view, name="logout"),
    path('party/', game_views.party_view, name='party'),
]