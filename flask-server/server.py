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

curr_path = os.path.dirname(os.path.realpath(__file__))
paths = {
    'mapping' : curr_path+"\\runTime\\mapping.pkl",
    'dict' : curr_path+"\\runTime\\dictionary.pkl",
    'contract' :  curr_path+"\\runTime\\contractAddress.pkl",
    'graph' :  curr_path+"\\runTime\\graph.json"
}



api.add_resource(utils.Data,"addResources/<string:address>", resource_class_kwargs={'_path': paths['dict']})
api.add_resource(utils.Contract,"addContract/", resource_class_kwargs={'_path': paths['contract']})
api.add_resource(utils.Mapping,"mapping/<string:address>", resource_class_kwargs={'_path': paths['mapping']})
api.add_resource(utils.Graph,"graph/", resource_class_kwargs={'_path': paths['graph']})

@app.route('/')
def index():
    loaded_CtcAddress = {}
    distinct_el = {}
    mapping = {}

    if(os.path.exists(paths['mapping'])):
        mapping = json.loads(pickle.load(open(paths['mapping'],'rb')))

    if os.path.exists(paths['dict']):
        loaded_dict = json.loads(pickle.load(open(paths['dict'], 'rb')))

        temp_dict = defaultdict(set)
        for item in loaded_dict:
            for key,value in item["metadata"].items():
                temp_dict[key].add(value)

        
        for key,value in temp_dict.items():
            distinct_el[key] = list(value)

    if os.path.exists(paths['contract']):
        loaded_CtcAddress = json.loads(pickle.load(open(paths['contract'], 'rb')))
   


    return render_template("index.html",data=distinct_el,addrs=loaded_CtcAddress,map=mapping)
