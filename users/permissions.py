from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    message = "Группа модераторов"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator_group').exists()

class IsOwner(BasePermission):
    message = "Только владелец может редактировать объект"

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user