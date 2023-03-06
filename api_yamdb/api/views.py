from http import HTTPStatus

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (IsAdmin, IsAdminUserOrReadOnly,
                             IsAuthorModerAdminOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializers,
                             GenreSerializer, ReadOnlyTitleSerializer,
                             ReviewSerializer, SignUpUserSerializer,
                             TitleSerializer, TokenSerializer, UserSerializer)

from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    """ Пользователь."""

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
    """ Вывод списка всех произведений. """
    
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

class ReviewViewSet(viewsets.ModelViewSet):
    """Вывод отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
