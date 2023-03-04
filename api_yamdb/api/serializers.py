from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre

class CategorySerializer(serializers.ModelSerializer):
    """Модель категорий произведений."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(
                queryset=Category.objects.all(),
                message='Категория уже существует.',
            )
        ],
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )

class GenreSerializer(serializers.ModelSerializer):
    """Модель жанров произведений."""

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
