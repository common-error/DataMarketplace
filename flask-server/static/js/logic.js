const ganache_url = "http://127.0.0.1:8545"
window.web3 = new Web3(ganache_url);
window.userWalletAddress = null
window.newCap = null

//-----------------------------------------------------
// data for testing
window.resourcesToBuy = ["a","b","c"]
window.userKey = "250f79b0de738847131c54244e5d7595930298a135e41de35c02a658023d82fc"
//-----------------------------------------------------

// VARIABLES
//*************************************************************************
const ABI = [
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "_buyer",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "price",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string[]",
        "name": "oldCababilityList",
        "type": "string[]"
      },
      {
        "indexed": false,
        "internalType": "string[]",
        "name": "newCapabilityList",
        "type": "string[]"
      }
    ],
    "name": "CapabilityListUpdated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "from",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "to",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "label",
            "type": "bytes32"
          }
        ],
        "indexed": false,
        "internalType": "struct accessAuth.updateData[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "name": "UpdateData",
    "type": "event"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string[]",
        "name": "_resources",
        "type": "string[]"
      }
    ],
    "name": "buyResources",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "from",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "to",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "label",
            "type": "bytes32"
          }
        ],
        "internalType": "struct accessAuth.updateData[]",
        "name": "_updateData",
        "type": "tuple[]"
      }
    ],
    "name": "updateCatalogue",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "id",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          }
        ],
        "internalType": "struct accessAuth.node[]",
        "name": "_node",
        "type": "tuple[]"
      },
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "id",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          }
        ],
        "internalType": "struct accessAuth.node",
        "name": "_data",
        "type": "tuple"
      }
    ],
    "name": "_updateElementsInNode",
    "outputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "id",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          }
        ],
        "internalType": "struct accessAuth.node",
        "name": "",
        "type": "tuple"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_buyer",
        "type": "address"
      }
    ],
    "name": "getCapabilityListByAddress",
    "outputs": [
      {
        "internalType": "string[]",
        "name": "",
        "type": "string[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "_from",
        "type": "bytes32"
      }
    ],
    "name": "getTokens",
    "outputs": [
      {
        "components": [
          {
            "internalType": "bytes32",
            "name": "id",
            "type": "bytes32"
          },
          {
            "internalType": "bytes32",
            "name": "token",
            "type": "bytes32"
          }
        ],
        "internalType": "struct accessAuth.node[]",
        "name": "",
        "type": "tuple[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "_edge",
        "type": "bytes32"
      }
    ],
    "name": "getLabel",
    "outputs": [
      {
        "internalType": "bytes32",
        "name": "",
        "type": "bytes32"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]


const contractAddress = document.getElementById("contractAddress").textContent
const contract = new window.web3.eth.Contract(ABI,contractAddress)



const metaButton = document.querySelector('.connectoToMetaMask');
const getCapListButton = document.querySelector('.getCapList');
const updateCapListButton = document.querySelector('.UpdateCapList');
const getKeysButton = document.querySelector('.GetKeys');



// EVENT LISTENER
//*************************************************************************
getCapListButton.addEventListener('click', () => {getCapList()})
updateCapListButton.addEventListener('click', () => {updateCapList()})
getKeysButton.addEventListener('click', () => {getKeys()})

// ON CHAIN FUNCTIONS 
//*************************************************************************
async function getCapList(){
  var result = await contract.methods.getCapabilityListByAddress(window.userWalletAddress)
              .call()
              .catch((e) => {
                console.error(e.message)
                return
              })
  console.log(result)

  cap = _capHash(result)
  new_cap = window.resourcesToBuy
  data_to_upload = []
  for (const el of new_cap){
    hash = sha3_256(el)
    if (!cap.includes(hash)){data_to_upload.push(el)}
  }
  
  window.newCap = data_to_upload
}


async function updateCapList(){
  
  const tx = contract.methods.buyResources(window.newCap)
  const gas = await tx.estimateGas({from: window.userWalletAddress})
  const gasPrice = await window.web3.eth.getGasPrice()
  const data = tx.encodeABI()
  const nonce = await window.web3.eth.getTransactionCount(window.userWalletAddress)
  const networkId = await window.web3.eth.net.getId()

  var params= [
    {
      from : window.userWalletAddress,
      to : contractAddress,
      data,
      gas : gas.toString(),
      gasPrice: gasPrice.toString(),
      nonce:nonce.toString(),
      chainId: networkId.toString(),
      value:(100).toString()
    },
  ]

  const result = await ethereum.request({
    method: 'eth_sendTransaction',
    params
  }).catch((e) => {
    console.log(e.message)
  })

  console.log(result)
}

async function getKeys(){
  res = await keys(_capHash(["a","e"]),window.userKey, window.userWalletAddress)
  console.log(res)
}

async function keys(_resources, _privKey, _from){
  var nodes = await contract.methods.getTokens(_from)
  .call()
  .catch((e) => {
    console.error(e.message)
    return
  })
  debugger
  nodes = _dataToStruct(nodes)
  //nodes = JSON.parse(nodes)  
  for(const node of nodes){
    token = (node.token).slice(2)
    label = await contract.methods.getLabel(node.id)
    .call()
    .catch((e) => {
      console.error(e.message)
      return
    })
    
    label = label.slice(2)
    nodeId = (node.id).slice(2)

    xor_Kl = bytesToHex(_byte_xor(hexToBytes(_privKey) , hexToBytes(label)))

    hash_Kl = hexToBytes(sha3_256(xor_Kl))
    nodekey = bytesToHex(_byte_xor(hexToBytes(token) , hash_Kl))
    
    if(_resources.includes(nodeId)){
      return {
        id: nodeId,
        key: nodekey
      }
    }else{
      return [{
        id: nodeId,
        key: nodekey
      },
      await keys(_resources,nodekey,node.id)]
    
      //.push(await keys(_resources,nodekey,node.id))
    }

  }

  return 
}

function _dataToStruct(_data){
  let nodes = []
  for(let i = 0; i < _data.length; i++){
    const node = {
      id : _data[i].id,
      token : _data[i].token
    }
    nodes.push(node)
  }
  return nodes
}

function _byte_xor(_ba1,_ba2){
  zip= rows=>rows[0].map((_,c)=>rows.map(row=>row[c]))
  var ret = new Uint8Array(32)
  var comb = zip([_ba1,_ba2])
  for(var ret = new Uint8Array(32), i=0; i < comb.length; i++){
    ret[i] = comb[i][0] ^ comb[i][1]
  }

  return ret
}

/*
const hexToBytes = hexString =>
  new Uint8Array(hexString.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));

  const bytesToHex = bytes =>
  Array.from(bytes).reduce((str, byte) => str + byte.toString(16).padStart(2, '0'), '');
*/

// CONNECTION TO METAMASK
//*************************************************************************
function handleAccountsChanged(accounts){
  if(accounts.length === 0){
    if (!window.ethereum){
      metaButton.innerText = "MetaMask not installed!"
      metaButton.classList.remove("btn-outline-success")
      metaButton.classList.add("btn-outline-danger","disabled")
      return false
    }
  
    metaButton.addEventListener('click', () =>{logInMetaMask()})
  }else{
    window.userWalletAddress = accounts[0]
  } 


}

async function logInMetaMask(){
  const accounts =  await window.ethereum.request({method: 'eth_requestAccounts'})
  .catch((e) => {
    console.error(e.message)
    return
  })
  if (!accounts) {return}
  window.userWalletAddress = accounts[0]
}


window.addEventListener('DOMContentLoaded',() => {
    ethereum
        .request({ method: 'eth_accounts' })
        .then(handleAccountsChanged)
        .catch(console.error);
});

//UTILITY
//*************************************************************************
function _capHash(capabilityList){
  hashed_res = []
  for (const el of capabilityList){
    hashed_res.push(sha3_256(el))
  }
  
  return hashed_res
}

Array.prototype.diff = function(dest) {return this.filter(x => !dest.includes(x));}

// Convert a hex string to a byte array
function hexToBytes(hex) {
  for (var bytes = [], c = 0; c < hex.length; c += 2)
      bytes.push(parseInt(hex.substr(c, 2), 16));
  return bytes;
}

// Convert a byte array to a hex string
function bytesToHex(bytes) {
  for (var hex = [], i = 0; i < bytes.length; i++) {
      var current = bytes[i] < 0 ? bytes[i] + 256 : bytes[i];
      hex.push((current >>> 4).toString(16));
      hex.push((current & 0xF).toString(16));
  }
  return hex.join("");
}