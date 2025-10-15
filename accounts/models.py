from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('dungeon_master', 'Dungeon Master'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def is_player(self):
        return self.role == 'player'

    def is_dungeon_master(self):
        return self.role == 'dungeon_master'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Character(models.Model):
    """A D&D-style character."""
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

    # Linked to a player (optional for anonymous users)
    player = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='characters',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"


class Party(models.Model):
    """A party that can include multiple players, led by a Dungeon Master."""
    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='owned_parties'
    )
    members = models.ManyToManyField(
        'accounts.User', related_name='parties', blank=True
    )

    def __str__(self):
        return f"{self.name} (DM: {self.dungeon_master.username})"
