from django.db import models
from django.conf import settings


class Tag(models.Model):
    """Tag model that support tag feature"""
    name = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model to be use in the recipe"""
    name = models.CharField(unique=True, max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name
