#from marshmallow import Schema, fields
from webargs import fields
from webargs.flaskparser import parser
from flask_restful import Resource
from flask import request
import pickle


class Data(Resource):

    def post(self,address):
        enkData = request.form['resources']
        
        with open('dictionary.pkl','wb') as f:
            pickle.dump(enkData,f)

        return {},200