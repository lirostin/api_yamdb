from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User, validate_username


USER_NAME_MAX_LENGTH = 150


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