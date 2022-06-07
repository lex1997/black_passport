import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'black_passport.settings')
app = Celery('black_passport')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


import logging
import datetime as dt
from passport.rfm import upload_list_rfm
from passport.fms import upload_fms

logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_db(self):
    logger.info(f'{dt.datetime.now()} starting upload list rfm')
    upload_list_rfm()
    logger.info(f'{dt.datetime.now()} finish upload list rfm')
    logger.info(f'{dt.datetime.now()} starting upload list fms')
    upload_fms()
    logger.info(f'{dt.datetime.now()} finish upload list fms')


@app.task(bind=True)
def test(self):
    print('Рабооооооооотает')

