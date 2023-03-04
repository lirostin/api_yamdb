from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer
from rest_framework import filters

from reviews.models import Category, Genre


class CategoryViewSet(ListCreateDestroyViewSet):
    """ Вывод списка всех категорий. """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """ Вывод списка всех жанров. """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
