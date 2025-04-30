from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from .models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

class IsModerator(BasePermission):
    message = "Группа модераторов"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator_group').exists()

class IsOwner(BasePermission):
    message = "Только владелец может редактировать объект"

    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.id == request.user.id or request.user.is_staff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':  # Регистрация доступна любому пользователю
            permission_classes = []
        elif self.action == 'retrieve':  # Просмотр любого профиля возможен
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'partial_update':  # Редактировать можно только собственный профиль
            permission_classes = [IsAuthenticated, IsOwner()]
        elif self.action == 'destroy':  # Удаление доступно только самому себе
            permission_classes = [IsAuthenticated, IsOwner()]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]