from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from passport.methods import check_person_rfm, check_person_fms
from passport.rfm import upload_list_rfm
from passport.fms import upload_fms
from passport.serializers import TerroristSerializer, PassportSerializer


import datetime


def send_hello():
    time = datetime.datetime.now()
    print('hello world:[{}]'.format(time))

    

@csrf_exempt
def upload_rfm_handler(request):
    upload_list_rfm()
    return HttpResponse('done', status=200)


@csrf_exempt
def upload_fms_handler(request):
    upload_fms()
    return HttpResponse('done', status=200)

class RosFinMon(APIView):
    def post(self, request):
        """
        Вызывает проверку пользователя по реестру Росфинмониторинг по средством post запроса
        """
        serializer = TerroristSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if check_person_rfm(request.data['lastname'],
                            request.data['name'],
                            request.data['middlename'],
                            request.data['birthday']):
            result = 'True'
        else:
            result = 'False'

        return Response({f'Result: {result}'})


class FedMigServ(APIView):
    def post(self, request):
        '''
        Проверяет паспорт по базе ФМС(таблица FMS), посредством POST запроса
        '''
        serializer = PassportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if check_person_fms(request.data['series'], request.data['number']):
            result = 'True'
        else:
            result = 'False'

        return Response({f'Result: {result}'})