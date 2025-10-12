from django.contrib import admin
from django.urls import path, include
from game_characters.views import home_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
]

# ✅ Serve static & media files only in DEBUG mode (local dev)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
