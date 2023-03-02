from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet

router = SimpleRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_patterns = []

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router.urls)),
]