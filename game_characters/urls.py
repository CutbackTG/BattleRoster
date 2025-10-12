from django.urls import path
from . import views

urlpatterns = [
    path('', views.party_view, name='party'),  # main party page
]
