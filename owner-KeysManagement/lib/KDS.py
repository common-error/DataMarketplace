from tkinter import N
import networkx as nx
import secrets
import hashlib
from os.path import exists
from cryptography.fernet import Fernet
import base64
from itertools import combinations
import matplotlib.pyplot as plt
import pydot 
from networkx.drawing.nx_pydot import graphviz_layout
from numpy import byte
import scipy as sp

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
                tag=secrets.token_hex(32),
                elements = [self._hash(_resource)]
            )


    def enforcePurchase(self,_buyer,_name,_capList):
        if _buyer not in self.G:
            self.G.add_node(
                _buyer,
                unHashName=_name,
                key = base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = True
            )
        
        oldCap,R = self._previousState(_buyer,_capList)

        n_cap_u = (self._capHash(oldCap)).hex()
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
        
        n_cap_u = (self._capHash(_capList)).hex()
        if n_cap_u in self.G:
            self.G.add_edge(_buyer,n_cap_u)
        else:
            self.G.add_node(
                n_cap_u,
                unHashName=','.join(_capList),
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = False,
                tag=secrets.token_hex(32),
                elements = [self._hash(el) for el in _capList]
            )
            self.G.add_edge(_buyer,n_cap_u)

            Desc = self._findDesc(_capList)
            Cover = self._greedySetCover(_capList,Desc)
            for el in Cover:
                self.G.add_edge(n_cap_u, el)
            
            Par = self._getPar(_capList,n_cap_u)
            notFlattenedDescCover = [list(nx.descendants(self.G,node)) for node in Desc] 
            DescCover =  [item for sublist in notFlattenedDescCover for item in sublist]
            DescCover = list(set(DescCover))
                                    
            for n_par in Par:
                ToRemove = []
                for n in list(set(DescCover) | set(Cover)):
                    if self.G.has_edge(n_par,n):
                        ToRemove = list(set(ToRemove) | set([(n_par,n)]))
                if len(ToRemove) >= 2:
                    self.G.add_edge(n_par,n_cap_u)
                    for n_par,n_z in ToRemove:
                        self.G.remove_edge(n_par,n_z)


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
    
    #il buyer sarà sempre connesso solo ad un nodo
    def _previousState(self,_buyer,_capList):
        edge = [to for frm,to in list(self.G.out_edges(_buyer))]
        if len(edge) == 1:
            target = edge[0]
            capHash = bytearray(32) 

            for idx,el in enumerate(_capList):
                capHash = self._byte_xor(capHash, bytes.fromhex(self._hash(el)))
                if capHash == target:
                    return (_capList[:idx+1],_capList[idx:])

        return ([],_capList)

    def _findDesc(self, _capList):
        comb = [list(combinations(_capList,size)) for size in range(len(_capList))]
        flattenedComb = [item for sublist in comb for item in sublist]
        flattenedComb = flattenedComb[1::]
        hashedComb = [(self._capHash(el)).hex() for el in flattenedComb]

        potentialSubset = self._potentialSubset(_capList)

        temp = set(potentialSubset) - set(hashedComb)
        return list(set(potentialSubset) - temp)
    

    def _potentialSubset(self, _capList):
        capHashes = [self._hash(el) for el in _capList]

        ancestors = [list(nx.ancestors(self.G,el)) for el in capHashes]
        flattenedAnc = [item for sublist in ancestors for item in sublist]
        
        return list(set(flattenedAnc) | set(capHashes))
    
    def _greedySetCover(self,_capList,_desc):
        capHashes = [self._hash(el) for el in _capList]
        DescCover = []

        while len(capHashes) != 0:
            value = 0
            maxSetRoundCover = []
            maxSetNode = []
            for el in _desc:
                if len(tmp := list(set(self.G.nodes[el]["elements"]) & set(capHashes))) > value: 
                    value = len(tmp)
                    maxSetRoundCover = tmp
                    maxSetNode = [el]
            capHashes = list(set(capHashes)-set(maxSetRoundCover))
            DescCover = list(set(DescCover)| set(maxSetNode))
        
        return DescCover

    def _getPar(self,_capList,_currentNode):
        capHashes = set([self._hash(el) for el in _capList])
        Par = []

        nodes = [x for x,y in self.G.nodes(data = True) if y['user']==0 and x != _currentNode]
        for node in nodes:
            if set(self.G.nodes[node]["elements"]).issuperset(capHashes):
                Par = list(set(Par) | set([node]))
        
        return Par

    def show(self):
        #pos = graphviz_layout(self.G,prog="dot")
        pos = nx.spring_layout(self.G, k=0.15, iterations=20)
        labels = nx.get_node_attributes(self.G, 'unHashName') 
        nx.draw(self.G,pos,with_labels = True,labels=labels)
        #nx.draw(self.G,pos)
        #nx.draw_circular(self.G,with_labels = True,labels=labels)
        #nx.draw_kamada_kawai(self.G,with_labels = True,labels=labels)
        #nx.draw_planar(self.G,with_labels = True,labels=labels)
        plt.show() 