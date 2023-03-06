from django.contrib.auth.models import AbstractUser, UserManager

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validator import validator_year


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class UserManagerYaMDB(UserManager):
    def create_superuser(self, username, email=None,
                         password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        return super().create_superuser(username, email,
                                        password, **extra_fields)


class User(AbstractUser):
    objects = UserManagerYaMDB()

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='E-mail',
    )
    confirmation_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Код подтверждения',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == UserRole.ADMIN
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR


class Category(models.Model):
    """Модель категорий произведений."""

    name = models.CharField(
        'имя категории',
        unique=True,
        max_length=250,
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает имя категории."""
        return self.name


class Genre(models.Model):
    """Модель жанров произведений."""

    name = models.CharField(
        'имя жанра',
        max_length=250,
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        max_length=50,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Возвращает имя жанра."""
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
        blank=True,
    )
    description = models.TextField(
        'описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='жанр',
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Возвращает название призведения."""
        return self.name


class GenreTitle(models.Model):
    """Модель связи жанра и произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=('произведение'),
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name=('жанр'),
    )

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title',
            ),
        )

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    """Модель отзывов о произведении."""

    text = models.TextField(verbose_name='Текст')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Значение рейтинга не может быть ниже 1.'),
            MaxValueValidator(10, 'Значение рейтинга не может быть выше 10.'),
        ],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title'),
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Отзыв {self.author.username} на {self.title.name}'


class Comment(models.Model):
    """Модель - комментарии к отзывам."""

    text = models.TextField(verbose_name='Текст')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращает текст комментария."""
        return self.text
