#from marshmallow import Schema, fields
from webargs import fields
from webargs.flaskparser import parser
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