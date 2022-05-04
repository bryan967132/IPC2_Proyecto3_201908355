from DictBuilders import *
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re
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

    def parseXMLtoJSON(self,ruta : str):
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
            usuario = re.findall('usuario:\s+[a-z0-9@.]*',campo)[0]
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
    
    def parseJSONtoXML(self,dict):
        lista_respuestas = ET.Element("lista_respuestas")
        for dictFecha in dict:
            respuesta = ET.SubElement(lista_respuestas,'respuesta')
            key = list(dictFecha.keys())[0]
            ET.SubElement(respuesta,'fecha').text = f' {key} '
            cuerpo = dictFecha[key]
            mensajes = ET.SubElement(respuesta,'mensajes')
            ET.SubElement(mensajes,'total').text = f' {cuerpo["total"]} '
            ET.SubElement(mensajes,'positivos').text = f' {cuerpo["positivos"]} '
            ET.SubElement(mensajes,'negativos').text = f' {cuerpo["negativos"]} '
            ET.SubElement(mensajes,'neutros').text = f' {cuerpo["neutros"]} '
            anls = cuerpo['analisis']
            analisis = ET.SubElement(respuesta,'analisis')
            for emprs in anls:
                empresa = ET.SubElement(analisis,'empresa',nombre = f'{emprs["empresa"]}')
                mensajes = ET.SubElement(empresa,'mensajes')
                ET.SubElement(mensajes,'total').text = f' {emprs["total"]} '
                ET.SubElement(mensajes,'positivos').text = f' {emprs["positivos"]} '
                ET.SubElement(mensajes,'negativos').text = f' {emprs["negativos"]} '
                ET.SubElement(mensajes,'neutros').text = f' {emprs["neutros"]} '
                srvs = emprs['servicios']
                servicios = ET.SubElement(empresa,'servicios')
                for srv in srvs:
                    servicio = ET.SubElement(servicios,'servicio',nombre = f'{srv["servicio"]}')
                    mensajes = ET.SubElement(servicio,'mensajes')
                    ET.SubElement(mensajes,'total').text = f' {srv["total"]} '
                    ET.SubElement(mensajes,'positivos').text = f' {srv["positivos"]} '
                    ET.SubElement(mensajes,'negativos').text = f' {srv["negativos"]} '
                    ET.SubElement(mensajes,'neutros').text = f' {srv["neutros"]} '
        return self.prettify(lista_respuestas)

    def prettify(self,elem):
        rough_string = ET.tostring(elem, 'utf-8').decode('utf8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")