from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Character, Party


class CharacterInline(admin.TabularInline):
    """Show characters inline within the User admin page."""
    model = Character
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin view for Users (Players & DMs)."""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')
    inlines = [CharacterInline]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    """Admin panel for Characters."""
    list_display = ('name', 'level', 'health', 'mana', 'player')
    list_filter = ('level', 'player')
    search_fields = ('name', 'player__username')
    ordering = ('player', 'name')


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    """Admin panel for Parties."""
    list_display = ('name', 'dungeon_master')
    list_filter = ('dungeon_master',)
    search_fields = ('name', 'dungeon_master__username')
    filter_horizontal = ('members',)  # ✅ Makes adding members easier
