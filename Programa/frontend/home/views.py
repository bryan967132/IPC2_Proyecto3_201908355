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
    if requests.method == 'POST' and 'btnEnsy' in requests.POST:
        req.get('http://127.0.0.1:3000/ensayo')
    if requests.method == 'POST' and 'btnDgrm' in requests.POST:
        req.get('http://127.0.0.1:3000/diagrama')
    if requests.method == 'POST' and 'btnClsfc' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        return render(requests,'home/clasificacionfecha.html',{'status':'working','fechas':fechas,'empresas':empresas})
    if requests.method == 'POST' and 'consult1' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        fechaR = requests.POST.get('fechasS')
        empresaR = requests.POST.get('empresasS')
        if fechaR is not None:
            dataFechaEmpresa = json.loads(req.post('http://127.0.0.1:3000/getDateCant',json = {'fecha':fechaR,'empresa':empresaR}).text)
            req.get('http://127.0.0.1:3000/graphDateCant',json = dataFechaEmpresa)
        return render(requests,'home/clasificacionfecha.html',{'status':'working','fechas':fechas,'empresas':empresas}) 
    if requests.method == 'POST' and 'btnRango' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        return render(requests,'home/clasificacionrangofecha.html',{'status':'working','fechas':fechas,'empresas':empresas,'graficasgeneradas':0})
    if requests.method == 'POST' and 'consult2' in requests.POST:
        fechas = json.loads(req.get('http://127.0.0.1:3000/date').text)['fechas']
        empresas = json.loads(req.get('http://127.0.0.1:3000/enterprise').text)['empresas']
        fechaInicial = requests.POST.get('fechas1S')
        fechaFinal = requests.POST.get('fechas2S')
        empresaR = requests.POST.get('empresasS')
        cantidadImg = []
        if fechaInicial is not None and fechaFinal is not None:
            dataRangoFechasEmpresa = json.loads(req.post('http://127.0.0.1:3000/getRangeDateCant',json = {'fechaInicio':fechaInicial,'fechaFinal':fechaFinal,'empresa':empresaR}).text)
            try:
                cantImg = json.loads(req.get('http://127.0.0.1:3000/graphRangeDateCant',json = dataRangoFechasEmpresa).text)
                cantidadImg = cantImg['imagenesgeneradas']
            except:
                pass
        return render(requests,'home/clasificacionrangofecha.html',{'status':'working','fechas':fechas,'empresas':empresas,'cantimg':cantidadImg}) 
    return render(requests,'home/index.html',{'status':'working','enter':enter,'out':out})

def upload(requests):
    rutaF = requests.POST.get('fileup')
    if rutaF is not None:
        entrada = req.post('http://127.0.0.1:3000/xml',json = {"ruta":rutaF}).text
        salida = req.get('http://127.0.0.1:3000/xml').text
        if entrada.strip() != '':
            Archivo.objects.create(root = rutaF,content = entrada,response = salida)