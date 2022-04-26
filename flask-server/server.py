from flask import Flask,render_template
from flask_restful import Api
from dotenv import load_dotenv
import os,pickle,json

from numpy import require

from data import encryptedData

load_dotenv()

app = Flask(__name__)

app.config["FLASK_ENV"] = os.getenv("FLASK_ENV")
app.config["FLASK_APP"] = os.getenv("FLASK_APP")

api = Api(app, prefix="/api/v1/")



api.add_resource(encryptedData.Data,"addResources/<string:address>")

@app.route('/')

def index():

    loaded_dict = json.loads(pickle.load(open('dictionary.pkl', 'rb')))
    
    return render_template("index.html",data=loaded_dict)

