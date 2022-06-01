from reviews.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "role", "bio"
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email"
        )

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError('Нельзя создать пользователя с никнеймом - "me"')
        return data


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = (
            "username", "email"
        )
