import logging

from celery import shared_task
from passport.rfm import upload_list_rfm
from passport.fms import upload_fms
import datetime as dt

logger = logging.getLogger(__name__)


@shared_task(bind=True,
             name='update_rfm',
             max_retries=3,
             soft_time_limit=20)
def update_rfm(self):
    logger.info(f'{dt.datetime.now()} starting upload list rfm')
    upload_list_rfm()
    logger.info(f'{dt.datetime.now()} finish upload list rfm')


@shared_task(bind=True,
             name='update_fms',
             max_retries=3,
             soft_time_limit=20)
def update_fms(self):
    logger.info(f'{dt.datetime.now()} starting upload list fms')
    upload_fms()
    logger.info(f'{dt.datetime.now()} finish upload list fms')
