import os

from celery.schedules import crontab

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'black_passport.settings')

app = Celery('black_passport')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(result_expires=3600,
                enable_utc=True,
                timezone='Europe/Moscow', )

app.conf.beat_schedule = {
    "every 3th days of month at 2 AM": {
        "task": "update_rfm",  # <---- Name of task
        "schedule": crontab(day_of_month='*/3',
                            hour='1',
                            minute=0,
                            )
    },
    "every 3th days of month at 3 AM": {
        "task": "update_fms",  # <---- Name of task
        "schedule": crontab(day_of_month='*/3',
                            hour='2',
                            minute=0,
                            )
    }
}


# Load task modules from all registered Django apps.
app.autodiscover_tasks()


