import webbrowser
from flask import Flask,request
from flask_cors import CORS
from Ctrl import Ctrl

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

ctrl = Ctrl()

@app.route('/',methods = ['GET'])
def home():
    return 'Servidor funcionando'

@app.route('/xml',methods = ['POST'])
def upload():
    data = request.json
    return ctrl.upload(data['ruta'])

@app.route('/xml',methods = ['GET'])
def analize():
    return ctrl.analize()

@app.route('/date',methods = ['GET'])
def getDates():
    try:
        return {'fechas':ctrl.fechas}
    except:
        return {'fechas':[]}

@app.route('/enterprise',methods = ['GET'])
def getEnterprises():
    try:
        return {'empresas':ctrl.empresas}
    except:
        return {'empresas':[]}

@app.route('/reset',methods = ['DELETE'])
def reset():
    ctrl.reset()
    return {'status':'reseted'}

@app.route('/getDateCant',methods = ['POST'])
def getDateCant():
    data = request.json
    return ctrl.getDateCant(data['fecha'],data['empresa'])

@app.route('/getRangeDateCant',methods = ['POST'])
def getRangeDateCant():
    data = request.json
    return ctrl.getRangeDateCant(data['fechaInicio'],data['fechaFinal'],data['empresa'])

@app.route('/graphDateCant',methods = ['GET'])
def graphDateCant():
    data = request.json
    return ctrl.graphDateCant(
        data['fecha'],
        data['empresa'],
        data['total'],
        data['positivos'],
        data['negativos'],
        data['neutros']
    )

@app.route('/graphRangeDateCant',methods = ['GET'])
def graphRangeDateCant():
    return ctrl.graphRangeDateCant(request.json)
    
@app.route('/ensayo',methods = ['GET'])
def ensayo():
    webbrowser.open('../../Documentacion/Ensayo.pdf')
    return {'status':'abierto'}

@app.route('/diagrama',methods = ['GET'])
def diagrama():
    webbrowser.open('../../Documentacion/DiagramaProyecto3.pdf')
    return {'status':'abierto'}

if __name__ == '__main__':
    app.run(port = 3000,debug = True)