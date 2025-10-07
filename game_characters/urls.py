from django.contrib import admin
from django.urls import path, include
from game_characters import views as game_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # your accounts app
    path('', game_views.home_view, name='home'),  # home page
    path('characters/', game_views.characters_view, name='characters'),
    path('party/', game_views.party_view, name='party'),
    path('signup-login/', game_views.signup_login_view, name='signup-login'),
    path('contact/', game_views.contact_view, name='contact'),
]
