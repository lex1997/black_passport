from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


class Command(BaseCommand):
    # def handle(self, *args, **options):
    #     if CrontabSchedule.objects.filter(minute='*/1').exists():
    #         CrontabSchedule.objects.filter(minute='*/1').delete()
    #     CrontabSchedule.objects.create(minute='*/1')
    #
    #     if PeriodicTask.objects.filter(
    #         name='update_db',
    #     ):
    #         PeriodicTask.objects.filter(
    #         name='update_db',
    #     ).delete()
    #     PeriodicTask.objects.create(
    #         name='update_db',
    #         task='black_passport._celery.update_db',
    #         crontab=CrontabSchedule.objects.get(minute='*/1'),
    #         one_off=True,
    #     )
    def handle(self, *args, **options):
        if CrontabSchedule.objects.filter(hour='2', day_of_month='*/3').exists():
            CrontabSchedule.objects.filter(hour='2', day_of_month='*/3').delete()
        CrontabSchedule.objects.create(hour='2', day_of_month='*/3')

        if PeriodicTask.objects.filter(
            name='update_db',
        ):
            PeriodicTask.objects.filter(
            name='update_db',
        ).delete()
        PeriodicTask.objects.create(
            name='update_db',
            task='black_passport._celery.update_db',
            crontab=CrontabSchedule.objects.get(hour='2', day_of_month='*/3'),
            one_off=True,
        )
        print('Таски на обновление справочников заведены')