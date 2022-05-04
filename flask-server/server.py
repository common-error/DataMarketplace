from flask import Flask,render_template
from flask_restful import Api
from dotenv import load_dotenv
from collections import defaultdict
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
    loaded_CtcAddress = {}
    distinct_el = {}

    if os.path.exists('dictionary.pkl'):
        loaded_dict = json.loads(pickle.load(open('dictionary.pkl', 'rb')))

        temp_dict = defaultdict(set)
        for item in loaded_dict:
            for key,value in item["metadata"].items():
                temp_dict[key].add(value)

        
        for key,value in temp_dict.items():
            distinct_el[key] = list(value)

    if os.path.exists('contractAddress.pkl'):
        loaded_CtcAddress = json.loads(pickle.load(open('contractAddress.pkl', 'rb')))
   


    return render_template("index.html",data=distinct_el,addrs=loaded_CtcAddress)
