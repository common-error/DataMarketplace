from tkinter import N
import networkx as nx
import secrets
import hashlib
from os.path import exists
from cryptography.fernet import Fernet
import base64
from itertools import combinations

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
                user = False,
                tag=secrets.token_hex(32)
            )


    def enforcePurchase(self,_buyer,_capList):
        if _buyer not in self.G:
            self.G.add_node(
                _buyer,
                key = base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = True
            )
        
        oldCap,R = self._previousState(_buyer,_capList)

        n_cap_u = self._capHash(oldCap)
        if  n_cap_u in self.G:
            self.G.remove_edge(_buyer,n_cap_u)
            if not self._existAnotherUser(_buyer,n_cap_u):
                par = [fr[0] for fr in self.G.in_edges(n_cap_u)]
                desc = [to[0] for to in self.G.out_edges(n_cap_u)]
                if (len(par) * len(desc)) < (len(par) + len(desc)):
                    for n_par in par:
                        self.G.remove_edge(n_par, n_cap_u)
                        for n_desc in desc:
                            self.G.remove_edge(n_cap_u, n_desc)
                            self.G.add_edge(n_par, n_desc)
                    self.G.remove_node(n_cap_u)
        
        n_cap_u = self._capHash(_capList)
        if n_cap_u in self.G:
            self.G.add_edge(_buyer,n_cap_u)
        else:
            self.G.add_node(
                n_cap_u,
                unHashName=','.join(_capList),
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = False,
                tag=secrets.token_hex(32)
            )
            self.G.add_edge(_buyer,n_cap_u)

            Desc = self._findDesc(_capList)

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
            tempHash = self._byte_xor(tempHash, hashlib.sha3_256(el.encode('utf-8')).digest())
        
        return tempHash
    
    def _existAnotherUser(self,_buyer,_node):
        for fr,to in self.G.in_edges(_node):
            if self.G.nodes[fr]["user"] and fr != _buyer:
                return True
            
        return False
    
    def _previousState(self,_buyer,_capList):
        source,target = self.G.out_edges(_buyer)[0]

        for idx,el in enumerate(_capList):
            capHash = self._byte_xor(capHash, self._hash(el))
            if capHash == target:
                return (_capList[:idx+1],_capList[idx:])

        return ([],_capList)

    def _findDesc(self, _capList):
        comb = [list(combinations(_capList,size)) for size in range(len(_capList))]
        flattenedComb = [item for sublist in comb for item in sublist]
        flattenedComb = flattenedComb[1::]
        hashedComb = [self._capHash(el) for el in flattenedComb]

        potentialSubset = self._potentialSubset(_capList)

        temp = set(potentialSubset) - set(hashedComb)
        return list(set(potentialSubset) - temp)
    
    def _findDescCover(self,_Desc,_n_cap_u):
        print()

    def _potentialSubset(self, _capList):
        capHashes = [self._hash(el) for el in _capList]

        ancestors = [list(nx.ancestors(self.G,el)) for el in capHashes]
        flattenedAnc = [item for sublist in ancestors for item in sublist]
        
        return list(set(flattenedAnc)) + capHashes
