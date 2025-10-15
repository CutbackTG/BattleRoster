from django.contrib import admin
from django.urls import path, include
from game_characters import views as game_views  # import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', game_views.index_view, name='home'),  # homepage
    path('accounts/', include('accounts.urls')),
    path('characters/', game_views.characters_view, name='characters'),
    path('party/', game_views.party_view, name='party'), 
]
