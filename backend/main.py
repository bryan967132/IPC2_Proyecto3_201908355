from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/',methods = ['GET'])
def home():
    return 'Servidor funcionando'

if __name__ == '__main__':
    app.run(port = 3000,debug = True)