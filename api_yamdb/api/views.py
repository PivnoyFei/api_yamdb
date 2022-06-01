from rest_framework import viewsets
from users.permissions import IsAdmin


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
