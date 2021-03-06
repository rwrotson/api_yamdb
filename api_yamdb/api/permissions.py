from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminPermission(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.user.is_active:
            if request.user.is_admin:
                return True
        return bool(request.user and request.user.is_staff)


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class IsModeratorPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin)
