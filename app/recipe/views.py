from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer, IngredientSerializer
from .models import Tag, Ingredient


class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attribute"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """return user related objects"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializers):
        """creating object pass extra(user) data as well"""
        serializers.save(user=self.request.user)


class TagListViewSet(BaseRecipeAttrViewSet):
    """Class for the showing tag list"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Class to manipulate the ingredient objects"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
