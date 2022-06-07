from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         PeriodicTask.objects.create(
#             name='Test',
#             task='black_passport._celery.test',
#             interval=IntervalSchedule.objects.get(every=3, period='seconds'),
#         )
#         # Необходимая логика после удачного получения статуса
#         print('Запуск обновления бд')