from django.urls import path
from . import views

urlpatterns = [
    path("", views.signup_login_view, name="signup_login"),  # Sign-up / Login page
    path("logout/", views.logout_view, name="logout"),       # Logout
]
