from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin' or (
                request.method in permissions.SAFE_METHODS):
            return True
        raise PermissionDenied('Нет прав доступа')
