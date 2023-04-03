from rest_framework.permissions import *


class IsAdminOrReadOnly(BasePermission):
    """
    The request is admin as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsAdminOrIsAuthenticated(BasePermission):
    """
    The request is admin as a user, or is authenticated for read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS and
             request.user and
             request.user.is_authenticated) or
            (request.user and
             request.user.is_staff)
        )
