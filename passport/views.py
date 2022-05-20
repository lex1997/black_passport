# from rest_framework import generics
# from django.shortcuts import render
#
# from rest_framework.response import Response
# from rest_framework.views import APIView

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from passport.rfm import upload_list_rfm
from passport.fms import upload_fms

@csrf_exempt
def upload_rfm_handler(request):
    upload_list_rfm()
    return HttpResponse('done', status=200)


@csrf_exempt
def upload_fms_handler(request):
    upload_fms()
    return HttpResponse('done', status=200)

# class BlackPassportAPIView(APIView):
#     def post(self, request):
#         return Response()