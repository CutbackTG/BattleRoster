from django.contrib import admin
from django.urls import path, include
from game_characters import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('characters/', include('game_characters.urls')),
    path('accounts/', include('accounts.urls')),
]
