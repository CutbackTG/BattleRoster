from django.db import models
from django.conf import settings

class Party(models.Model):
    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dm_parties"
    )

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_characters",  # ✅ changed from "characters" to avoid clash
    )
    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name="members",
        null=True,
        blank=True
    )
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    mana = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"
