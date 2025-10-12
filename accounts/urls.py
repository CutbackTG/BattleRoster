from django.urls import path
from . import views

urlpatterns = [
    path('signup-login/', views.signup_login_view, name='signup-login'),
    path('logout/', views.logout_view, name='logout'),
]
