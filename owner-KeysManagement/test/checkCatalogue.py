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

w = {
    "publicKey" : "0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0",
    "privateKey" : "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1"
}


contractAddress = os.getenv("CONTRACT_ADDRESS")

accessAuth = web3.eth.contract(address=contractAddress,abi=abi)

catalogue = [('0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b', '0x30315c6871ecc6b720c584038e5400442b2a3e3aa8d06667d9b483b74b53a92c', 'd47b9694c351e51419882b2813d094b5d93553e7b35828dd79ed0ed1d5bf30f7'),('0x160beb0a56e1fdc4f32749dc1498897f9d977f2bab9783b23d099e8b59dd0026', '0x30315c6871ecc6b720c584038e5400442b2a3e3aa8d06667d9b483b74b53a92c', '2cb77750b798b90b8221c7c89aa3951c8483f724b4c33d3fa46d63a23f1b5c8b'),('0x30315c6871ecc6b720c584038e5400442b2a3e3aa8d06667d9b483b74b53a92c', '0x80084bf2fba02475726feb2cab2d8215eab14bc6bdd8bfb2c8151257032ecd8b', 'e6296bf6cceeeaefbc963767c3ac778ff38fbf384b1ee7b707da48d3de838c43'),('0x30315c6871ecc6b720c584038e5400442b2a3e3aa8d06667d9b483b74b53a92c', '0xb039179a8a4ce2c252aa6f2f25798251c19b75fc1508d9d511a191e0487d64a7', 'a23ad819dc4ed9b5ede8dab3cc568ee62e5506819ccee036ca6f3afd1f77375b'),('0x160beb0a56e1fdc4f32749dc1498897f9d977f2bab9783b23d099e8b59dd0026', '0x80084bf2fba02475726feb2cab2d8215eab14bc6bdd8bfb2c8151257032ecd8b', ''),('0x160beb0a56e1fdc4f32749dc1498897f9d977f2bab9783b23d099e8b59dd0026', '0xb039179a8a4ce2c252aa6f2f25798251c19b75fc1508d9d511a191e0487d64a7', '')]

for frm,to,exTo in catalogue:

    if (accessAuth.functions.getToken(frm,to).call()).hex() == exTo:
        print("True")
    else:
        print("False")
        
    