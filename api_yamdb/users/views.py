from users.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions, viewsets, status, generics
from users.permissions import IsAdmin
from users.serializers import UserSerializer, SignUpSerializer
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        methods=["patch", "get"],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        user = self.request.user
        if request.method == "GET":
            serializer = UserSerializer(user, status=status.HTTP_200_OK)
        else:
            serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpViewSet(generics.CreateAPIView):
    serializer_class = SignUpSerializer


class TokenViewSet(generics.CreateAPIView):
    serializer_class = SignUpSerializer
