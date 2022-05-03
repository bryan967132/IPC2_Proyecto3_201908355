from django.shortcuts import render
from .models import Archivo
import requests as req
import json

# Create your views here.

def home(requests):
    enter = ''
    if requests.method == 'POST' and 'btnCarga' in requests.POST:
        rutaF = requests.POST.get('fileup')
        if rutaF != '':
            contenido = json.loads(req.post('http://127.0.0.1:3000/xml',json = {"ruta":rutaF}).text)
            Archivo.objects.create(root = rutaF,content = contenido['response'])
    if requests.method == 'POST' and 'btnSend' in requests.POST:
            rutaF = Archivo.objects.last()
            if rutaF:
                enter = rutaF.content
    if requests.method == 'POST' and  'btnReset' in requests.POST:
            Archivo.objects.all().delete()
    return render(requests,'home/index.html',{'status':'working','enter':enter})