from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer, IngredientSerializer
from .models import Tag, Ingredient


class TagListViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Class for the showing tag list"""
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Tag.objects.all()

    def get_queryset(self):
        queryset = Tag.objects.filter(
            user__id=self.request.user.id
        )
        return queryset

    def perform_create(self, serializers):
        """Create a new tag"""
        serializers.save(user=self.request.user)


class IngredientViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Class to manipulate the ingredient objects"""
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        queryset = Ingredient.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializers):
        """creating ingredient object pass extra(user) data as well"""
        serializers.save(user=self.request.user)
