from django.contrib import admin
from .models import User
from game_characters.models import Character, Party

admin.site.register(User)
admin.site.register(Character)
admin.site.register(Party)
