from api import serializers
from api.filters import TitleFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnlyAnonymusPermission,
                             IsAuthorOrAdminOrModerator)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    lookup_field = "username"

    @action(methods=["patch", "get"], detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = serializers.UserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnlyAnonymusPermission
    )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return serializers.TitleCreateSerializer
        return serializers.TitleSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg(
            "reviews__score")).order_by("id")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentsSerializer
    permission_classes = (IsAuthorOrAdminOrModerator,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)


class GetMixin(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('name',)
    search_fields = ('name',)
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)


class GenreViewSet(GetMixin):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class CategoryViewSet(GetMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_signup(request):
    serializer = serializers.SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get("username")
    email = request.data.get("email")
    try:
        user, created = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            'Никнейм должен быть уникальный у каждого прользователя',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)

    send_mail("Код подтверждения,",
              f"Ваш код подтверждения: {confirmation_code}",
              "valid_email@yamdb.fake",
              (email,))
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = serializers.TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get("username")
    confirmation_code = request.data.get("confirmation_code")
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({f"token: {token}"}, status=status.HTTP_200_OK)
    return Response(
        {"WRONG CODE": "Неверный код подтверждения"},
        status=status.HTTP_400_BAD_REQUEST
    )
