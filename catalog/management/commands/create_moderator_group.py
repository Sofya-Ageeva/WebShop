from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создаёт группу "Модератор продуктов" с необходимыми правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        content_type = ContentType.objects.get_for_model(Product)

        permissions = [
            'can_unpublish_product',
            'delete_product',
        ]

        for perm_codename in permissions:
            try:
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )
                group.permissions.add(permission)
                self.stdout.write(f'Добавлено право: {perm_codename}')
            except Permission.DoesNotExist:
                self.stdout.write(f'Право {perm_codename} не найдено')

        self.stdout.write(self.style.SUCCESS('Группа настроена успешно!'))
