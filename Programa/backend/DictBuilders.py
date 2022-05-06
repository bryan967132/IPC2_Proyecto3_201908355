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