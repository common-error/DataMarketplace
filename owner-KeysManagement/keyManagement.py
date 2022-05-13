import argparse, os,sys,requests
import json
import re
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

parser.add_argument("-s","--show",action="store_true",help="Show the current visual representation of the graph")
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
        enk_list = []
        
        for x in resources["data"]:
            if kds.addResource(x['id']):
                id,key = kds.getResourceEncKey(x['id'])
                enk_data = util.crypt(key,bytes(x['data'].encode()))
                enk_list.append({
                    "id": id,
                    "data":enk_data,
                    "metadata":x["metadata"]
                    })
        
        
        if enk_list:
            data_to_send = {
                "resources":json.dumps(enk_list)
            }

            url = "{}addResources/{}".format(os.getenv("BASE_URL"),os.getenv("PUBLIC_KEY"))

            response = requests.post(url,data_to_send)
            print(response.json())
    
        kds.save()
        kds.show(args.show)
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

        to_add = util.modifiedResources(old_catalogue,new_catalogue)
        
        rpt = chain.updateCatalogue(to_add)
        print("{},{},{}".format(args.alias[0],rpt["gasUsed"],len(to_add)))

        kds.save()
        kds.show(args.show)
elif args.command == "deploy":
        chain = manageChain.chain()
        receipt = chain.deployContract()

        contractAddress = receipt.contractAddress

        data_to_send = {
            "contractAddress":contractAddress
        }

        #print(receipt)
        url = "{}addContract/{}".format(os.getenv("BASE_URL"),os.getenv("PUBLIC_KEY"))

        response = requests.post(url,data_to_send)
        print(response.json())

        print("")
        print("Contract created with the following address\n\t -> {}".format(contractAddress))
        print("SAVE THE FORMER ADDRESS IN THE .ENV FILE!")
        print("")
else:
    print("Incomplete command!")




