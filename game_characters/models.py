from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Character(models.Model):
    """Full D&D-style character model."""

    # Basic Info
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=100, blank=True)
    char_class = models.CharField(max_length=100, blank=True)
    background = models.CharField(max_length=100, blank=True)
    alignment = models.CharField(max_length=100, blank=True)
    level = models.PositiveIntegerField(default=1)

    # Core Stats
    strength = models.PositiveIntegerField(default=10)
    dexterity = models.PositiveIntegerField(default=10)
    constitution = models.PositiveIntegerField(default=10)
    intelligence = models.PositiveIntegerField(default=10)
    wisdom = models.PositiveIntegerField(default=10)
    charisma = models.PositiveIntegerField(default=10)

    # Personality
    traits = models.TextField(blank=True)
    ideals = models.TextField(blank=True)
    bonds = models.TextField(blank=True)
    flaws = models.TextField(blank=True)

    # Inventory
    equipment = models.TextField(blank=True)
    weapons = models.TextField(blank=True)

    # Spells & Notes
    spells = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Owner
    player = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="characters", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} (Lv.{self.level})"


class Party(models.Model):
    """Party of characters led by a Dungeon Master."""

    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_parties"
    )
    members = models.ManyToManyField(User, related_name="parties", blank=True)

    def __str__(self):
        return f"{self.name} (DM: {self.dungeon_master.username})"
