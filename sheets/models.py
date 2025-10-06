from django.db import models

from django.db import models
from django.conf import settings

class CharacterLocal(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='characters')
    sheet_row = models.PositiveIntegerField()
    name = models.CharField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'sheet_row')