import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8').decode('utf8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='    ')

lista_respuestas = ET.Element('lista_respuestas')

respuesta = ET.SubElement(lista_respuestas,'respuesta')

ET.SubElement(respuesta,'fecha').text = ' 01/04/2022 '

mensajes = ET.SubElement(respuesta,'mensajes')
ET.SubElement(mensajes,'total').text = ' 3 '
ET.SubElement(mensajes,'positivos').text = ' 1 '
ET.SubElement(mensajes,'negativos').text = ' 1 '
ET.SubElement(mensajes,'neutros').text = ' 1 '

analisis = ET.SubElement(respuesta,'analisis')
empresa = ET.SubElement(analisis,'empresa',nombre = 'USAC')

mensajes = ET.SubElement(empresa,'mensajes')
ET.SubElement(mensajes,'total').text = ' 3 '
ET.SubElement(mensajes,'positivos').text = ' 1 '
ET.SubElement(mensajes,'negativos').text = ' 1 '
ET.SubElement(mensajes,'neutros').text = ' 1 '

servicios = ET.SubElement(empresa,'servicios')
servicio = ET.SubElement(servicios,'servicio',nombre = 'inscripción')

mensajes = ET.SubElement(servicio,'mensajes')
ET.SubElement(mensajes,'total').text = ' 3 '
ET.SubElement(mensajes,'positivos').text = ' 1 '
ET.SubElement(mensajes,'negativos').text = ' 1 '
ET.SubElement(mensajes,'neutros').text = ' 1 '

#print (ET.tostring(prtg))
print(prettify(lista_respuestas))
