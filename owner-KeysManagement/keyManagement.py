import argparse

#from brownie import Contract, network, web3

from lib import KDS
from lib import util

kds = KDS.KDS()

resources = [
    {"id":"r1","data":b"prima risorsa"},
    {"id":"r2","data":b"seconda risorsa"},
]

for x in resources:
    kds.addResource(x['id'])
    print(util.crypt(kds.getResourceEncKey(x['id']),x['data']))

#kds.enforcePurchase("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387",["r1","r2"])

kds.save()





