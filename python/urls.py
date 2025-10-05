from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('characters:list')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('characters/', include(('characters.urls','characters'), namespace='characters')),
    path('parties/', include(('parties.urls','parties'), namespace='parties')),
])
