import os
import matplotlib.pyplot as plotpy
from datetime import datetime
from ParserXML import Parser
import pandas as pd
import datetime as dtime
import re
class Ctrl:
    def upload(self,ruta : str):
        try:
            self.parser = Parser()
            self.parsed = self.parser.parseXMLtoJSON(f'../{ruta}')
            self.fechas = self.parser.fechas
            self.fechas.sort(key = lambda date : datetime.strptime(date,'%d/%m/%Y'))
            self.empresas = self.parser.empresas
            contenido = open(f'../{ruta}',encoding = 'utf-8').read()
            return contenido
        except:
            return ''

    def analize(self):
        self.msg_fecha_general = self.countGeneral()
        return self.parser.parseJSONtoXML(self.msg_fecha_general)
    
    def countGeneral(self):
        msg_fecha_general = []
        for fecha in self.fechas:
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
            msg_fecha_general.append({fecha:{'total':pos + neg + neut,'positivos':pos,'negativos':neg,'neutros':neut,'analisis':self.countByDate(fecha)}})
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
            msg_analize_empresa.append({'empresa':empresa['nombre'],'total':pos + neg + neut,'positivos':pos,'negativos':neg,'neutros':neut,'servicios':self.countByService(empresa,fecha)})
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
            msg_analize_servicio.append({'servicio':servicio['nombre'],'total':pos + neg + neut,'positivos':pos,'negativos':neg,'neutros':neut})
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
    
    def reset(self):
        try:
            del self.fechas
            del self.empresas
        except:
            pass
        if os.path.exists('../frontend/home/static/images/Grafica.png'):
            os.remove('../frontend/home/static/images/Grafica.png')
        try:
            for i in range(1,self.contador + 1):
                if os.path.exists(f'../frontend/home/static/images/Grafica{i}.png'):
                    os.remove(f'../frontend/home/static/images/Grafica{i}.png')
        except:
            pass
        return {'status':'reseted'}

    def getDateEnt(self,fechaR,empresaR):
        try:
            total = 0
            positivos = 0
            negativos = 0
            neutros = 0
            for fecha in self.msg_fecha_general:
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
            nombre = [f'Positivos: {positivos}',f'Negativos: {negativos}',f'Neutros: {neutros}']
            vend = [positivos,negativos,neutros]
            fig, ax = plotpy.subplots()
            fig.canvas.manager.set_window_title('Grafica') 
            ax.pie(vend,autopct = "%0.1f%%")
            ax.set_title(f'Empresa: {empresaR}\nFecha: {fechaR}\nMensajes Totales: {total}')
            ax.legend(nombre,loc = 'upper left')
            ax.grid(True)
            plotpy.savefig('../frontend/home/static/images/Grafica.png',dpi = 300)
            return {'status':'grafica generada'}
        except:
            return {'status':'ocurrio un error'}

    def getRangeDate(self,fechaInicio,fechaFinal,empresaR):
        self.contador = 0
        try:
            start = dtime.datetime.strptime(fechaInicio,'%d/%m/%Y')
            end = dtime.datetime.strptime(fechaFinal,'%d/%m/%Y')
            fechasGeneradas = pd.date_range(start,end)
            for fecha in self.msg_fecha_general:
                llave = list(fecha.keys())[0]
                total = 0
                positivos = 0
                negativos = 0
                neutros = 0
                if dtime.datetime.strptime(llave,'%d/%m/%Y') in fechasGeneradas:
                    self.contador += 1
                    for empresa in fecha[llave]['analisis']:
                        if empresa['empresa'] == empresaR:
                            total = empresa['total']
                            positivos = empresa['positivos']
                            negativos = empresa['negativos']
                            neutros = empresa['neutros']
                            break
                        elif empresaR == 'Todas las empresas':
                            total += empresa['total']
                            positivos += empresa['positivos']
                            negativos += empresa['negativos']
                            neutros += empresa['neutros']
                    print('FECHA:',llave)
                    print('EMPRESA:',empresaR)
                    print('TOTAL:',total)
                    print('POSITIVOS:',positivos)
                    print('NEGATIVOS:',negativos)
                    print('NEUTROS:',neutros)

                    nombre = [f'Positivos: {positivos}',f'Negativos: {negativos}',f'Neutros: {neutros}']
                    vend = [positivos,negativos,neutros]
                    fig, ax = plotpy.subplots()
                    fig.canvas.manager.set_window_title('Grafica') 
                    ax.pie(vend,autopct = "%0.1f%%")
                    ax.set_title(f'Empresa: {empresaR}\nFecha: {llave}\nMensajes Totales: {total}')
                    ax.legend(nombre,loc = 'upper left')
                    ax.grid(True)
                    plotpy.savefig(f'../frontend/home/static/images/Grafica{self.contador}.png',dpi = 300)
            return {'imagenesgeneradas':self.contador}
        except:
            return {'imagenesgeneradas':self.contador}
        