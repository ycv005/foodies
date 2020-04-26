from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Tag objects"""
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
