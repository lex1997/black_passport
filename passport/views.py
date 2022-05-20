# from rest_framework import generics
# from django.shortcuts import render
#
# from rest_framework.response import Response
# from rest_framework.views import APIView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from passport.methods import check_person_rfm
from passport.rfm import upload_list_rfm
from passport.fms import upload_fms
from passport.serializers import TerroristSerializer


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
        serilizer = TerroristSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)

        # lastname: str,
        # name: str,
        # middlename:
        return Response({'data': check_person_rfm(request.data['lastname'], request.data['name'], request.data['middlename'], request.data['birthday'])})