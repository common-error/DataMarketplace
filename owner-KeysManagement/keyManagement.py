import argparse, os,sys,requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

#from brownie import Contract, network, web3

from lib import KDS,util, manageChain
curr_path = os.path.dirname(os.path.realpath(__file__))
paths = {
    'graph' : curr_path+"\\runTime\\KDS.gml",
    'mapping' : curr_path+"\\runTime\\mapping.json",
    'abi' :  curr_path+"\\ABI\\accessAuth.json"
}

kds = KDS.KDS(paths['graph'],paths['mapping'])

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
parser.add_argument("-r","--ropsten",action="store_true",help="Use the ropsten test network")
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
            url = "{}addResources/{}".format(os.getenv("BASE_URL"),os.getenv("PUBLIC_KEY"))
            print(util.sendToWebServer("resources",enk_list,url))
    
        kds.save(_pubKey = os.getenv("PUBLIC_KEY"),_baseUrl=os.getenv("BASE_URL"))
        kds.show(args.show)
elif args.command == "update":
    if os.getenv("CONTRACT_ADDRESS") == "":
        print("Contract not deployed nor .env file not updated!")
        sys.exit(0)

    if args.address:
        chain = manageChain.chain(paths['abi'],args.ropsten)
        resources = chain.getCapabilityListByAddress(args.address[0])   

        print("Buyer ->\t"+args.address[0])
        
        old_catalogue = set(kds.generateCatalogue())
        if(kds.enforcePurchase(args.address[0],args.alias[0],resources) != None):
            new_catalogue = set(kds.generateCatalogue())

            (to_add,num_removed,num_added) = util.modifiedResources(old_catalogue,new_catalogue)
            
            rpt = chain.updateKDS_Hash(kds.generateHash())
            
            print("{},{},{},{}\n".format(args.address[0],rpt["gasUsed"],num_removed,num_added))

            url = "{}graph".format(os.getenv("BASE_URL"))
            print(util.sendToWebServer("graph",kds.exportToWebServer(),url))

            kds.save(_pubKey = os.getenv("PUBLIC_KEY"),_baseUrl=os.getenv("BASE_URL"))
            kds.show(args.show)
        else:
            print("No update on capList!")
            kds.show(args.show)
        
elif args.command == "deploy":
        chain = manageChain.chain(paths['abi'],args.ropsten)
        receipt = chain.deployContract()

        contractAddress = receipt.contractAddress

        
        url = "{}addContract/{}".format(os.getenv("BASE_URL"),os.getenv("PUBLIC_KEY"))
        print(util.sendToWebServer("contractAddress",contractAddress,url))

        print("")
        print("Contract created with the following address\n\t -> {}".format(contractAddress))
        print("SAVE THE FORMER ADDRESS IN THE .ENV FILE!")
        print("")
else:
    print("Incomplete command!")




