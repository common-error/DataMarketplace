from cryptography.fernet import Fernet
import secrets
import hashlib
import base64
import networkx as nx
import matplotlib.pyplot as pltpip

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def byte_and(ba1, ba2):
    return bytes([_a & _b for _a, _b in zip(ba1, ba2)])

def hash(_data):
    return hashlib.sha3_256(_data.encode('utf-8')).hexdigest()

def capHash(_data):
    tempHash = bytearray(32)
    for el in _data:
        tempHash = byte_xor(tempHash, hashlib.sha3_256(el.encode('utf-8')).digest())
        
    return tempHash
"""

ka = base64.urlsafe_b64decode(Fernet.generate_key())
kc = base64.urlsafe_b64decode(Fernet.generate_key())
lc = secrets.token_bytes(32)

f = Fernet(base64.urlsafe_b64encode(kc))
token = f.encrypt(b"my deep dark secret")

print(token)


hash_ka = hashlib.sha3_256(ka).digest()
hash_lc = hashlib.sha3_256(lc).digest()

print(type(hash_ka))

T_ac = byte_xor(kc,hashlib.sha3_256(hash_ka + hash_lc).digest())


new_kc = byte_xor(T_ac,hashlib.sha3_256(hash_ka + hash_lc).digest())


if kc == new_kc:
    print("true")
    f = Fernet(base64.urlsafe_b64encode(new_kc))

    print(f.decrypt(token))
else:
    print("false")

##################################################

x = ["x","x"]
y = ["y","y","y"]
z = ["r1","r5"]

hash = bytearray(32)
hash1 = bytearray(32)
hash2 = bytearray(32)

for el in x:
    hash = byte_xor(hash, hashlib.sha3_256(el.encode('utf-8')).digest())

for el in y:
    hash1 = byte_xor(hash1, hashlib.sha3_256(el.encode('utf-8')).digest())

for el in z:
    hash2 = byte_xor(hash2, hashlib.sha3_256(el.encode('utf-8')).digest())

print(hash == hash1)
print(hash == hash2)
########################################################################################

G = nx.read_gml("../KDS.gml")



#print(G.in_edges("d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f"))
_buyer = "0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387"
G.add_edge(_buyer,"d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f")
#G.add_edge("0xC1192bc74BF3b44EEC9ad07271165dD6B6FF8387","d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f")
for fr,to in G.in_edges("d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f"):
    if G.nodes[fr]["user"] and fr != _buyer:
        print("True")

print("false")


######################################################

test = ["r1","r2","r2"]
test2 = ["r3"]
G = nx.read_gml("../KDS.gml")

G.add_edge("d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f","5dc06a84656da8277d534b82c36a5c0607efcd73295d75a66f8a5fca7b44cb65")
G.add_edge("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387","5dc06a84656da8277d534b82c36a5c0607efcd73295d75a66f8a5fca7b44cb65")

capHashes = ["5dc06a84656da8277d534b82c36a5c0607efcd73295d75a66f8a5fca7b44cb65","5dc06a84656da8277d534b82c36a5c0607efcd73295d75a66f8a5fca7b44cb65"]
x = [list(nx.ancestors(G,el)) for el in capHashes]
l = [item for sublist in x for item in sublist]
print(list(set(l)))
nx.write_gml(G,"x.gml")


bc = byte_xor( hashlib.sha3_256("b".encode("utf-8")).digest(),hashlib.sha3_256("c".encode("utf-8")).digest())
b = hashlib.sha3_256("b".encode("utf-8")).digest()
c = hashlib.sha3_256("c".encode("utf-8")).digest()

x = byte_xor(bc,b)

print(byte_xor(x,c) == bytearray(32))



from itertools import combinations


 
vec = ["a","b","c"]
comb = [list(combinations(vec,x)) for x in range(len(vec))]
flattened = [item for sublist in comb for item in sublist]
flattened = flattened[1::]
hashed = [capHash(el) for el in flattened]
print(hashed[0] == capHash(["b"]))
print(hashed)

##########################################################################
import matplotlib.pyplot as plt
G = nx.read_gml("../KDS.gml")
labels = nx.get_node_attributes(G, 'unHashName') 
nx.draw(G,with_labels = True,labels=labels)
plt.show()

###################################################

ToRemove = []
ToRemove = list(set(ToRemove) | set([("a","b")]))
ToRemove = list(set(ToRemove) | set([("c","b")]))
ToRemove = list(set(ToRemove) | set([("c","b")]))
for x,y in ToRemove:
    print("{} {}".format(x,y))

"""

G = nx.read_gml("./x.gml")
a,b = list(G.out_edges("d0bd83a1c71c96b196e5369a674dd41b804c9f32c8fbf2f00514bd4b9d7a057f"))[0]
print(b)