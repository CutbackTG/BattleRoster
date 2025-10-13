from django.db import models
from django.conf import settings


class Character(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=100)
    mana = models.PositiveIntegerField(default=50)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_characters"
    )

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"


class Party(models.Model):
    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_parties_led"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="game_parties_joined",
        blank=True
    )

    def __str__(self):
        return f"{self.name} (DM: {self.dungeon_master.username})"
