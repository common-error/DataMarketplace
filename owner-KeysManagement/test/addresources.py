import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
PATH_TO_TRUFFLE = "../../smart-contract/build/contracts/"
trufflefile = json.load(open(PATH_TO_TRUFFLE+"accessAuth.json"))

abi = trufflefile['abi']
bytecode = trufflefile['bytecode']

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337

w = {
    "lb" : "w",
    "publicKey" : "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
    "privateKey" : "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
}

x = {
    "lb" : "x",
    "publicKey" : "0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b",
    "privateKey" : "0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c"
}

y = {
    "lb" : "y",
    "publicKey" : "0xE11BA2b4D45Eaed5996Cd0823791E0C93114882d",
    "privateKey" : "0x646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913"
}

z = {
    "lb" : "z",
    "publicKey" : "0xd03ea8624C8C5987235048901fB614fDcA89b117",
    "privateKey" : "0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743"
}



contractAddress = os.getenv("CONTRACT_ADDRESS")

accessAuth = web3.eth.contract(address=contractAddress,abi=abi)


def tx(_user,_resources):
    
    nonce = web3.eth.getTransactionCount(_user["publicKey"])

    strore_transaction = accessAuth.functions.buyResources(_resources).buildTransaction({
        "gasPrice":350000000,
        "chainId":chain_id,
        "from":_user["publicKey"],
        "nonce":nonce,
        "value": web3.toWei(6469331.115997997, 'gwei')
    })
    sign_store_tnx = web3.eth.account.sign_transaction(
        strore_transaction,
        private_key=_user["privateKey"]
    )
    send_store_tx = web3.eth.send_raw_transaction(sign_store_tnx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(send_store_tx)

    print("{},{}".format(_user["lb"],tx_receipt["gasUsed"]))


user = x
resources = ["a","b","c"]
tx(user,resources)

input()

user = w
resources = ["d","e","f"]
tx(user,resources)

input()

user = y
resources = ["d","e"]
tx(user,resources)

input()

user = y
resources = ["a","b","c","f"]
tx(user,resources)

input()

user = w
resources = ["c"]
tx(user,resources)

input()

user = z
resources = ["c","d","e","f"]
tx(user,resources)




