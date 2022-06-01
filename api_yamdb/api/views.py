from reviews.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets, status, generics
from api.permissions import IsAdmin
from api.serializers import UserSerializer, SignUpSerializer, TokenSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(methods=["patch", "get"], detail=False,
            permission_classes=(permissions.IsAuthenticated,))

    def me(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = request.data.get('username')
    email = request.data.get('email')
    user, created = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)

    send_mail('Код подтверждения,',
              f'Ваш код подтверждения: {confirmation_code}',
              'valid@yamdb.fake',
              [email])
    token = AccessToken.for_user(user)

    return Response(
        {f'token: {token}'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response(
            {'OK': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        {'WRONG CODE': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )
