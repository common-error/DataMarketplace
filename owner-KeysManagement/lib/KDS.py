import secrets,hashlib,base64,networkx as nx,matplotlib.pyplot as plt
from os.path import exists
from cryptography.fernet import Fernet
from itertools import combinations
from numpy import byte

from .mapping import map

DEFAULTPATH = "D:\\Users\\richi\\Desktop\\DataMarketplace\\KDS.gml"

"""
Class used for the purpose of managing a key derivation structure 

NOTE:   Every node in the KDS is identified by an unique value built as the hash of the parts
        For example, the identifier of a resource called "a" is its hash : id_a = hash("a")
        where hash() is the sha3 deterministic function.
        The combination of any set of resources result as follows:
        id_abc = hash("a") xor hash("b") xor hash("c")
        This order independent hash rule is used to verify if a node in the KDS is the composition of 
        a specific set of resources without worrying about the order of the atomic resources.
"""
class KDS():

    def __init__(self, _graphName = DEFAULTPATH):
        self.map = map()
        if(exists(_graphName)):
            self.G = nx.read_gml(_graphName)
        else:
            self.G = nx.DiGraph()

    """
    The following function is used whenever a new resource need to be added to the KDS 

    idResource  :   is the sha3 result of the resource name
    unHashName  :   is used only for printing purpose
    key         :   is the secret key used for encrypt the data of the resource
    user        :   specify if a node is a user or a resource
    tag         :   (called label in the paper) represent the label associated to the secret key
    elements    :   is a collection of hashes of each resource that makes up the node. 
                    Essential for the resolution of the cover set problem.
    """
    def addResource(self,_resource):
        idResource = self.map.add(_resource)
        if idResource not in self.G:
            self.G.add_node(
                idResource,
                unHashName=_resource,
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = False,
                tag=secrets.token_hex(32),
                elements = [self.map.get(_resource)]
            )
            return True
        return False

    """
    The following procedure updates the KDS allowing a buyer to access the resources they are entitled to
    """
    def enforcePurchase(self,_buyer,_name,_capList):
        _buyer = _buyer.lower()
        if(self.map.get(_buyer)):
            _buyer = self.map.get(_buyer)
        else:
            _buyer = self.map.add(_buyer)
        

        if _buyer not in self.G:
            self.G.add_node(
                _buyer,
                unHashName=_name,
                key = base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = True
            )
        
        oldCap,R = self._previousState(_buyer,_capList)

        if(len(R)==0):
            return None

        n_cap_u = self._customCapHash(oldCap) 
        if  n_cap_u in self.G:
            self.G.remove_edge(_buyer,n_cap_u)
            if not self._existAnotherUser(_buyer,n_cap_u):
                par = [fr for fr,to in list(self.G.in_edges(n_cap_u))]
                desc = [to for fr,to in list(self.G.out_edges(n_cap_u))]
                if (len(par) * len(desc)) < (len(par) + len(desc)):
                    for n_par in par:
                        self.G.remove_edge(n_par, n_cap_u)
                        for n_desc in desc:
                            self.G.remove_edge(n_cap_u, n_desc)
                            self.G.add_edge(n_par, n_desc)
                    self.G.remove_node(n_cap_u)
        
        n_cap_u = self._customCapHash(_capList)
        if n_cap_u in self.G:
            self.G.add_edge(_buyer,n_cap_u)
        else:
            n_cap_u = self.map.add("".join(sorted(_capList,key=str.lower)))
            print("Updating -> \t{}".format(_capList))
            self.G.add_node(
                n_cap_u,
                unHashName=",".join(sorted(_capList,key=str.lower)),
                key= base64.urlsafe_b64decode(Fernet.generate_key()).hex(),
                user = False,
                tag=secrets.token_hex(32),
                elements = [self.map.get(el) for el in _capList]
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
            
        return True


    def getResourceEncKey(self,_resource):
        idResource = self.map.get(_resource)
        return idResource,self.G.nodes[idResource]["key"]

    def save(self,_path=DEFAULTPATH,_pubKey = "",_baseUrl="",_publish=True):
        nx.write_gml(self.G,_path)
        self.map.save(_pubKey=_pubKey,_baseUrl=_baseUrl,_publish=_publish)
    
    def _byte_xor(self,ba1, ba2):
        return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

    def _hash(self,_data):
        return hashlib.sha3_256(_data.encode('utf-8')).hexdigest()

    
    def _existAnotherUser(self,_buyer,_node):
        for fr,to in self.G.in_edges(_node):
            if self.G.nodes[fr]["user"] and fr != _buyer:
                return True
            
        return False
    
    def _customCapHash(self,_capList):
        return self.map.get("".join(sorted(_capList,key=str.lower)))

    """
    Compare the capability list with the current state in the KDS and returns the already accessible
    resources and the ones to be updated
    NOTE: the buyer will always be connected to only one node
    """
    def _previousState(self,_buyer,_capList):
        edge = [to for frm,to in list(self.G.out_edges(_buyer))]
        if len(edge) == 1:
            target = edge[0]
            capHash = "" 

            for idx,el in enumerate(_capList):
                capHash = self._customCapHash(_capList[:idx+1])
                if capHash == target:
                    return (_capList[:idx+1],_capList[idx+1:])

        return ([],_capList)

    """
    This function find the set of descendand of a node 

    First all combination of a set of resources if found: 
    example: the combination of "abc" = [a,b,c,ab,ab,bc]
    Those are all the possible subset that could exist in the KDS for the node "abc"

    Thanks to _potentialSubset() all the combination set that does not exist will be eliminated
    """
    def _findDesc(self, _capList):
        """
        comb = [list(combinations(_capList,size)) for size in range(len(_capList))]
        flattenedComb = [item for sublist in comb for item in sublist]
        flattenedComb = flattenedComb[1::]
        hashedComb = [self._customCapHash(el) for el in flattenedComb]

        potentialSubset = self._potentialSubset(_capList)

        temp = set(potentialSubset) - set(hashedComb)
        return list(set(potentialSubset) - temp)
        """
        Desc = []
        capHashes = set([self.map.get(el) for el in _capList])
        potentialSubsets = self._potentialSubset(_capList)

        for ptsbst in potentialSubsets:
            if set(self.G.nodes[ptsbst]["elements"]).issubset(capHashes):
                Desc = list(set(Desc) | set([ptsbst]))
        
        return Desc



    
    """
    Startign from the capability list of a buyer is possible to find the distinct ancestors
    """
    def _potentialSubset(self, _capList):
        capHashes = [self.map.get(el) for el in _capList]

        ancestors = [list(nx.ancestors(self.G,el)) for el in capHashes]
        flattenedAnc = [item for sublist in ancestors for item in sublist]
        flattenedAncNoUser = [node for node in flattenedAnc if self.G.nodes(data = True)[node]['user'] == 0]
        
        return list(set(flattenedAncNoUser) | set(capHashes))
    
    """
    Considering the set cover problem, the function follows the implementation of a greedy solution
    """
    def _greedySetCover(self,_capList,_desc):
        capHashes = [self.map.get(el) for el in _capList]
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

    """
    The following function return all the nodes that are superset of a given node
    """
    def _getPar(self,_capList,_currentNode):
        capHashes = set([self.map.get(el) for el in _capList])
        Par = []

        nodes = [x for x,y in self.G.nodes(data = True) if y['user']==0 and x != _currentNode]
        
        for node in nodes:
            if set(self.G.nodes[node]["elements"]).issuperset(capHashes):
                Par = list(set(Par) | set([node]))

        
        return Par

    def generateCatalogue(self):
        catalogue=[]
        for edge in self.G.edges:
            K_from = bytes.fromhex(self.G.nodes[edge[0]]["key"])
            K_to = bytes.fromhex(self.G.nodes[edge[1]]["key"])
            l_to = bytes.fromhex(self.G.nodes[edge[1]]["tag"])
            xor_Kl = self._byte_xor(K_from,l_to)

            hash_kl = bytes.fromhex(self._hash(xor_Kl.hex()))

            token = self._byte_xor(K_to,hash_kl).hex()
            """
            print("id :\t{}\ntoken:\t{}\nhash:\t{}\nxor:\t{}\nlabel:\t{}\nkey:\t{}".format(
                edge[1],
                token,
                hash_kl.hex(),
                xor_Kl.hex(),
                l_to.hex(),
                K_from.hex()
                ))
            """
            frm = edge[0] if edge[0][:2] == "0x" else "0x"+edge[0]
            to = edge[1] if edge[1][:2] == "0x" else "0x"+edge[1]

            label = "0x"+l_to.hex()

            catalogue.append((frm,to,token,label))

        return catalogue

    def show(self,_do):
        if _do:
            #pos = graphviz_layout(self.G,prog='twopi')
            #pos = nx.spring_layout(self.G, k=0.15, iterations=20)
            labels = nx.get_node_attributes(self.G, 'unHashName') 
            color_map = []
            for node,data in self.G.nodes(data = True):
                if data['user'] == 1:
                    color_map.append('red')
                else:
                    color_map.append('gray')
            #nx.draw(self.G,pos,with_labels = True,labels=labels)
            #nx.draw(self.G,pos)
            #nx.draw_circular(self.G,with_labels = True,labels=labels)
            #nx.draw_kamada_kawai(self.G,with_labels = True,labels=labels)
            nx.draw_planar(self.G,node_color = color_map, with_labels = True,labels=labels)
            plt.show() 