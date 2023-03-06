from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import (Category, Comment, Genre, Review, Title, User,
                            validate_username)
from reviews.validator import validator_year


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


class CommentSerializers(serializers.ModelSerializer):
    """Серилизатор для комментариев отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        read_only_fields = ('author', )

class ReviewSerializer(serializers.ModelSerializer):
    """Серилизатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
                and request.user.reviews.filter(title=title).exists()):
            raise ValidationError(
                'Нельзя делать 2 отзыва на одно и тоже произведение.'
            )
        return data
    
    def validate_score(self, value):
        """Проверка, что оценка в диапазоне от 1 до 10."""
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Оценка может быть от 1 до 10!')
        return value
