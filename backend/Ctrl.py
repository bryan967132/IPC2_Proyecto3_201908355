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
    def __init__(self,mensaje : str):
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
            mensajes.append(Mensaje(self.deleteChar(mensaje.firstChild.data.strip())).__dict__)
            
        return Archivo(sent_pos,sent_neg,empresas,mensajes).__dict__

class Ctrl:
    def __init__(self):
        self.archivos = []

    def upload(self,ruta : str):
        try:
            self.parsed = Parser().parseXML(f'../{ruta}')
            contenido = open(f'../{ruta}',encoding = 'utf-8').read()
            return json.dumps({'response':contenido})
        except:
            return json.dumps({'response':''})
    
    def analize(self):
        self.parsed['positivos']
        self.parsed['negativos']
        return {'response':'resultado'}