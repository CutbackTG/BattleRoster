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
