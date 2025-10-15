from django.contrib import admin
from django.urls import path
from game_characters import views as game_views
from sheets import views as sheets_views  # for contact form

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', game_views.index_view, name='home'),

    # Character pages
    path('characters/', game_views.characters_view, name='characters'),
    path('characters/edit/<int:pk>/', game_views.character_update, name='character_update'),
    path('characters/delete/<int:pk>/', game_views.character_delete, name='character_delete'),

    # Contact page
    path('contact/', sheets_views.contact_view, name='contact'),
]
