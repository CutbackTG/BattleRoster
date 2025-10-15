from django.db import models
from django.conf import settings

class Character(models.Model):
    """A D&D-style character associated with a user or anonymous player."""
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    race = models.CharField(max_length=100, blank=True, null=True)
    class_type = models.CharField(max_length=100, blank=True, null=True)
    health = models.PositiveIntegerField(default=100)
    mana = models.PositiveIntegerField(default=50)

    # Core attributes
    strength = models.PositiveIntegerField(default=10)
    dexterity = models.PositiveIntegerField(default=10)
    constitution = models.PositiveIntegerField(default=10)
    intelligence = models.PositiveIntegerField(default=10)
    wisdom = models.PositiveIntegerField(default=10)
    charisma = models.PositiveIntegerField(default=10)

    # Text fields for freeform input
    equipment = models.TextField(blank=True, null=True)
    weapons = models.TextField(blank=True, null=True)
    spells = models.TextField(blank=True, null=True)

    # Link to a player (optional for anonymous users)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_characters',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"


class Party(models.Model):
    """A party that can include multiple players, led by a Dungeon Master."""
    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='game_owned_parties'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='game_parties',
        blank=True
    )

    def __str__(self):
        return f"{self.name} (DM: {self.dungeon_master.username})"


class Campaign(models.Model):
    """Optional: a campaign to group parties or adventures."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    dungeon_master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='campaigns'
    )
    parties = models.ManyToManyField(Party, blank=True, related_name='campaigns')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
