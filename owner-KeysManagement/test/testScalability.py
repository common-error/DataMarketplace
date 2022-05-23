from copy import copy
from distutils.command.build import build
import json
import random
from web3 import Web3
import os
import subprocess
from dotenv import load_dotenv
from os.path import exists

load_dotenv()
PATH_TO_TRUFFLE = "../../smart-contract/build/contracts/"
WALLETS = "../wallets.json"
RESOURCES = "../resources.json"
MAX_X_BUY = 50
trufflefile = json.load(open(PATH_TO_TRUFFLE+"accessAuth.json"))

abi = trufflefile['abi']
bytecode = trufflefile['bytecode']

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337


class tester():

    def __init__(self,_wallets=WALLETS,_resources=RESOURCES):
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

    def startTest(self):
        numBuy = 0
        while(len(self.stillToBuy.keys())>1):
            numBuy+=1
            pubKey,privKey,idxBuyer = self._chooseRndBuyer()
            buyer = {
                "publicKey" : web3.toChecksumAddress(pubKey),
                "privateKey" : privKey 
            }
            print(buyer['publicKey'])
            resToBuy = self._fixList(pubKey,random.randint(1,min(len(self.stillToBuy[pubKey]),MAX_X_BUY)))

            self._tx(buyer,resToBuy)
            self.iteration+=1

            subprocess.call(["python","D:\\Users\\richi\\Desktop\\DataMarketplace\\owner-KeysManagement\\keyManagement.py","update",buyer['publicKey'],str(idxBuyer)],shell=True)
        print("Numero acquisti:\t{}".format(numBuy))

    
    def _fixList(self,_buyer,_wantedRes):
        print(self.stillToBuy[_buyer])
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
            "gasPrice":350000000,
            "chainId":chain_id,
            "from":_user["publicKey"],
            "nonce":nonce,
            "value": web3.toWei(500, 'gwei')
        })
        sign_store_tnx = web3.eth.account.sign_transaction(
            strore_transaction,
            private_key=_user["privateKey"]
        )
        send_store_tx = web3.eth.send_raw_transaction(sign_store_tnx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(send_store_tx)

        self._saveResult("{},{},{}\n".format(self.iteration,_user["publicKey"],tx_receipt["gasUsed"]))
    
    def _saveResult(self,_text):
        with open("D:\\Users\\richi\\Desktop\\DataMarketplace\\scalabilityResults\\buyProcess.txt", "a+") as f:
            f.write(_text)


ts = tester()
ts.startTest()
