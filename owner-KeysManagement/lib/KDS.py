import networkx as nx
import secrets
import hashlib
from os.path import exists
from cryptography.fernet import Fernet
import base64

DEFAULTPATH = "../KDS.gml"

class KDS():

    def __init__(self, _graphName = DEFAULTPATH):
        if(exists(_graphName)):
            self.G = nx.read_gml(_graphName)
        else:
            self.G = nx.Graph()


    def addResource(self,_resource):
        idResource = hashlib.sha3_256(_resource.encode('utf-8')).hexdigest()
        if idResource not in self.G:
            self.G.add_node(
                idResource,
                unHashName=_resource,
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                tag=secrets.token_hex(32)
            )

        #AGGIUNGI LA CIFRATURA DELLA RISORSA E CARICA NEL DATA MARKET
    def getResourceEncKey(self,_resource):
        idResource = hashlib.sha3_256(_resource.encode('utf-8')).hexdigest()
        return self.G.nodes[idResource]["key"]

    def save(self,_path=DEFAULTPATH):
        nx.write_gml(self.G,_path)