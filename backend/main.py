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
    return #ctrl.analize(data)

if __name__ == '__main__':
    app.run(port = 3000,debug = True)