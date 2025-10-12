from django.contrib import admin
from django.urls import path, include
from game_characters import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),  # Homepage route
    path('accounts/', include('accounts.urls')),
    path('characters/', include('game_characters.urls')),
]

# Static files for development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
