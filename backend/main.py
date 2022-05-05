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

@app.route('/dateEnterprise',methods = ['POST'])
def getDateEnterprise():
    data = request.json
    print(data)
    return ctrl.graph(data['fecha'],data['empresa'])

if __name__ == '__main__':
    app.run(port = 3000,debug = True)