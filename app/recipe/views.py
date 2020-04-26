from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TagSerializer
from .models import Tag


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
        ).order_by('-name')
        return queryset

    def perform_create(self, serializers):
        """Create a new tag"""
        serializers.save(user=self.request.user)
