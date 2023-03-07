from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ для пользователей с ролью гость. Любому для чтения"""

    message = 'По данному запросу нет доступа.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAdminUser(permissions.BasePermission):
    """Доступ для пользователей с ролью администратора."""

    message = 'По данному запросу нет доступа.'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAuthorOrModerAdminPermission(permissions.BasePermission):
    """Доступ для пользователя с ролью админ, модер, автор."""

    message = 'По данному запросу нет доступа.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )
