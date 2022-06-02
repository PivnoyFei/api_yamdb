from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "role", "bio"
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if data["username"] == "me":
            raise serializers.ValidationError(
                'Нельзя создать пользователя с никнеймом - "me"'
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
