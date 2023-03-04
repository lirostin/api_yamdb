from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             ReadOnlyTitleSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
