from api.views import UserViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router_v1 = SimpleRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_patterns = []

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]