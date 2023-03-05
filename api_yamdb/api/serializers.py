from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, validate_username


class UserSerializer(serializers.ModelSerializer):
    """ Пользователь."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all()),
        ]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class TokenSerializer(serializers.Serializer):
    """ Токен."""
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)


class SignUpUserSerializer(serializers.Serializer):
    """ Регистрация."""
    email = serializers.EmailField(
        max_length=254
    )
    username = serializers.CharField(
        max_length=254,
        validators=[validate_username]
    )
