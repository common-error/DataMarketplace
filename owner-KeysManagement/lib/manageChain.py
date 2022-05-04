import json,os,sys
from numpy import byte
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

PATH_TO_ABI = "../smart-contract/build/contracts/accessAuth.json"

class chain():

    def __init__(self,_pathToAbi=PATH_TO_ABI):
        data = json.load(open(_pathToAbi))

        self.abi = data['abi']
        self.bytecode = data['bytecode']
        self.owner = {
            "privKey":os.getenv("PRIVATE_KEY"),
            "pubKey": os.getenv("PUBLIC_KEY")
        }
        self.network = {
            "url": os.getenv("GANACHE_URL"),
            "chainId": int(os.getenv("CHAIN_ID"))
        }

        self.w3 = Web3(Web3.HTTPProvider(self.network["url"]))

        if self.w3.isConnected():
            print("Connected to {}".format(self.network["url"]))
        else:
            print("Connection to {} failed".format(self.network["url"]))
            sys.exit(0)

    def deployContract(self):
        self.contract = self.w3.eth.contract(abi=self.abi,bytecode=self.bytecode)

        #Get the latest transaction
        nonce = self.w3.eth.getTransactionCount(self.owner["pubKey"])

        transaction = self.contract.constructor().buildTransaction({
            "gasPrice":self.w3.eth.gas_price,
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

    def updateCatalogue(self, _catalogue):
        contract = self.w3.eth.contract(address=self._safeContractAddress(),abi=self.abi)

        
        nonce = self.w3.eth.getTransactionCount(self.owner["pubKey"])

        transaction = contract.functions.updateCatalogue(_catalogue).buildTransaction({
            "gasPrice":self.w3.eth.gas_price,
            "chainId":self.network["chainId"],
            "from":self.owner["pubKey"],
            "nonce":nonce
        })

        self._completeTransaction(transaction)

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
