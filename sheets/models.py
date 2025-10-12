from django.db import models
from django.conf import settings

class CharacterLocal(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    mana = models.IntegerField(default=50)
    notes = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="local_characters",  # ✅ renamed to avoid clashes
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (owned by {self.owner.username})"
