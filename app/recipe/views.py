from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, RecipeDetailSerializer
)
from .models import Tag, Ingredient, Recipe


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attribute"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """return user related objects"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagListViewSet(BaseRecipeAttrViewSet):
    """Class for the showing tag list"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Class to manipulate the ingredient objects"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """Class to manipulate the recipe objects"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """return user related objects"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """return appropriate serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class
