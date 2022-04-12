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
            self.G = nx.DiGraph()


    def addResource(self,_resource):
        idResource = self._hash(_resource)
        if idResource not in self.G:
            self.G.add_node(
                idResource,
                unHashName=_resource,
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                tag=secrets.token_hex(32)
            )

        #AGGIUNGI LA CIFRATURA DELLA RISORSA E CARICA NEL DATA MARKET


    def enforcePurchase(self,_buyer,_capList):
        if _buyer not in self.G:
            self.G.add_node(
                _buyer,
                key = base64.urlsafe_b64decode(Fernet.generate_key()).hex()
            )
        """
        source,target = self.G.out_edges(_buyer)[0]
        capHash = bytearray(32)

        for el in _capList:
            capHash = self._byte_xor(capHash, self._hash(el))
            if capHash == target:


        #self.G.add_edge(_buyer,self._hash("r1"))
        """
        if self._capHash(_capList) in self.G:
            print()

    def getResourceEncKey(self,_resource):
        idResource = self._hash(_resource)
        return self.G.nodes[idResource]["key"]

    def save(self,_path=DEFAULTPATH):
        nx.write_gml(self.G,_path)
    
    def _byte_xor(self,ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    def _hash(self,_data):
        return hashlib.sha3_256(_data.encode('utf-8')).hexdigest()

    def _capHash(self,_data):
        tempHash = bytearray(32)
        for el in _data:
            tempHash = self._byte_xor(tempHash, self._hash(el))
        
        return tempHash