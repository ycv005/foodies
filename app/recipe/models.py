from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Tag model that support tag feature"""
    name = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
