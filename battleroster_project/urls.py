from django.contrib import admin
from django.urls import path, include
from game_characters import views as game_views
from sheets import views as sheets_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Homepage
    path('', game_views.index_view, name='home'),

    # Characters app URLs (includes characters, edit, delete, party)
    path('characters/', include('game_characters.urls')),

    # Accounts URLs (signup/login/logout)
    path('accounts/', include('accounts.urls')),

    #Party page
    path('party/', game_views.party_view, name='party'),
    
    # Contact page
    path('contact/', sheets_views.contact_view, name='contact'),

]
