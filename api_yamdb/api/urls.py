from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    TitleViewSet, UserViewSet, get_token, signup_user)
from api.views import UserViewSet

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('titles', TitleViewSet, basename='title')

auth_patterns = [
    path('signup/', signup_user),
    path('token/', get_token),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls), name='api'),
]
