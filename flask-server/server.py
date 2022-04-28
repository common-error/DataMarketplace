from flask import Flask,render_template
from flask_restful import Api
from dotenv import load_dotenv
import os,pickle,json

from numpy import require

from data import utils

load_dotenv()

app = Flask(__name__)

app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
app.config["FLASK_APP"] = os.getenv("FLASK_APP")

api = Api(app, prefix="/api/v1/")



api.add_resource(utils.Data,"addResources/<string:address>")
api.add_resource(utils.Contract,"addContract/<string:address>")

@app.route('/')

def index():
    if os.path.exists('dictionary.pkl'):
        if os.path.exists('contractAddress.pkl'):
            loaded_CtcAddress = json.loads(pickle.load(open('contractAddress.pkl', 'rb')))
            loaded_dict = json.loads(pickle.load(open('dictionary.pkl', 'rb')))


            return render_template("index.html",data=loaded_dict,addrs=loaded_CtcAddress)
        else:
            return render_template("index.html",data={"error":"Contract not deployed!"})
    else:
        return render_template("index.html",data={"error":"File not found!"})

