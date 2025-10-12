from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Sign-up
    path('signup/', views.signup_view, name='signup'),

    # Login / Logout using Django’s built-in views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # For your navbar link (temporary combined route)
    path('signup-login/', views.signup_login_redirect, name='signup-login'),
]
