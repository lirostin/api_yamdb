import re

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from reviews.validators import validate_username

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = [(ADMIN, ADMIN), (MODERATOR, MODERATOR), (USER, USER), ]


def validate_username(value):
    """Проверка на недопустимые username."""
    if value.lower() == 'me':
        raise ValidationError('"me" - Недопустимое имя пользователя.')

    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Недопустимый набор символов: "{value}"'),
            params={'value': value},
        )


class User(AbstractUser):
    """Абстрактная модель пользователя."""
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
    
    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )

    @property
    def is_user(self):
        return self.role == USER


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

# Создал комментарий для commit
