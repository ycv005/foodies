from rest_framework import serializers
from .models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize the recipe model"""
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['id']
