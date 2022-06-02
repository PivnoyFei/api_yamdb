from api.permissions import IsAdmin, IsAuthorOrAdminOrModerator
from django_filters.rest_framework import DjangoFilterBackend
from api import serializers
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, Review, Title
from .filters import TitleFilter

#from rest_framework.pagination import LimitOffsetPagination


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrAdminOrModerator)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.TitleSerializer
        return serializers.TitleSerializer


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
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            pk=review_id,
            title__id=title_id,
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            pk=review_id,
            title__id=title_id,
        )
        serializer.save(author=self.request.user, review=review)



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
