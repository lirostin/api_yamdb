from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Review)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(GenreTitle)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',
#         'review',
#         'author',
#         'pub_date',
#     )
#     list_filter = ('author',)
#     empty_value_display = '-пусто-'
