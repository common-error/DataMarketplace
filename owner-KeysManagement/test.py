from cProfile import label
from tkinter import Pack
from urllib import response
from brownie import chain, web3
from cryptography.fernet import Fernet
import secrets
import hashlib
import base64
import networkx as nx
import matplotlib.pyplot as pltpip
from numpy import byte
from rsa import sign

from lib import KDS

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

##################################################
G = nx.read_gml("./x.gml")
print(G.nodes())

########################################
a = "sdgasdfgasdfgsdfg"
c = [a]
b = ["sdfasdfasdf"]

print(list(set(c)-set(b)))

###########################################################
"""

"""
#WORK WITH WEB3PY
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

PATH_TO_TRUFFLE = "../smart-contract/build/contracts/"
trufflefile = json.load(open(PATH_TO_TRUFFLE+"accessAuth.json"))

abi = trufflefile['abi']
bytecode = trufflefile['bytecode']


ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337

print("Connected: {}".format(web3.isConnected()))



owner = {
    "publicKey" : "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1",
    "privateKey" : os.getenv("PRIVATE_KEY")
}
user = "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0"


#Create a contract in python
accessAuth = web3.eth.contract(abi=abi,bytecode=bytecode)
print(accessAuth)

#Get the latest transaction
nonce = web3.eth.getTransactionCount(owner["publicKey"])
print(nonce)

#Create a transaction
transaction = accessAuth.constructor().buildTransaction({
    "gasPrice":web3.eth.gas_price,
    "chainId":chain_id,
    "from":owner["publicKey"],
    "nonce":nonce
})

signed_txn = web3.eth.account.sign_transaction(transaction,private_key=owner["privateKey"])

tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(tx_receipt.contractAddress)

###########################################################

#working with contracts
contractAddress = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"

accessAuth = web3.eth.contract(address=contractAddress,abi=abi)
nonce = web3.eth.getTransactionCount(owner["publicKey"])
print("nonce: {}".format(nonce))



#Crea una transazione e modifica la blockchain
strore_transaction = accessAuth.functions.buyResources(["a","b"]).buildTransaction({
    "gasPrice":web3.eth.gas_price,
    "chainId":chain_id,
    "from":owner["publicKey"],
    "nonce":nonce,
    "value": 50
})
sign_store_tnx = web3.eth.account.sign_transaction(
    strore_transaction,
    private_key=owner["privateKey"]
)
send_store_tx = web3.eth.send_raw_transaction(sign_store_tnx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(send_store_tx)

#Chiama una funzione in sola lettura
print(accessAuth.functions.getCapabilityListByAddress(owner["publicKey"]).call())
print(web3.eth.get_balance(owner["publicKey"]))

###################################################################
"""

"""
#LEGGI GLI EVENTI
contractAddress = "0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"
accessAuth = web3.eth.contract(address=contractAddress,abi=abi)

transfer_filter = accessAuth.events.capabilityListUpdated.createFilter(
    fromBlock="0x0",
    argument_filters={
        '_buyer': owner["publicKey"]
        }
)

print(transfer_filter.get_all_entries())


import requests,json

BASE="http://127.0.0.1:5000/api/v1/"

address="0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab"
dict = {
    "signature":"",
    "resources":json.dumps({
        "a0b37b8bfae8e71330bd8e278e4a45ca916d00475dd8b85e9352533454c9fec8":"f",
        "42538602949f370aa331d2c07a1ee7ff26caac9cc676288f94b82eb2188b8465":"e"
    })

}

test ={
    "signature":"asdfasdfasd",
    "tewst":3,
    "d":json.dumps([2,4,56,3,2]),
    "a":json.dumps({
        "ab":"c",
        "ac":"df"
    })
}

response = requests.post(BASE + "addResources/"+address,dict)

print(response.json())
"""
kds = KDS.KDS()

kds.generateCatalogue()

