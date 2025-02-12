from django.core.management.base import BaseCommand
from projects.models import Team

class Command(BaseCommand):
    help = 'Копирует значение из поля name в old_name для всех записей'

    def handle(self, *args, **kwargs):
        teams = Team.objects.all()
        updated_count = 0

        for team in teams:
            if team.name:
                team.old_name = team.name
                team.save(update_fields=['old_name'])
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Успешно обновлено {updated_count} записей!'))
