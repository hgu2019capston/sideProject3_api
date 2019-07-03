from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework import serializers
from rest_framework import viewsets

from data.models import Stones
from .serializers import OmokSerializer
from django.shortcuts import redirect, render

import subprocess
import os
import requests 

class Session1View(TemplateView):
    def get(self, request, **kwargs):
         if request.method == 'GET':
            return render(request, 'index.html', context=None)

    def post(self, request, **kwargs):
        return redirect(reverse('session2'))

class Session2View(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index1.html', context=None)
    
    def post(self, request, **kwargs):
        return redirect(reverse('session1'))


@api_view(["POST"])
def CalcTest(x1):
    try:
        x=json.loads(x1.body.decode('utf-8'))
        y=str(x*100)
        return JsonResponse("result:"+y,safe=False)
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)

def ResetData(request):
    os.chdir(os.path.abspath(''))
    command = 'rm db.sqlite3'
    command = command.split()
 
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    p.communicate()

    command = 'python manage.py migrate'
    command = command.split()

    p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    p.communicate()

    data = {'client': 'black', 'x': 'J', 'y':10 }
    requests.post('http://turnincode.cafe24.com:8000/home/omok/', data=data)

    return HttpResponse()

class OmokViewSet(viewsets.ModelViewSet):
        queryset = Stones.objects.all()
        serializer_class = OmokSerializer



