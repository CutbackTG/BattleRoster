from django.contrib import admin
from django.urls import path, include
from game_characters import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('characters/', include('game_characters.urls')),
]