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


class Title(models.Model):
    """Модель произведений."""


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""


class Review(models.Model):
    """Модель отзывов о произведении."""


class Comment(models.Model):
    """Модель - комментарии к отзывам."""
