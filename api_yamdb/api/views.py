from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import GenreSerializer
from rest_framework import filters

from reviews.models import Genre


class GenreViewSet(ListCreateDestroyViewSet):
    """ Вывод списка всех жанров. """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'
