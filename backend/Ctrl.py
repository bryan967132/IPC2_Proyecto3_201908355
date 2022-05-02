import json

class Archivo:
    def __init__(self,nombre,ruta):
        self.nombre = nombre
        self.ruta = ruta

class Ctrl:
    def __init__(self):
        self.archivos = []

    def upload(self,ruta):
        return json.dumps({'response':ruta})