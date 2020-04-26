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


class Recipe(models.Model):
    """Recipe model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    time_took_min = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    url = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
