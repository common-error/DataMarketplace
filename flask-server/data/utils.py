from email.policy import default
from webargs.flaskparser import parser
from flask_restful import reqparse
from flask_restful import Resource
from flask import request
import pickle,json,os


class Data(Resource):

    def post(self,address):
        enkData = request.form['resources']
        
        if os.path.exists('dictionary.pkl'):
            loaded_dict = ""
            with open('dictionary.pkl', 'rb') as f:
                loaded_dict = pickle.load(f)

            with open('dictionary.pkl','wb') as f:
                combined_data = loaded_dict[:-1]+','+enkData[1:]
                pickle.dump(combined_data,f)
        else:
            with open('dictionary.pkl','wb') as f:
                pickle.dump(enkData,f)

        return "{} resources added!".format(len(json.loads(enkData))),200

class Contract(Resource):

    def post(self,address):
        contractAddress = request.form['contractAddress']
        dataToSave = json.dumps({
            "address":contractAddress
        })
        with open('contractAddress.pkl','wb') as f:
                pickle.dump(dataToSave,f)


class Mapping(Resource):

    def post(self,address):

        dataToSave = json.dumps({
            "address":request.form['map']
        })
        with open('mapping.pkl','wb') as f:
                pickle.dump(dataToSave,f)

class Graph(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('node',type=str,default='')
        super(Graph,self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        return args,201

    def post(self):
        with open('graph.json','w') as f:
            json.dump(request.form['graph'],f)