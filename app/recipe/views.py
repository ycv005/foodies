from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, RecipeDetailSerializer,
    RecipeImageSerializer
)
from .models import Tag, Ingredient, Recipe
from rest_framework.decorators import action
from rest_framework.response import Response


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
        elif self.action == "upload_image":
            return RecipeImageSerializer
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
