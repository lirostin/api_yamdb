from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import CommentSerializers, GenreSerializer
from reviews.models import Genre, Review


class GenreViewSet(ListCreateDestroyViewSet):
    """ Вывод списка всех жанров. """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии для отзывов."""

    serializer_class = CommentSerializers
    permission_classes = (IsAdminUserOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
