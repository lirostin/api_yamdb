from django.contrib import admin
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, Review, Title, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_rating',
    )

    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(avg_score=Avg('score', default=0))
        return round(rating.get('avg_score'), 1)

    get_rating.short_description = 'Рейтинг'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'score', 'pub_date')
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'pub_date')
    search_fields = ('author',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'role')
    list_filter = ('username',)
    empty_value_display = '-пусто-'
