from django.urls import path
from .views import signup_login_view, logout_view

urlpatterns = [
    path("signup_login/", signup_login_view, name="signup_login"),
    path("logout/", logout_view, name="logout"),
]
