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
    def parseXML(self,ruta : str):
        myDoc = minidom.parse(ruta)

        sent_pos = []
        etiquetas = myDoc.getElementsByTagName('sentimientos_positivos')
        for positivos in etiquetas:
            for palabra in positivos.getElementsByTagName('palabra'):
                sent_pos.append(palabra.firstChild.data.strip())

        sent_neg = []
        etiquetas = myDoc.getElementsByTagName('sentimientos_negativos')
        for negativos in etiquetas:
            for palabra in negativos.getElementsByTagName('palabra'):
                sent_neg.append(palabra.firstChild.data.strip())

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
                    alias.append(al.firstChild.data.strip())
                servicios.append(Servicio(nomServ,alias).__dict__)
            empresas.append(Empresa(nombre,servicios).__dict__)
        
        mensajes = []
        etiquetas = myDoc.getElementsByTagName('mensaje')
        for mensaje in etiquetas:
            mensajes.append(Mensaje(mensaje.firstChild.data.strip()).__dict__)
            
        return Archivo(sent_pos,sent_neg,empresas,mensajes).__dict__

class Ctrl:
    def __init__(self):
        self.archivos = []

    def upload(self,ruta : str):
        self.parsed = Parser().parseXML(ruta)
        contenido = open(ruta).read()
        return json.dumps({'response':contenido})