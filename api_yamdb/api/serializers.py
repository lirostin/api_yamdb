from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Genre


class GenreSerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Genre.objects.all(),
                message='Жанр уже существует.',
            )
        ],
    )

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
