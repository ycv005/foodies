from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5}}

    def create(self, validated_data):
        """Create a new user and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update exisiting and authenticated user profile"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            username=email,
            password=password,
        )
        if not user:
            msg = _('Invalid Credential, Try again')
            raise serializers.ValidationError(msg, code='authenticatoion')

        attrs['user'] = user
        return attrs
