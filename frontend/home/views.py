from django.shortcuts import render
from .models import Archivo
import requests as req
import json

# Create your views here.

def home(requests):
    enter = ''
    if requests.method == 'POST' and 'btnSend' in requests.POST:
        try:
            upload(requests)
        except:
            pass
        try:
            enter = sendXml()
        except:
            pass
    if requests.method == 'POST' and  'btnReset' in requests.POST:
            Archivo.objects.all().delete()
    return render(requests,'home/index.html',{'status':'working','enter':enter})

def upload(requests):
    rutaF = requests.POST.get('fileup')
    if rutaF != 'None':
        contenido = json.loads(req.post('http://127.0.0.1:3000/xml',json = {"ruta":rutaF}).text)
        Archivo.objects.create(root = rutaF,content = contenido['content'],parsed = contenido['parsed'])
    print('PASA DEL IF')

def sendXml():
    enter = ''
    rutaF = Archivo.objects.last()
    print(rutaF)
    if rutaF:
        enter = rutaF.content
    return enter