from django.urls import path
from . import views

urlpatterns = [
    path("signup_login/", views.signup_login_view, name="signup_login"),  # ✅ use hyphen
    path("logout/", views.logout_view, name="logout"),
]
