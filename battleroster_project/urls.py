from django.contrib import admin
from django.urls import path, include
from game_characters import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('characters/', views.characters_view, name='characters'),
    path('party/', views.party_view, name='party'),
    path('accounts/', include('accounts.urls')),
]

# ✅ Serve static & media files only in DEBUG mode (local dev)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
