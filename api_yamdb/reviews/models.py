from django.contrib.auth.models import AbstractUser
from django.db import models


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = [(ADMIN, ADMIN), (MODERATOR, MODERATOR), (USER, USER), ]


class User(AbstractUser):
    """Абстрактная модель пользователя."""


class Category(models.Model):
    """Модель категорий произведений."""


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
        return f'{self.name} {self.name}'


class Title(models.Model):
    """Модель произведений."""


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""


class Review(models.Model):
    """Модель отзывов о произведении."""


class Comment(models.Model):
    """Модель - комментарии к отзывам."""
