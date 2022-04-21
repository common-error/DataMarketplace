import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
PATH_TO_TRUFFLE = "../smart-contract/build/contracts/"
trufflefile = json.load(open(PATH_TO_TRUFFLE+"accessAuth.json"))

abi = trufflefile['abi']
bytecode = trufflefile['bytecode']

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
chain_id = 1337

buyer = {
    "publicKey" : "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
    "privateKey" : "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
}

contractAddress = "0x26b4AFb60d6C903165150C6F0AA14F8016bE4aec"

accessAuth = web3.eth.contract(address=contractAddress,abi=abi)
nonce = web3.eth.getTransactionCount(buyer["publicKey"])

strore_transaction = accessAuth.functions.buyResources(["a","b"]).buildTransaction({
    "gasPrice":web3.eth.gas_price,
    "chainId":chain_id,
    "from":buyer["publicKey"],
    "nonce":nonce,
    "value": 50
})
sign_store_tnx = web3.eth.account.sign_transaction(
    strore_transaction,
    private_key=buyer["privateKey"]
)
send_store_tx = web3.eth.send_raw_transaction(sign_store_tnx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(send_store_tx)