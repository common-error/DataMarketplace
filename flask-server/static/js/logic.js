const ganache_url = "http://127.0.0.1:8545"
window.web3 = new Web3(ganache_url);
window.userWalletAddress = null


//-----------------------------------------------------
// data for testing
window.resourcesToBuy = ["0","1","2","3","4","5","6","7","8","9","10"]
window.userKey = ""
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
const privKeyButton = document.querySelector('.privKeyBTN');



// EVENT LISTENER
//*************************************************************************
getCapListButton.addEventListener('click', () => {getCapList()})
updateCapListButton.addEventListener('click', () => {updateCapList()})
getKeysButton.addEventListener('click', () => {getKeys()})
privKeyButton.addEventListener('click',getprivKey,false)

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

  return result
}


async function updateCapList(){
  cap = _capHash(await getCapList())
  new_cap = window.resourcesToBuy
  data_to_upload = []
  for (const el of new_cap){
    hash = sha3_256(el)
    if (!cap.includes(hash)){data_to_upload.push(el)}
  }

  const tx = contract.methods.buyResources(data_to_upload)
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
      gasPrice: "350000000",
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
  data = _capHash(["1","23","101"])
  
  Keys = []
  var root = await contract.methods.getTokens(window.userWalletAddress)
  .call()
  .catch((e) => {
    console.error(e.message)
    return
  })
  root = _dataToStruct(root)
  
  res = await getKeysFromRequestedData(data,window.userKey,root[0],Keys)
  //res = await getAllKeys(window.userKey,root[0],Keys)
  console.log(Keys)
}

async function getAllKeys(_privKey, _node,_dictKeys){
  label = await contract.methods.getLabel(_node.id)
  .call()
  .catch((e) => {
    console.error(e.message)
    return
  })
  
  token = (_node.token).slice(2)
  label = label.slice(2)
  nodeId = (_node.id).slice(2)
  nodeKey = _createNodeKey(_privKey,label,token)
  
  _dictKeys["id"] = nodeId
  _dictKeys["key"] = nodeKey
  _dictKeys["children"] = []

  var nodes = await contract.methods.getTokens("0x"+nodeId)
  .call()
  .catch((e) => {
    console.error(e.message)
    return
  })
  childrens = _dataToStruct(nodes)

  for(const child of childrens){
    if(child.token != "0x0000000000000000000000000000000000000000000000000000000000000000"){
      child_dict = Object.create(null)
      getAllKeys(nodeKey,child,child_dict)
      _dictKeys["children"].push(child_dict)
    }
  }
  
  }


async function getKeysFromRequestedData(_data, _privKey, _node,_dictKeys){
  
  if(_data.length > 0){
    label = await contract.methods.getLabel(_node.id)
    .call()
    .catch((e) => {
      console.error(e.message)
      return
    })
    
    token = (_node.token).slice(2)
    label = label.slice(2)
    nodeId = (_node.id).slice(2)
    nodeKey = _createNodeKey(_privKey,label,token)

    //console.log("id:\t"+nodeId,"key:\t"+nodeKey)
    
    if(_data.includes(nodeId)){
      _dictKeys.push({
        id: nodeId,
        key: nodeKey
      })

      _data = _data.diff(nodeId)
    }
  
    var nodes = await contract.methods.getTokens("0x"+nodeId)
    .call()
    .catch((e) => {
      console.error(e.message)
      return
    })
    childrens = _dataToStruct(nodes)
  
    for(const child of childrens){
      if(child.token != "0x0000000000000000000000000000000000000000000000000000000000000000"){
        child_dict = []
        getKeysFromRequestedData(_data,nodeKey,child,_dictKeys)
      }
    }
  }
}

function _createNodeKey(_privKey,_label,_token){
  xor_Kl = bytesToHex(_byte_xor(hexToBytes(_privKey) , hexToBytes(_label)))

  hash_Kl = hexToBytes(sha3_256(xor_Kl))
  nodekey = bytesToHex(_byte_xor(hexToBytes(_token) , hash_Kl))

  return nodekey
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

function getprivKey(){
  window.userKey = document.getElementById('privKey').value
  debugger
  if(window.userKey != ""){
    privKeyButton.classList.remove("btn-outline-danger")
    privKeyButton.classList.add("btn-outline-success")
    document.getElementById('privKey').value = ""
  }

}

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