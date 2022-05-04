from ParserXML import Parser
import re
class Ctrl:
    def upload(self,ruta : str):
        try:
            self.parser = Parser()
            self.fechas = self.parser.fechas
            self.parsed = self.parser.parseXMLtoJSON(f'../{ruta}')
            contenido = open(f'../{ruta}',encoding = 'utf-8').read()
            return contenido
        except:
            return ''

    def analize(self):
        msg_fecha_general = self.countGeneral()
        return self.parser.parseJSONtoXML(msg_fecha_general)
    
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