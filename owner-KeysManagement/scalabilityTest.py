from copy import copy
import datetime
from distutils.command.build import build
import json
import random
from tkinter import N
import requests
from web3 import Web3
import signal
import sys
import os
import subprocess
from dotenv import load_dotenv
from os.path import exists
import time

from lib import KDS,util,manageChain

curr_path = os.path.dirname(os.path.realpath(__file__))
paths = {
    'graph' : curr_path+"\\runTime\\KDS.gml",
    'mapping' : curr_path+"\\runTime\\mapping.json",
    'abi' :  curr_path+"\\ABI\\accessAuth.json",
    'wallets' : curr_path+"\\wallets\\wallets500x.json",
    'resources' : curr_path+"\\resources\\resources10000x.json",
    'saveUpdate' : curr_path+"\\runTime\\scalabilityResults\\savedUpdate.txt",
    'saveBuy' : curr_path+"\\runTime\\scalabilityResults\\savedBuy.txt",
    'saveBought' : curr_path+"\\runTime\\scalabilityResults\\savedBought.json"
}

load_dotenv()
MAX_X_BUY = 250
trufflefile = json.load(open(paths['abi']))

abi = trufflefile['abi']
bytecode = trufflefile['bytecode']

ganache_url = "http://127.0.0.1:8545"
#adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
#session = requests.Session()
#session.mount('http://', adapter)
#session.mount('https://', adapter)
#web3 = Web3(Web3.HTTPProvider(ganache_url,session=session,request_kwargs={'timeout':600}))
web3 = Web3(Web3.HTTPProvider(ganache_url,request_kwargs={'timeout': 600}))
chain_id = 1337
bougthResources = {
    "bougthRes" : []
}


class tester():

    def __init__(self,_wallets=paths['wallets'],_resources=paths['resources']):
        self.iteration = 0
        if(exists(_wallets)):
            with open(_wallets,'r') as f:
                self.keys = json.load(f)['private_keys']

        if(exists(_resources)):
            self.stillToBuy = {}
            with open(_resources,'r') as f:
                resources = [el['id'] for el in json.load(f)['data']]
                for key in [*self.keys.keys()]:
                    self.stillToBuy[key] = copy(resources)

        contractAddress = os.getenv("CONTRACT_ADDRESS")

        self.accessAuth = web3.eth.contract(address=contractAddress,abi=abi)
        self.chain = manageChain.chain(paths['abi'])
        self.kds = KDS.KDS(paths['graph'],paths['mapping'])
        self.numBoughtRes = 0
        self.start_time = time.time()

        signal.signal(signal.SIGINT, self.signal_handler) 

    def signal_handler(self,*args):
        print("\nChiusura.... salvataggio file!")
        
        with open(paths['saveBought'], "w") as f:
            json.dump(bougthResources, f)
        print("Numero risorse acquistate:\t{}".format(self.numBoughtRes))
        print("--- %s seconds ---" % (time.time() - self.start_time))
        sys.exit(0)

    def startTest(self,_file=""):

        try:
            if(_file == ""):
                while(len(self.stillToBuy.keys())>1 and self.numBoughtRes < 18000):
                    pubKey,privKey,idxBuyer = self._chooseRndBuyer()
                    buyer = {
                        "publicKey" : web3.toChecksumAddress(pubKey),
                        "privateKey" : privKey 
                    }
                    resToBuy = self._fixList(pubKey,random.randint(1,min(len(self.stillToBuy[pubKey]),MAX_X_BUY)))
                    self.numBoughtRes += len(resToBuy)
                    bougthResources['bougthRes'].append({
                        'key' : pubKey,
                        'res' : resToBuy,
                        'idx' : idxBuyer 
                    })

                    print("==========================================")
                    print("\t\tBuying")
                    print("Buyer ->\t{}".format(buyer['publicKey']))
                    print("Buying ->\t{}".format(resToBuy))
                    self._tx(buyer,resToBuy)
                    

                    print("\t\tUpdating")
                    self._update(buyer['publicKey'],str(idxBuyer))
                    self.iteration+=1
            else:
                with open(_file,'r') as f:
                    data = json.load(f)
                for el in data["bougthRes"]:
                    buyer = {
                        "publicKey" : web3.toChecksumAddress(el["key"]),
                        "privateKey" : self.keys[el["key"]] 
                    }
                    resToBuy = el["res"]
                    self.numBoughtRes += len(resToBuy)
                    
                    print("==========================================")
                    print("Buying...")
                    print("Buyer ->\t{}".format(buyer['publicKey']))
                    print("Buying ->\t{}".format(resToBuy))
                    self._tx(buyer,resToBuy)
                    

                    print("Updating...")
                    self._update(buyer['publicKey'],str(el["idx"]))
                    self.iteration+=1
                    
        except Exception as e:
            print("Errore!")
            print(e)
            with open(paths['saveBought'], "w") as f:
                json.dump(bougthResources, f)
            print("Numero risorse acquistate:\t{}".format(self.numBoughtRes))
            print("--- %s seconds ---" % (time.time() - self.start_time))
            sys.exit(0)
            

        print("Numero risorse acquistate:\t{}".format(self.numBoughtRes))
        print("--- %s seconds ---" % (time.time() - self.start_time))

    def startTimeTest(self,_file=""):
        current = 50
        try:
            if(_file == ""):
                while(current <= MAX_X_BUY):
                    pubKey,privKey,idxBuyer = self._chooseRndBuyer()
                    buyer = {
                        "publicKey" : web3.toChecksumAddress(pubKey),
                        "privateKey" : privKey 
                    }
                    resToBuy = self._fixList(pubKey,current)
                    if current == 250:
                        current = 50
                    else:
                        current += 10
                    self.numBoughtRes += len(resToBuy)
                    bougthResources['bougthRes'].append({
                        'key' : pubKey,
                        'res' : resToBuy,
                        'idx' : idxBuyer 
                    })

                    print("==========================================")
                    print("\t\tBuying")
                    print("Buyer ->\t{}".format(buyer['publicKey']))
                    print("Buying ->\t{}".format(resToBuy))

                    self._tx(buyer,resToBuy)
                    

                    print("\t\tUpdating")
                    self._update(buyer['publicKey'],str(idxBuyer))
                    self.iteration+=1
            else:
                with open(_file,'r') as f:
                    data = json.load(f)
                for el in data["bougthRes"]:
                    buyer = {
                        "publicKey" : web3.toChecksumAddress(el["key"]),
                        "privateKey" : self.keys[el["key"]] 
                    }
                    resToBuy = el["res"]
                    self.numBoughtRes += len(resToBuy)
                    
                    print("==========================================")
                    print("Buying...")
                    print("Buyer ->\t{}".format(buyer['publicKey']))
                    print("Buying ->\t{}".format(resToBuy))
                    self._tx(buyer,resToBuy)
                    

                    print("Updating...")
                    self._update(buyer['publicKey'],str(el["idx"]))
                    self.iteration+=1
                    
        except Exception as e:
            print("Errore!")
            print(e)
            with open(paths['saveBought'], "w") as f:
                json.dump(bougthResources, f)
            print("Numero risorse acquistate:\t{}".format(self.numBoughtRes))
            print("--- %s seconds ---" % (time.time() - self.start_time))
            sys.exit(0)
            

        print("Numero risorse acquistate:\t{}".format(self.numBoughtRes))
        print("--- %s seconds ---" % (time.time() - self.start_time))
    
    def _fixList(self,_buyer,_wantedRes):
        resToBuy = []
        for idx in range(_wantedRes):
            rndIdx = random.randint(0,(len(self.stillToBuy[_buyer])-1))
            resToBuy.append(self.stillToBuy[_buyer][rndIdx])
            self.stillToBuy[_buyer][rndIdx] = self.stillToBuy[_buyer][-1]
            self.stillToBuy[_buyer].pop(-1)

        if(len(self.stillToBuy[_buyer]) == 0):
            del self.stillToBuy[_buyer]
            del self.keys[_buyer]

        return resToBuy



    def _chooseRndBuyer(self):
        idx = random.randint(0,len(self.keys)-1)
        pblKey = [*self.stillToBuy.keys()][idx]
        return pblKey,self.keys[pblKey],idx

    def _randomIndexes(self, _len=MAX_X_BUY):
        return random.sample(range(_len),random.randint(0,_len))

    def _tx(self,_user,_resources):
        
        nonce = web3.eth.getTransactionCount(_user["publicKey"])

        strore_transaction = self.accessAuth.functions.buyResources(_resources).buildTransaction({
            "gasPrice":web3.toWei('20', 'gwei'),
            "chainId":chain_id,
            "from":_user["publicKey"],
            "nonce":nonce,
            "value": web3.toWei(50, 'gwei')
        })
        sign_store_tnx = web3.eth.account.sign_transaction(
            strore_transaction,
            private_key=_user["privateKey"]
        )

        t1 = time.time()
        send_store_tx = web3.eth.send_raw_transaction(sign_store_tnx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(send_store_tx)
        t2 = time.time()

        self._saveResult("{},{},{},{},{}\n".format(self.iteration,_user["publicKey"],tx_receipt["gasUsed"],len(_resources),(t2-t1)))
        self.sleep()


    def _saveResult(self,_text):
        with open(paths['saveBuy'], "a+") as f:
            f.write(_text)
    
    def deployAndAdd(self):
        receipt = self.chain.deployContract()
        print("Contract deployed at ->\t{}".format(receipt.contractAddress))

        resources = json.load(open(paths['resources']))
        
        for x in resources["data"]:
            self.kds.addResource(x['id'])

        print("Resources added -> {}".format(len(resources["data"])))
    
    def _update(self,_pubKey,_alias):
        resources = self.chain.getCapabilityListByAddress(_pubKey)

        old_catalogue = set(self.kds.generateCatalogue())
        if(self.kds.enforcePurchase(_pubKey,_alias,resources) != None):
            new_catalogue = set(self.kds.generateCatalogue())

            (to_add,num_removed,num_added) = util.modifiedResources(old_catalogue,new_catalogue)
            
            hash= self.kds.generateHash()
            rpt = self.chain.updateKDS_Hash(hash)
            
            print("pubKey -> \t{}\ngasUsed ->\t{}\nKDS_Hash ->\t{}".format(_pubKey,rpt["gasUsed"],hash))
            util.saveResult("{},{},{},{}\n".format(self.iteration,_pubKey,rpt["gasUsed"],hash),paths['saveUpdate'])

        else:
            print("No update on capList!")

        self.sleep()

    
    def sleep(self):
        time.sleep(0)

ts = tester()

ts.deployAndAdd()
ts.startTimeTest()