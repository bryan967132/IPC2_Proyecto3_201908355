import webbrowser
import matplotlib.pyplot as plotpy
from matplotlib import colors


diccionario = [
    {
        "03/05/2021": {
            "total": 1,
            "positivos": 0,
            "negativos": 1,
            "neutros": 0,
            "analisis": [
                {
                    "empresa": "usac",
                    "total": 1,
                    "positivos": 0,
                    "negativos": 1,
                    "neutros": 0,
                    "servicios": [
                        {
                            "servicio": "inscripcion",
                            "total": 1,
                            "positivos": 0,
                            "negativos": 1,
                            "neutros": 0
                        },
                        {
                            "servicio": "asignacion",
                            "total": 1,
                            "positivos": 0,
                            "negativos": 1,
                            "neutros": 0
                        },
                        {
                            "servicio": "graduacion",
                            "total": 0,
                            "positivos": 0,
                            "negativos": 0,
                            "neutros": 0
                        }
                    ]
                },
                {
                    "empresa": "irtra",
                    "total": 1,
                    "positivos": 0,
                    "negativos": 1,
                    "neutros": 0,
                    "servicios": [
                        {
                            "servicio": "inscripcion",
                            "total": 1,
                            "positivos": 0,
                            "negativos": 1,
                            "neutros": 0
                        }
                    ]
                }
            ]
        }
    },
    {
        "01/04/2022": {
            "total": 2,
            "positivos": 1,
            "negativos": 0,
            "neutros": 1,
            "analisis": [
                {
                    "empresa": "usac",
                    "total": 2,
                    "positivos": 1,
                    "negativos": 0,
                    "neutros": 1,
                    "servicios": [
                        {
                            "servicio": "inscripcion",
                            "total": 2,
                            "positivos": 1,
                            "negativos": 0,
                            "neutros": 1
                        },
                        {
                            "servicio": "asignacion",
                            "total": 1,
                            "positivos": 1,
                            "negativos": 0,
                            "neutros": 0
                        },
                        {
                            "servicio": "graduacion",
                            "total": 1,
                            "positivos": 0,
                            "negativos": 0,
                            "neutros": 1
                        }
                    ]
                },
                {
                    "empresa": "irtra",
                    "total": 1,
                    "positivos": 1,
                    "negativos": 0,
                    "neutros": 0,
                    "servicios": [
                        {
                            "servicio": "inscripcion",
                            "total": 2,
                            "positivos": 1,
                            "negativos": 0,
                            "neutros": 1
                        }
                    ]
                }
            ]
        }
    }
]

fechaR = '01/04/2022'
empresaR = 'Todas las empresas'

total = 0
positivos = 0
negativos = 0
neutros = 0

for fecha in diccionario:
    llave = list(fecha.keys())[0]
    if llave == fechaR:
        for empresa in fecha[llave]['analisis']:
            if empresa['empresa'] == empresaR:
                total = empresa['total']
                positivos = empresa['positivos']
                negativos = empresa['negativos']
                neutros = empresa['neutros']
            elif empresaR == 'Todas las empresas':
                total += empresa['total']
                positivos += empresa['positivos']
                negativos += empresa['negativos']
                neutros += empresa['neutros']

print('FECHA:',fechaR)
print('EMPRESA:',empresaR)
print('TOTAL:',total)
print('POSITIVOS:',positivos)
print('NEGATIVOS:',negativos)
print('NEUTROS:',neutros)

nombre = [f'Positivos: {positivos}',f'Negativos: {negativos}',f'Neutros: {neutros}']
vend = [positivos,negativos,neutros]  
normdata = colors.Normalize(min(vend), max(vend))
fig, ax = plotpy.subplots()
fig.canvas.manager.set_window_title('Grafica') 
ax.pie(vend,autopct = "%0.1f%%")
ax.set_title(f'Empresa: {empresaR}\nFecha: {fechaR}\nMensajes Totales: {total}')
ax.legend(nombre,loc = 'upper left')
ax.grid(True)
plotpy.savefig('frontend/home/static/images/Grafica.png',dpi = 300)

#from datetime import datetime
#
#def printDates(dates):
#    for i in range(len(dates)):   
#        print(dates[i])
#
#fechas = ['01/05/2022','12/03/2021','15/03/2021','30/04/2022','25/04/2022','25/07/2022']
#
#print('\nFECHAS DESORDENADAS')
#printDates(fechas)
#print()
#
#fechas.sort(key = lambda date: datetime.strptime(date,'%d/%m/%Y'))
#
#printDates(fechas)



#import xml.etree.ElementTree as ET
#from xml.dom import minidom
#
#def prettify(elem):
#    rough_string = ET.tostring(elem, 'utf-8').decode('utf8')
#    reparsed = minidom.parseString(rough_string)
#    return reparsed.toprettyxml(indent='    ')
#
#lista_respuestas = ET.Element('lista_respuestas')
#
#respuesta = ET.SubElement(lista_respuestas,'respuesta')
#
#ET.SubElement(respuesta,'fecha').text = ' 01/04/2022 '
#
#mensajes = ET.SubElement(respuesta,'mensajes')
#ET.SubElement(mensajes,'total').text = ' 3 '
#ET.SubElement(mensajes,'positivos').text = ' 1 '
#ET.SubElement(mensajes,'negativos').text = ' 1 '
#ET.SubElement(mensajes,'neutros').text = ' 1 '
#
#analisis = ET.SubElement(respuesta,'analisis')
#empresa = ET.SubElement(analisis,'empresa',nombre = 'USAC')
#
#mensajes = ET.SubElement(empresa,'mensajes')
#ET.SubElement(mensajes,'total').text = ' 3 '
#ET.SubElement(mensajes,'positivos').text = ' 1 '
#ET.SubElement(mensajes,'negativos').text = ' 1 '
#ET.SubElement(mensajes,'neutros').text = ' 1 '
#
#servicios = ET.SubElement(empresa,'servicios')
#servicio = ET.SubElement(servicios,'servicio',nombre = 'inscripción')
#
#mensajes = ET.SubElement(servicio,'mensajes')
#ET.SubElement(mensajes,'total').text = ' 3 '
#ET.SubElement(mensajes,'positivos').text = ' 1 '
#ET.SubElement(mensajes,'negativos').text = ' 1 '
#ET.SubElement(mensajes,'neutros').text = ' 1 '
#
#print (ET.tostring(prtg))
#print(prettify(lista_respuestas))