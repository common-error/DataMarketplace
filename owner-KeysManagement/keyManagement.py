import argparse
import json
import re
from tokenize import group


#from brownie import Contract, network, web3

from lib import KDS
from lib import util

kds = KDS.KDS()

def input_file(arg_value, pat=re.compile(r".*\.(json)")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest = "command")
add_resources = subparser.add_parser("add",help="Used when there is the need to add new resources")
add_resources.add_argument("path",nargs=1,type=input_file,help="Path to the json file containing the resources")
args = parser.parse_args()

if args.command == "add":
    if args.path:
        resources = json.load(open(args.path[0]))
        
        for x in resources["data"]:
            kds.addResource(x['id'])
            #print(util.crypt(kds.getResourceEncKey(x['id']),x['data']))
        
        #kds.save()
        kds.show()

"""
for x in resources:
    kds.addResource(x['id'])
    #print(util.crypt(kds.getResourceEncKey(x['id']),x['data']))

#kds.show()

kds.enforcePurchase("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387","w",["a","b","c"])
kds.enforcePurchase("0xwdfgsdfc74BF3b44EEC9ad07271165dD6B6FF8387","x",["c","d","e","f"])
kds.enforcePurchase("0xD1192bcsdfgsdfg44EEC9ad07271165dD6B6FF8387","y",["a","b","c"])
kds.enforcePurchase("0xZcompraBC","z",["b","c"])
kds.enforcePurchase("0xZcompraBC","z",["b","c","a","d","e","f"])
kds.enforcePurchase("0xD1192bc74BF3b44EEC9ad07271165dD6B6FF8387","w",["a","b","c","d","e","f"])


kds.show()
#kds.save()
"""




