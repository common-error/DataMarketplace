import argparse

#from brownie import Contract, network, web3

from lib import KDS

kds = KDS.KDS()

resources = ["r1","r2","r3"]

for x in resources:
    kds.addResource(x)

kds.save()


