# DJANGO REST FRAMEWORK IMPORTS
from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    """
    Allows access only to superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
