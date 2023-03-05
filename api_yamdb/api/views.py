from rest_framework import filters, viewsets

from api.serializers import UserSerializer
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    """ Пользователь."""
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    queryset = User.objects.all()
    permission_classes = ()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
