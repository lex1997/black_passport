import os

import pandas as pd
import requests
from django.conf import settings
from sqlalchemy import create_engine

from passport.utils import create_folder_if_not_exist


FILE_PATH = 'passport/data/list_of_expired_passports.csv.bz2'
FILE_EMPTY_PATH = 'passport/data/EMPTY.csv'
FMS_URL = 'https://проверки.гувм.мвд.рф/upload/expired-passports/list_of_expired_passports.csv.bz2'


def upload_fms(file_path=FILE_PATH, empty_file=FILE_EMPTY_PATH):
    """ Функция загружает данные в таблицу fms.
        file_path должен вести к файлу формата .bz2, полученного функцией get_fms.
        Данные загружаются в таблицу 'кусками' по 500 тысяч записей.
    """

    get_fms(file_path)

    column_names = ['series', 'number']
    d_type = {'series': str, 'number': str}

    chunk_size = 500_000

    df_empty = pd.read_csv(empty_file,
                              skiprows=1,
                              chunksize=chunk_size,
                              delimiter=',',
                              header=None,
                              names=column_names,
                              dtype=d_type,
                              )

    for df in df_empty:
        df.to_sql('passport_passport', con=_get_engine(), index=False, if_exists='replace')

    df_iterator = pd.read_csv(file_path,
                              skiprows=1,
                              compression='bz2',
                              chunksize=chunk_size,
                              delimiter=',',
                              header=None,
                              names=column_names,
                              dtype=d_type,
                              )

    for df in df_iterator:
        df.to_sql('passport_passport', con=_get_engine(), index=False, if_exists='append')

    os.remove(file_path)


def _get_engine():
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']
    database_name = settings.DATABASES['default']['NAME']
    database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
        user=user,
        password=password,
        database_name=database_name,
    )
    return create_engine(database_url, echo=False)


def get_fms(file_path):
    """ Функция скачивает базу недействительных паспортов"""

    create_folder_if_not_exist(file_path)
    response = requests.get(FMS_URL, stream=True)
    with open(file_path, mode='wb') as f:
        f.write(response.content)

