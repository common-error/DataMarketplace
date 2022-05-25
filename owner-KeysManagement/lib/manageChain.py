import json,os,sys
from pickle import FALSE
from async_timeout import timeout
from numpy import byte
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class chain():

    def __init__(self,_pathToAbi,_ropsten = False):
        data = json.load(open(_pathToAbi))

        self.abi = data['abi']
        self.bytecode = data['bytecode']
        self.owner = {
            "privKey":os.getenv("PRIVATE_KEY"),
            "pubKey": os.getenv("PUBLIC_KEY")
        }
        if(_ropsten):
            self.ropsten = True
            self.network = {
                "url": os.getenv("ROPSTEN")
            }
        else:
            self.ropsten = False
            self.network = {
                "url": os.getenv("GANACHE_URL"),
                "chainId": int(os.getenv("CHAIN_ID"))
            }

        adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self.w3 = Web3(Web3.HTTPProvider(self.network["url"],session=session,request_kwargs={'timeout':600}))
        #self.w3 = Web3(Web3.HTTPProvider(self.network["url"], request_kwargs={'timeout': 600}))

        if self.w3.isConnected():
            print("Connected to {}".format(self.network["url"]))
        else:
            print("Connection to {} failed".format(self.network["url"]))
            sys.exit(0)

    def deployContract(self):
        self.contract = self.w3.eth.contract(abi=self.abi,bytecode=self.bytecode)

        #Get the latest transaction
        nonce = self.w3.eth.getTransactionCount(self.owner["pubKey"])

        if(self.ropsten):
            transaction = self.contract.constructor().buildTransaction({
                "gasPrice":self.w3.toWei('50', 'gwei'),
                "from":self.owner["pubKey"],
                "nonce":nonce
            })
        else:
            transaction = self.contract.constructor().buildTransaction({
                "gasPrice":self.w3.toWei('21', 'gwei'),
                "chainId":self.network["chainId"],
                "from":self.owner["pubKey"],
                "nonce":nonce
            })

        receipt = self._completeTransaction(transaction)
        self.contractAddress = receipt.contractAddress
        return receipt

    def getCapabilityListByAddress(self,_buyer):

        self.contract = self.w3.eth.contract(
            address=self._safeContractAddress(),
            abi=self.abi
        )

        return  self.contract.functions.getCapabilityListByAddress(_buyer).call()

    def updateKDS_Hash(self, _KDS_Hash):
        contract = self.w3.eth.contract(address=self._safeContractAddress(),abi=self.abi)

        
        nonce = self.w3.eth.getTransactionCount(self.owner["pubKey"])

        if(self.ropsten):
            transaction = contract.functions.updateKDS_Hash(_KDS_Hash).buildTransaction({
                "gasPrice":self.w3.toWei('21', 'gwei'),
                "from":self.owner["pubKey"],
                "nonce":nonce
            })
        else:
            transaction = contract.functions.updateKDS_Hash(_KDS_Hash).buildTransaction({
                "gasPrice":self.w3.toWei('21', 'gwei'),
                "chainId":self.network["chainId"],
                "from":self.owner["pubKey"],
                "nonce":nonce
            })

        return self._completeTransaction(transaction)

        

    def _completeTransaction(self,_transaction):

        signed_tx = self.w3.eth.account.sign_transaction(
            _transaction,
            private_key = self.owner["privKey"]
        )

        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return tx_receipt

    def _safeContractAddress(self):
        if (contractAddress := os.getenv("CONTRACT_ADDRESS")) == "" and self.contractAddress == "":
            print("Contract address not available!")
            print("Create one, or provide it into .env file")
            sys.exit(0)
        else:
            return contractAddress if contractAddress != "" else  self.contractAddress
