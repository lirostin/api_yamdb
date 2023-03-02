from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, viewsets, serializers, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from reviews.models import User
from api.serializers import (
    UserSerializer,
    TokenSerializer,
    SignUpUserSerializer
)
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

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    serializer = SignUpUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    try:
        user, _ = User.objects.get_or_create(
            email=email,
            username=username
        )
    except IntegrityError:
        raise serializers.ValidationError('Такой пользователь уже существует')

    confirmation_code = default_token_generator.make_token(user)

    message = (
        f'Ваш код для подтверждения: {confirmation_code}'
    )

    send_mail(
        'Регистрация',
        message,
        'from@example.com',
        [email, ],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User,
                             username=request.data.get('username'))
    confirmation_code = request.data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        refresh = AccessToken.for_user(user)
        context = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(context, status=HTTPStatus.OK)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
