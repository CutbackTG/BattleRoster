from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Player'),
        ('dm', 'DungeonMaster'),
    )
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='player')

    def is_player(self):
        return self.role == 'player'

    def is_dm(self):
        return self.role == 'dm'
