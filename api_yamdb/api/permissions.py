from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from .models import CustomUser


class IsAdminPermission(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.user.is_active:
            if request.user.role == CustomUser.RoleChoice.ADMIN:
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
            or request.user.role == CustomUser.RoleChoice.MODERATOR
            or request.user.role == CustomUser.RoleChoice.ADMIN)


class ReviewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['partial_update', 'destroy']:
            if (request.user == obj.author
                    or request.user.role in ['admin', 'moderator']
                    or request.user.is_staff):
                return True
            return False
