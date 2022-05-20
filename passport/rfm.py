import csv
import re
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
from django.db.models.query_utils import Q

from passport.models import Terrorist
from passport.utils import create_folder_if_not_exist

FMS_URL = 'https://fedsfm.ru/documents/terrorists-catalog-portal-act'


def upload_list_rfm(data_file_path='passport/data/RFM.csv'):
    """ Функция парсит данные с террористами и сохраняет их в csv формате в папку data.
        Заносит полученные данные в таблицу Terrorist.
        Совокупность параметров name + birthday в таблице Terrorist уникальна.
        Если ФИО и дата рождения(name + birthday) не найдены в текущей версии реестра, статус записи в таблице
         меняется на 'Archive'.
    """

    get_rfm(data_file_path)

    try:  # отсутствие файла
        names = []
        birthdays = []

        with open(data_file_path) as data:
            for terrorist in data:
                names.append(terrorist.strip().upper().split(',')[0])
                birthdays.append(transform_date(terrorist.strip().split(',')[1]))
                _add_terrorist(terrorist)

            _archive_terrorists(names, birthdays)

        os.remove(data_file_path)

        return {'result': 'successful'}
    except IOError as e:
        return {'result': 'error', 'reasons': str(e)}


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def transform_date(date: str) -> str:
    return str(datetime.strptime(date.strip(), '%d.%m.%Y').date())


def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'fedsfm.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
    }

    r = requests.get(url, headers=headers, verify=False)
    return r.text


def parse_rfm(html):
    soup = BeautifulSoup(html, features='html.parser')
    data = soup.find('div', {'id': 'russianFL'})
    table = []
    for terrorist in data.find_all('li'):
        try:
            birthday = re.findall(r'[\d]{1,2}.[\d]{1,2}.[\d]{4}', terrorist.text)[0]
        except IndexError:
            continue
        first_name = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b|\W\s|\*', "", re.split(',', terrorist.text)[0])
        table.append([first_name, birthday])

        second_name = re.findall(r'\((.+)\)', terrorist.text)
        if second_name and len(second_name[0].split(';')) == 1:
            table.append([second_name[0], birthday])

        elif second_name and len(second_name[0].split(';')) > 1:
            for name in second_name[0].split(';'):
                table.append([name.strip(), birthday])

    return table


def write_csv(table, data_file_path):
    create_folder_if_not_exist(data_file_path)

    with open(data_file_path, 'w', newline="") as f:
        w = csv.writer(f)
        for row in table:
            w.writerow(row)


def get_rfm(data_file_path='passport/data/RFM.csv'):
    """Функция скачивает данные по террористам и формирует csv файл с этими данными"""
    url = FMS_URL
    html = get_html(url)
    table = parse_rfm(html)
    write_csv(table, data_file_path)


def _add_terrorist(terrorist):
    Terrorist.objects.get_or_create(name=terrorist.strip().upper().split(',')[0],
                                    birthday=transform_date(terrorist.split(',')[1]),
                                    status='Active')


def _archive_terrorists(names, birthdays):
    missing_terrorist_filter = Q(name__in=names) | Q(birthday__in=birthdays)
    Terrorist.objects.exclude(missing_terrorist_filter).update(status='Archive', tms_archive=get_current_time())
