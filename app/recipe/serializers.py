from rest_framework import serializers
from .models import Tag, Ingredient


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Tag objects"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the ingredient"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']
