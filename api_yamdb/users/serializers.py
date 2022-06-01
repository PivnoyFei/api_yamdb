from users.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "role", "bio"
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("username", "email"),
                message="Никнейм и почта должны быть уникальными."
            )
        ]


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username", "email"
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("username", "email"),
                message="Никнейм и почта должны быть уникальными."
            )
        ]
