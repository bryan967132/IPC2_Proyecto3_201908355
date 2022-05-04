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
    def __init__(self,lugar : str,fecha : str,hora : str,usuario : str,red_social : str,mensaje : str):
        self.lugar = lugar
        self.fecha = fecha
        self.hora = hora
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
    def __init__(self):
        self.fechas = []

    def appendDates(self,fecha):
        if fecha not in self.fechas:
            self.fechas.append(fecha)

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
            fecha = re.findall('[0-3]?[0-9]/[0-1]?[0-9]/[0-9]*',lugar_fecha[1].strip())[0]
            hora = re.findall('[0-2]?[0-9]:[0-5]?[0-9]',lugar_fecha[1].strip())[0]
            red_social = re.findall('red social:\s+[a-z]*',campo)[0]
            campo = campo.replace(red_social,'')
            red_social = red_social.replace('red social:','')
            self.appendDates(fecha)
            mensajes.append(Mensaje(lugar_fecha[0].strip(),fecha,hora,usuario.strip(),red_social.strip(),campo.strip()).__dict__)
        return Archivo(sent_pos,sent_neg,empresas,mensajes).__dict__

class Ctrl:
    def upload(self,ruta : str):
        parser = Parser()
        self.fechas = parser.fechas
        self.parsed = parser.parseXML(f'../{ruta}')
        contenido = open(f'../{ruta}',encoding = 'utf-8').read()
        return json.dumps({'content':contenido,'parsed': self.parsed})

    def analize(self):
        self.upload('prueba.xml')
        msg_fecha_empresa = self.countGeneral()
            
        #print(msg_analize_empresa)
        return json.dumps(msg_fecha_empresa)
    
    def countGeneral(self):
        msg_fecha_general = []
        for fecha in self.fechas:
            msg_analize_general = []
            pos = 0
            neg = 0
            neut = 0
            cantmsg = 0
            for mensaje in self.parsed['mensajes']:
                if mensaje['fecha'] == fecha:
                    count = self.count(mensaje['mensaje'])
                    cantp = count[0]
                    cantn = count[1]
                    if cantp > cantn:
                        pos += 1
                    elif cantn > cantp:
                        neg += 1
                    else:
                        neut += 1
                    cantmsg += 1
            msg_analize_general.append({'positivos':pos,'negativos':neg,'neutros':neut,'analisis':self.countByDate(fecha)})
            msg_fecha_general.append({fecha:msg_analize_general})
        return msg_fecha_general
    
    def countByDate(self,fecha):
        msg_analize_empresa = []
        for empresa in self.parsed['empresas']:
            pos = 0
            neg = 0
            neut = 0
            cantmsg = 0
            for mensaje in self.parsed['mensajes']:
                if mensaje['fecha'] == fecha:
                    x = re.findall(f'\\b({empresa["nombre"]})\\b',mensaje['mensaje'])
                    if len(x) > 0:
                        count = self.count(mensaje['mensaje'])
                        cantp = count[0]
                        cantn = count[1]
                        if cantp > cantn:
                            pos += 1
                        elif cantn > cantp:
                            neg += 1
                        else:
                            neut += 1
                        cantmsg += 1
            msg_analize_empresa.append({'empresa':empresa['nombre'],'positivos':pos,'negativos':neg,'neutros':neut,'servicios':self.countByService(empresa,fecha)})
        return msg_analize_empresa
        
    def countByService(self,empresa,fecha):
        msg_analize_servicio = []
        for servicio in empresa['servicios']:
            pos = 0
            neg = 0
            neut = 0
            cantmsg = 0
            for mensaje in self.parsed['mensajes']:
                if mensaje['fecha'] == fecha:
                    x = re.findall(f'\\b({servicio["nombre"]})\\b',mensaje['mensaje'])
                    if len(x) > 0:
                        count = self.count(mensaje['mensaje'])
                        cantp = count[0]
                        cantn = count[1]
                        if cantp > cantn:
                            pos += 1
                        elif cantn > cantp:
                            neg += 1
                        else:
                            neut += 1
                        cantmsg += 1
                    else:
                        count = self.countByAlias(servicio['alias'],mensaje['mensaje'])
                        if count:
                            count = self.count(mensaje['mensaje'])
                            cantp = count[0]
                            cantn = count[1]
                            if cantp > cantn:
                                pos += 1
                            elif cantn > cantp:
                                neg += 1
                            else:
                                neut += 1
                            cantmsg += 1
            msg_analize_servicio.append({'servicio':servicio['nombre'],'positivos':pos,'negativos':neg,'neutros':neut})
        return msg_analize_servicio
                        
    
    def countByAlias(self,alias,mensaje):
        for al in alias:
            x = re.findall(f'\\b({al})\\b',mensaje)
            if len(x) > 0:
                return True
        return False
    
    def count(self,mensaje):
        cantp = 0
        cantn = 0
        for positivo in self.parsed['positivos']:  
            p = re.findall(f'\\b({positivo})\\b',mensaje)
            cantp += len(p)
        for negativo in self.parsed['negativos']:
            n = re.findall(f'\\b({negativo})\\b',mensaje)
            cantn += len(n)
        return [cantp,cantn]