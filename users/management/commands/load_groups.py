from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User


class Command(BaseCommand):
    help = 'Создает группу "Модераторы" и назначает ей соответствующие права.'

    def handle(self, *args, **kwargs):
        # Получаем объект модели User (или другой нужной вам модели)
        user_content_type = ContentType.objects.get_for_model(User)

        # Создаем группу модераторов
        moderators_group, _ = Group.objects.get_or_create(name="Модераторы")

        # Определяем права для модераторов
        moderator_permissions = [
            ("view_user", "Может просматривать пользователей"),
            ("change_user", "Может редактировать пользователей"),
        ]

        # Создаем и назначаем права группе
        for codename, name in moderator_permissions:
            # Сначала проверяем существование разрешения
            existing_permission = Permission.objects.filter(
                codename=codename,
                content_type=user_content_type
            ).first()

            if existing_permission:
                # Если разрешение уже существует, сразу добавляем его группе
                moderators_group.permissions.add(existing_permission)
                continue

            # Если разрешения нет то создаем его
            permission = Permission.objects.create(
                codename=codename,
                content_type=user_content_type,
                name=name
            )
            moderators_group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Группа модераторов и права созданы.'))