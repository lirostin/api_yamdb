from rest_framework import filters, viewsets

from reviews.models import User
from api.serializers import UserSerializer
from api.permissions import (
    IsAdmin, IsAdminUserOrReadOnly,
    IsAuthorModerAdminOrReadOnly
)

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
