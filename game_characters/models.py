from django.db import models
from django.conf import settings

# Character model
class Character(models.Model):
    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(default=1)
    health = models.PositiveIntegerField(default=100)
    mana = models.PositiveIntegerField(default=50)
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters"
    )

    def __str__(self):
        return f"{self.name} (Lv {self.level})"


# Party model
class Party(models.Model):
    name = models.CharField(max_length=100)
    dungeon_master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_parties"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="parties",
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"
