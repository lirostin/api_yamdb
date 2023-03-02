from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, signup_user, get_token

router = SimpleRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_patterns = [
    path('signup/', signup_user),
    path('token/', get_token),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]