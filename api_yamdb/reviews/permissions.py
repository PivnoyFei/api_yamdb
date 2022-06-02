from rest_framework import permissions


class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (request.user.is_staff
                    or request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                    or request.method == 'POST'):
                return True
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
