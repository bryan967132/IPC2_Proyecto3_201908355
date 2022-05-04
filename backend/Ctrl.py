from datetime import date
from flask import jsonify
from xml.dom import minidom
import json
import re

class MArchivo:
    def __init__(self,nombre : str,ruta : str):
        self.nombre = nombre
        self.ruta = ruta

class Empresa:
    def __init__(self,nombre : str,servicios : list):
        self.nombre = nombre
        self.servicios = servicios

class Servicio:
    def __init__(self,nombre : str,alias : list):
        self.nombre = nombre
        self.alias = alias

class Mensaje:
    def __init__(self,lugar : str,fecha : str,usuario : str,red_social : str,mensaje : str):
        self.lugar = lugar
        self.fecha = fecha
        self.usuario = usuario
        self.red_social = red_social
        self.mensaje = mensaje

class Archivo:
    def __init__(self,positivos,negativos,empresas,mensajes):
        self.positivos = positivos
        self.negativos = negativos
        self.empresas = empresas
        self.mensajes = mensajes

class Parser:
    def deleteChar(self,texto):
        texto = texto.lower()
        vocales = [{'á':'a'},{'é':'e'},{'í':'i'},{'ó':'o'},{'ú':'u'}]
        for par in vocales:
            for k in par:
                texto = texto.replace(k,par[k])
        return texto

    def parseXML(self,ruta : str):
        myDoc = minidom.parse(ruta)

        sent_pos = []
        etiquetas = myDoc.getElementsByTagName('sentimientos_positivos')
        for positivos in etiquetas:
            for palabra in positivos.getElementsByTagName('palabra'):
                sent_pos.append(self.deleteChar(palabra.firstChild.data.strip()))

        sent_neg = []
        etiquetas = myDoc.getElementsByTagName('sentimientos_negativos')
        for negativos in etiquetas:
            for palabra in negativos.getElementsByTagName('palabra'):
                sent_neg.append(self.deleteChar(palabra.firstChild.data.strip()))

        empresas = []
        etiquetas = myDoc.getElementsByTagName('empresa')
        for empresa in etiquetas:
            for nom in empresa.getElementsByTagName('nombre'):
                nombre = nom.firstChild.data.strip()
            servicios = []
            for servicio in empresa.getElementsByTagName('servicio'):
                nomServ = servicio.attributes['nombre'].value.strip()
                alias = []
                for al in servicio.getElementsByTagName('alias'):
                    alias.append(self.deleteChar(al.firstChild.data.strip()))
                servicios.append(Servicio(self.deleteChar(nomServ),alias).__dict__)
            empresas.append(Empresa(self.deleteChar(nombre),servicios).__dict__)
        
        mensajes = []
        etiquetas = myDoc.getElementsByTagName('mensaje')
        for mensaje in etiquetas:
            campo = self.deleteChar(mensaje.firstChild.data.replace('\n','').strip())
            usuario = re.findall('usuario:\s+[a-z0-9]*@[a-z]*.[a-z]*',campo)[0]
            campo = campo.replace(usuario,'')
            usuario = usuario.replace('usuario:','')
            lugar_fecha = re.findall('lugar y fecha:\s+[a-z0-9]*,\s+[0-3]?[0-9]/[0-1]?[0-9]/[0-9]*\s+[0-2]?[0-9]:[0-5]?[0-9]',campo)[0]
            campo = campo.replace(lugar_fecha,'')
            lugar_fecha = lugar_fecha.replace('lugar y fecha:','').split(',')
            red_social = re.findall('red social:\s+[a-z]*',campo)[0]
            campo = campo.replace(red_social,'')
            red_social = red_social.replace('red social:','')
            mensajes.append(Mensaje(lugar_fecha[0].strip(),lugar_fecha[1].strip(),usuario.strip(),red_social.strip(),campo.strip()).__dict__)
            
        return Archivo(sent_pos,sent_neg,empresas,mensajes).__dict__

class Ctrl:
    def __init__(self):
        self.archivos = []

    def upload(self,ruta : str):
        self.parsed = Parser().parseXML(f'../{ruta}')
        contenido = open(f'../{ruta}',encoding = 'utf-8').read()
        return json.dumps({'content':contenido,'parsed': self.parsed})
    
    def analize(self):
        return self.temporal