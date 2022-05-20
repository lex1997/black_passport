from time import sleep

import requests
from loguru import logger

from passport.models import Terrorist, Passport

# INN_URL = "https://service.nalog.ru/inn-proc.do"
# MAX_INN_ATTEMPTS = 15
#
#



def check_person_rfm(lastname: str, name: str, middlename: str, dob: str):
    """ Проверка пользователя по реестру Росфинмониторинг(таблица RFM).
        Возвращает булевый признак (True == проверка пройдена, человек не террорист)
    """
    middlename = middlename if middlename else ""
    full_name = (lastname + " " + name + " " + middlename).strip()
    return not Terrorist.objects.filter(name=full_name, birthday=dob).exists()


def check_person_fms(series: str, number: str):
    """ Проверяет паспорт по базе ФМС(таблица FMS).
        Возвращает булевый признак. (True == Проверка пройдена, паспорт валидный)
    """
    return not Passport.objects.filter(series=series, number=number).exists()


# def check_inn(
#     lastname: str,
#     name: str,
#     middlename: str,
#     birthday: str,
#     place_of_birth: str,
#     series_number: str,
#     passport_date: str,
# ):
#     # TODO переделать сигнатуру
#     """ Функция проверяет наличие инн по паспортным данным через сайт service.nalog.ru,
#         и возвращает инн, если он найден или False, если его нет в базе.
#         Если у клиента отсутсвует отчество, то middlename должен быть равен 'no_middlename'.
#         birthday и passport_date передаются в формате YYYY-MM-DD
#     """
#     url = INN_URL
#     ser_num_passport = series_number.replace(" ", "")
#
#     birthday = birthday.split("-")
#     birthday = birthday[2] + "." + birthday[1] + "." + birthday[0]
#     passport_date = passport_date.split("-")
#     passport_date = passport_date[2] + "." + passport_date[1] + "." + passport_date[0]
#
#     data = {
#         "c": "innMy",
#         "captcha": "",
#         "captchaToken": "",
#         "fam": lastname,
#         "nam": name,
#         "bdate": birthday,
#         "bplace": place_of_birth,
#         "doctype": 21,
#         "docno": f"{ser_num_passport[0:2]} {ser_num_passport[2:4]} {ser_num_passport[4:11]}",
#         "docdt": passport_date,
#     }
#
#     if middlename == "no_middlename":
#         data["opt_otch"] = 1
#     else:
#         data["otch"] = middlename
#
#     count = 0
#     response = None
#     error = None
#
#     while count <= MAX_INN_ATTEMPTS and not response:
#         try:
#             r = requests.post(url, data=data, timeout=30)
#             response = r.json()
#         except requests.exceptions.ReadTimeout:
#             return {"result": False, "reason": "service.nalog.ru not responding"}
#         except Exception as e:
#             error = e
#             count += 1
#             sleep(2)
#
#     if not response:
#         logger.exception(error)
#         logger.info(data)
#         return {"result": False, "reason": "error in service.nalog.ru"}
#
#     # TODO: переписать на декоратор, нельзя запускать функцию чаще, чем раз в секунду
#     sleep(1)
#
#     code = response.get("code")
#     if code == 1:
#         return {"result": response["inn"]}
#     elif code == 0:
#         return {"result": False}
#
#     error = response.get("ERROR")
#     if error == "-":
#         return {"result": "error", "reasons": error}
