from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к чтению (list, retrieve) — для всех.
    Доступ к изменению (update, delete, create) — только для админов.
    """

    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS для всех
        if view.action in ['list', 'retrieve']:
            return True
        # Для остальных действий разрешаем только администраторам
        return request.user and request.user.is_staff
