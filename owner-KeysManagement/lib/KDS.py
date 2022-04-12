import networkx as nx
import secrets
import hashlib
from os.path import exists

class KDS():

    def __init__(self, _graphName = "../test.gml"):
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
                key= secrets.token_hex(32),
                tag=secrets.token_hex(5)
            )

        #AGGIUNGI LA CIFRATURA DELLA RISORSA E CARICA NEL DATA MARKET

    def save(self,_path="../test.gml"):
        nx.write_gml(self.G,_path)