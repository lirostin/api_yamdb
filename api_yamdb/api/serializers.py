from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, validate_username


USER_NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=USER_NAME_MAX_LENGTH,
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
    username = serializers.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        required=True,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)


class SignUpUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH
    )
    username = serializers.CharField(
        max_length=EMAIL_MAX_LENGTH,
        validators=[validate_username]
    )