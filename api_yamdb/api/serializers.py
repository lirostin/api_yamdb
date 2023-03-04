from rest_framework import serializers
from rest_framework.validators import UniqueValidator


from reviews.models import Comment, Genre

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
