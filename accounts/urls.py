from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Combined signup + login page
    path('signup-login/', views.signup_login_view, name='signup_login'),

    # Individual routes
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password management (optional)
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done',
    ),
]
