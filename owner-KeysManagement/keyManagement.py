import argparse


#from brownie import Contract, network, web3

from lib import KDS
from lib import util

kds = KDS.KDS()


resources = [
    {"id":"a","data":b"risorsa a"},
    {"id":"b","data":b"risorsa b"},
    {"id":"c","data":b"risorsa c"},
    {"id":"d","data":b"risorsa d"},
    {"id":"e","data":b"risorsa e"},
    {"id":"f","data":b"risorsa f"},
]



for x in resources:
    kds.addResource(x['id'])
    #print(util.crypt(kds.getResourceEncKey(x['id']),x['data']))

#kds.show()

kds.enforcePurchase("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387","w",["a","b","c"])
kds.show()
kds.enforcePurchase("0xwdfgsdfc74BF3b44EEC9ad07271165dD6B6FF8387","x",["c","d","e","f"])
kds.show()
kds.enforcePurchase("0xD1192bcsdfgsdfg44EEC9ad07271165dD6B6FF8387","y",["a","b","c"])
kds.show()
kds.enforcePurchase("0xZcompraBC","z",["b","c"])
kds.show()
kds.enforcePurchase("0xZcompraBC","z",["a","d","e","f"])
kds.show()
kds.enforcePurchase("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387","w",["d","e","f"])
kds.show()
kds.save()





