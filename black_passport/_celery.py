
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'black_passport.settings')

app = Celery('black_passport')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def test(self):
    print('Рабооооооооотает')


