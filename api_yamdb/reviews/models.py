from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.validator import validator_year


class User(AbstractUser):
    """Абстрактная модель пользователя."""


class Category(models.Model):
    """Модель категорий произведений."""

    name = models.CharField(
        'имя категории',
        max_length=50
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""

    name = models.CharField(
        'имя жанра',
        max_length=50
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        max_length=50,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        'название произведения',
        max_length=100,
    )
    year = models.IntegerField(
        'год выпуска',
        validators=[validator_year], 
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
    )
    description = models.TextField(
        'описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанр'
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=('произведение')
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=('жанр')
    )

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(models.Model):
    """Модель отзывов о произведении."""


class Comment(models.Model):
    """Модель - комментарии к отзывам."""
