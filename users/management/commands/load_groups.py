from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создает группу "Модераторы" и назначает ей соответствующие права.'

    def handle(self, *args, **kwargs):
        user_content_type = ContentType.objects.get_for_model(User)
        moderators_group, _ = Group.objects.get_or_create(name="Модераторы")
        moderator_permissions = [
            ("view_user", "Может просматривать пользователей"),
            ("change_user", "Может редактировать пользователей"),
        ]
        for codename, name in moderator_permissions:
            existing_permission = Permission.objects.filter(
                codename=codename, content_type=user_content_type
            ).first()
            if existing_permission:
                moderators_group.permissions.add(existing_permission)
                continue

            permission = Permission.objects.create(
                codename=codename, content_type=user_content_type, name=name
            )
            moderators_group.permissions.add(permission)
        self.stdout.write(self.style.SUCCESS("Группа модераторов и права созданы."))
