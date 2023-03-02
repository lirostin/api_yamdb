import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = [(ADMIN, ADMIN), (MODERATOR, MODERATOR), (USER, USER), ]

ROLE_MAX_LENGTH = max(len(role) for role, _ in ROLE_CHOICES)

USER_NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254



"""Проверка на недопустимые username."""
def validate_username(value):
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
        max_length=USER_NAME_MAX_LENGTH,
        unique=True,
        blank=False,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=USER_NAME_MAX_LENGTH,
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default='user'
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

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
