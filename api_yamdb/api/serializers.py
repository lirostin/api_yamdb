from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from reviews.models import Category, Genre, Title
from reviews.validator import validator_year


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


class TitleSerializer(serializers.ModelSerializer):
    """Модель произведений для всех."""

    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    year = serializers.IntegerField(validators=[validator_year])

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category'),
                message='Произведение уже существует.',
            )
        ]


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    """Модель произведений только для чтения: read_only=True."""

    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
