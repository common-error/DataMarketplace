from cryptography.fernet import Fernet
import secrets
import hashlib
import base64
import networkx as nx

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

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

"""
test = ["r1","r2","r3"]
print(test[:1])
print(test[1:])