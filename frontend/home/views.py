import os
import webbrowser
from django.shortcuts import render
from .models import Archivo
import requests as req
import json

# Create your views here.

def home(requests):
    enter = ''
    out = ''
    if requests.method == 'POST' and 'btnSend' in requests.POST:
        try:
            upload(requests)
        except:
            pass
        try:
            enter = Archivo.objects.last().content
        except:
            pass
    if requests.method == 'POST' and  'btnReset' in requests.POST:
        Archivo.objects.all().delete()
        req.delete('http://127.0.0.1:3000/reset')
    if requests.method == 'POST' and 'btnCnslt' in requests.POST:
        try:
            enter = Archivo.objects.last().content
            out = Archivo.objects.last().response
        except:
            pass
    if requests.method == 'POST' and 'btnDcmnt' in requests.POST:
        #webbrowser.open('../../Ensayo.pdf')
        pass
    if requests.method == 'POST' and 'btnClsfc' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        return render(requests,'home/clasificacionfecha.html',{'status':'working','fechas':fechas,'empresas':empresas})    
    if requests.method == 'POST' and 'consult' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        fechaR = requests.POST.get('fechasS')
        empresaR = requests.POST.get('empresasS')
        if fechaR is not None:
            req.post('http://127.0.0.1:3000/dateEnterprise',json = {'fecha':fechaR,'empresa':empresaR})
        return render(requests,'home/clasificacionfecha.html',{'status':'working','fechas':fechas,'empresas':empresas}) 
    return render(requests,'home/index.html',{'status':'working','enter':enter,'out':out})

def upload(requests):
    rutaF = requests.POST.get('fileup')
    if rutaF is not None:
        entrada = req.post('http://127.0.0.1:3000/xml',json = {"ruta":rutaF}).text
        salida = req.get('http://127.0.0.1:3000/xml').text
        if entrada.strip() != '':
            Archivo.objects.create(root = rutaF,content = entrada,response = salida)