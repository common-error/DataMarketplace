import argparse, os,sys
from lib2to3.pgen2 import token
import json
import re
import string
from tokenize import group
from dotenv import load_dotenv

load_dotenv()

#from brownie import Contract, network, web3

from lib import KDS,util, manageChain

kds = KDS.KDS()

def input_file(arg_value, pat=re.compile(r".*\.(json)")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

def bytes_address(arg_value, pat=re.compile(r"^0x[a-fA-F0-9]{40}$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest = "command")
add_resources = subparser.add_parser("add",help="Used when there is the need to add new resources")
add_resources.add_argument("path",nargs=1,type=input_file,help="Path to the json file containing the resources")
update_kds = subparser.add_parser("update",help="Used when a buyer bought new resources and the KDS must be updated")
update_kds.add_argument("address",nargs=1,type=bytes_address,help="Public Key of a buyer wallet")
update_kds.add_argument("alias",nargs=1,type=str,help="Plain name of the buyer (only for visual representation)")
deploy = subparser.add_parser("deploy", help="Used to deploy a new smart contract on the blockchain")
args = parser.parse_args()


if args.command == "add":
    if args.path:
        resources = json.load(open(args.path[0]))
        
        for x in resources["data"]:
            kds.addResource(x['id'])
            #print(util.crypt(kds.getResourceEncKey(x['id']),x['data']))
        
        kds.save()
        kds.show()
elif args.command == "update":
    if os.getenv("CONTRACT_ADDRESS") == "":
        print("Contract not deployed nor .env file not updated!")
        sys.exit(0)

    if args.address:
        chain = manageChain.chain()
        resources = chain.getCapabilityListByAddress(args.address[0])   
        print("Current cap list: {}".format(resources))
        
        old_catalogue = set(kds.generateCatalogue())
        kds.enforcePurchase(args.address[0],args.alias[0],resources)
        new_catalogue = set(kds.generateCatalogue())

        common_el = (new_catalogue & old_catalogue)

        to_remove = old_catalogue - common_el
        to_add = list(new_catalogue - common_el)
        for fr,to,tok in to_remove:
            to_add.append((fr,to,""))

        for el in to_add:
            print(el)
        chain.updateCatalogue(to_add)

        kds.save()
        kds.show()
elif args.command == "deploy":
        chain = manageChain.chain()
        
        print("")
        print("Contract created with the following address\n\t -> {}".format(chain.deployContract()))
        print("SAVE THE FORMER ADDRESS IN THE .ENV FILE!")
        print("")
else:
    print("Incomplete command!")


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




