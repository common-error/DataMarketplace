from email.policy import default
from webargs.flaskparser import parser
from flask_restful import reqparse
from flask_restful import Resource
from flask import request
import pickle,json,os


class Data(Resource):

    def __init__(self,_path):
        self.path = _path

    def post(self,address):
        enkData = request.form['resources']
        
        if os.path.exists(self.path):
            loaded_dict = ""
            with open(self.path, 'rb') as f:
                loaded_dict = pickle.load(f)

            with open(self.path,'wb') as f:
                combined_data = loaded_dict[:-1]+','+enkData[1:]
                pickle.dump(combined_data,f)
        else:
            with open(self.path,'wb') as f:
                pickle.dump(enkData,f)

        return "{} resources added!".format(len(json.loads(enkData))),200

class Contract(Resource):
    def __init__(self,_path):
        self.path = _path

    def post(self):
        contractAddress = request.form['contractAddress']
        dataToSave = json.dumps({
            "address":contractAddress
        })
        with open(self.path,'wb') as f:
                pickle.dump(dataToSave,f)


class Mapping(Resource):

    def __init__(self,_path):
        self.path = _path

    def post(self,address):

        dataToSave = json.dumps({
            "address":request.form['map']
        })
        with open(self.path,'wb') as f:
                pickle.dump(dataToSave,f)

class Graph(Resource):

    def __init__(self,_path):
        self.path = _path
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('node',type=str,default='',required = True)
        super(Graph,self).__init__()

    def get(self):
        args = self.reqparse.parse_args()

        print(args)
        with open(self.path,'r') as f:
            data = json.load(f)
     
        return [node for node in data['catalogue'] if node['from'] == args['node']],201

    def post(self):
        with open(self.path,'w') as f:
            f.write(json.loads(request.form['graph']))