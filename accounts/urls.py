from django.urls import path
from . import views

urlpatterns = [
    # Combined signup + login
    path('signup-login/', views.signup_login_view, name='signup_login'),

    # Logout route
    path('logout/', views.logout_view, name='logout'),
]
