const ropsten_url = "https://ropsten.infura.io/v3/36f070bc6251423c8466175d6a49ec77"
const ganache_url = "http://127.0.0.1:8545"
window.web3 = new Web3(ganache_url);
window.userWalletAddress = null
window.TestGas = []
window.CurrentResourceIdx = 0
window.Resources =  ['28307', '7061', '10892', '49355', '8323', '15054', '43651', '29676', '23219', '28116', '3107', '32675', '23490', '18008', '8538', '27200', '6513', '949', '31151', '13108', '6823', 
'5180', '7013', '22242', '33162', '41703', '6749', '24272', '13736', '40419', '8947', '34058', '1851', '2045', '11241', '47473', '5716', '94', '29767', '5877', '43064', '1975', '47591', '36278', '49413', '7612', '26224', '15314', '29755', '18901', '38728', '12617', '32795', '43799', '32277', '5173', '3407', '27402', '40941', '19600', '36554', '1891', '24023', '39681', '35569', '22849', '48567', '8448', '46649', '43298', '12637', '20504', '11300', '2927', '23195', '31980', '1360', '30203', '3093', '21844', '13498', '36429', '2471', '39937', 
'41827', '41536', '24265', '6464', '15300', '44588', '33521', '16808', '10793', '43793', '28281', '5251', '38887', '26179', '32662', '36343']
window.timeDelta = []

//-----------------------------------------------------
// data for testing
window.resourcesToBuy = []
window.secretKey = ""
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
        "name": "BoughtResources",
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
        "indexed": false,
        "internalType": "bytes32",
        "name": "KDS_Hash",
        "type": "bytes32"
      }
    ],
    "name": "UpdateKDS",
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
        "internalType": "bytes32",
        "name": "_newKDS_Hash",
        "type": "bytes32"
      }
    ],
    "name": "updateKDS_Hash",
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
  }
]

const contractAddress = document.getElementById("contractAddress").textContent
const contract = new window.web3.eth.Contract(ABI,contractAddress)



const metaButton = document.querySelector('.connectoToMetaMask');
const getCapListButton = document.querySelector('.getCapList');
const updateCapListTestingButton = document.querySelector('.UpdateCapListTesting');
const updateCapListButton = document.querySelector('.UpdateCapList');
const getKeysButton = document.querySelector('.GetKeys');
const privKeyButton = document.querySelector('.privKeyBTN');
const printDataButton = document.querySelector('.PrintData');
const loopBtn = document.querySelector("#loopValues");




// EVENT LISTENER
//*************************************************************************
getCapListButton.addEventListener('click', () => {getCapList()})
updateCapListTestingButton.addEventListener('click', async () => {
  while(window.CurrentResourceIdx < 20){
    await updateCapListTesting()
  }

  console.log(window.timeDelta)
})
updateCapListButton.addEventListener('click', () => {updateCapList()})
getKeysButton.addEventListener('click', () => {getKeys()})
privKeyButton.addEventListener('click',getprivKey,false)
printDataButton.addEventListener('click', () => {
  let output = 'index,gas\n'
  for(const [idx,value] of window.TestGas.entries()){
    output += (idx+1).toString()+','+value+'\n'
  }
  console.log(output)
})

var states= [1, 10, 50];
var index = 0;
loopBtn.addEventListener('click', () => {
  index++;
  document.getElementById('loopValues').textContent = states[index%3];
})



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
  
  
  document.getElementById('modal-cap-Data').textContent = result
  document.getElementById('modal-cap-Title').textContent = "Bought Resources"
  return result
}

async function updateCapList(){
  
  new_cap = document.getElementById('buyResources').value
  if(new_cap){
    cap = _capHash(await getCapList())
    new_cap = new_cap.split(",").map(String)
    console.log("Buying : "+new_cap)
  
    data_to_upload = []
    for (const el of new_cap){
      hash = sha3_256(el)
      if (!cap.includes(hash)){data_to_upload.push(el)}
    }
  
    const tx = contract.methods.buyResources(data_to_upload)
    const gas = await tx.estimateGas({from: window.userWalletAddress})
    console.log("Estimated gas: "+gas)
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
  
    const txhash = await window.ethereum.request({
      method: 'eth_sendTransaction',
      params
    }).catch((e) => {
      console.log(e.message)
    })
  
    console.log(txhash)
    var txGas = (await web3.eth.getTransaction(txhash))//.gas
    //window.TestGas.push(txGas)
    console.log(txGas)
  }
}

async function updateCapListTesting(){
  cap = _capHash(await getCapList())
  increment = parseInt(document.getElementById('loopValues').textContent)
  dimension = parseInt(document.getElementById('loopValues').textContent)
  //new_cap = Array(dimension).fill().map((x,i)=>(i+window.CurrentResource).toString())
  new_cap = window.Resources.slice(window.CurrentResourceIdx,window.CurrentResourceIdx+dimension)
  console.log("Buying : "+new_cap)
  window.CurrentResourceIdx += increment

  data_to_upload = []
  for (const el of new_cap){
    hash = sha3_256(el)
    if (!cap.includes(hash)){data_to_upload.push(el)}
  }
  
  const nonce = await window.web3.eth.getTransactionCount(window.userWalletAddress)
  data = contract.methods.buyResources(data_to_upload)
  const gasPrice = await window.web3.eth.getGasPrice()
  const gas = await data.estimateGas({from: window.userWalletAddress})
  console.log("Estimated gas: "+gas)
  txObj = {
    nonce: web3.utils.toHex(parseInt(nonce)),
    to: contractAddress,
    //maxFeePerGas : (2 * parseInt(gasPrice)*10**-9) +  parseInt('2.5'),
    maxPriorityFeePerGas : web3.utils.toHex(web3.utils.toWei('27000','gwei')),
    //gas: gas,
    //value: web3.utils.toWei('1', 'wei'),
    gasLimit: web3.utils.toHex(2100000),
    gasPrice: web3.utils.toHex(gasPrice),
    data : data.encodeABI(),
    //value: web3.utils.toHex(web3.utils.toWei((540000*dimension).toString(), 'gwei'))
  }
  

  var tx = new ethereumjs.Tx(txObj)
  privateKey = new ethereumjs.Buffer.Buffer('3d9c07817ad0af82ef569eb8954c689b7ca8745e9016a29643f534849181aed3', 'hex');
  tx.sign(privateKey)
  var serializedTx = tx.serialize()

  txtTime = {}
  time = Math.floor(Date.now()/1000)
  receipt = await window.web3.eth.sendSignedTransaction('0x'+serializedTx.toString('hex'))


  console.log(receipt)
  txtTime['transactionHash'] = receipt['transactionHash']
  txtTime['blockHash'] = receipt['blockHash']
  
  window.TestGas.push(receipt["gasUsed"])

  //var txGas = (await web3.eth.getTransaction(receipt["transactionHash"]))
  var block = await web3.eth.getBlock(receipt["blockNumber"])

  console.log("Start Time: "+time.HumanTime())
  console.log("End time: "+block['timestamp'].HumanTime())
  delta = Math.abs((block["timestamp"]) - time)
  txtTime['delta'] = delta.toHHMMSS()
  console.log(txtTime['delta'])

  window.timeDelta.push(txtTime)

}


async function getKeys(){
  document.getElementById('modal-keys-Title').textContent = "Resource Keys"
  data = document.getElementById('getKeysInput').value
  
  if(data && window.secretKey){
    data = data.split(",").map(String)
    data = _capHash(data)
    
    
    var root = await contract.methods.getTokens("0x"+mapping[window.userWalletAddress])
    .call()
    .catch((e) => {
      console.error(e.message)
      return
    })
    root = _dataToStruct(root)
    root = root.filter((obj) => obj.token !== "0x0000000000000000000000000000000000000000000000000000000000000000");
    
    
    await getKeysFromRequestedData(data,window.secretKey,root[0]).then(result => {
      result = result.filter((value, index, self) =>
        index === self.findIndex((t) => (
          t.id === value.id && t.key === value.key
        ))
      )

      var table = document.getElementById('modal-keys-Data')
      while(table.rows.length > 1){
        table.deleteRow(1);
      }

      for(let idx = 0; idx <= result.length-1; idx++){
        id = Object.keys(mapping).find(key => mapping[key] === result[idx]['id']);
        var row = table.insertRow(idx+1);
        var idR = row.insertCell(0);
        var keyR = row.insertCell(1);
        idR.innerHTML = id;
        keyR.innerHTML = result[idx]['key'];
      }
    })
    
    
    //res = await getAllKeys(window.userKey,root[0],Keys)
 
    
    
  }


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


async function getKeysFromRequestedData(_data, _privKey, _node,_result = []){
  debugger
  if(_data.length > 0){
      label = await contract.methods.getLabel(_node.id)
    .call()
    .catch((e) => {
      console.error(e.message)
    })
    
    token = (_node.token).slice(2)
    label = label.slice(2)
    nodeId = (_node.id).slice(2)
    const nodeKey = _createNodeKey(_privKey,label,token)

    //console.log("id:\t"+nodeId,"key:\t"+nodeKey)
    
    if(_data.includes(nodeId)){
      _result.push( {
        id: nodeId,
        key: nodeKey
      })
      _data = _data.diff(nodeId)
    }

    
    var nodes = await contract.methods.getTokens("0x"+nodeId)
    .call()
    .catch((e) => {
      console.error(e.message)
    })
    childrens = _dataToStruct(nodes)
    
    if(childrens.length > 0){
      for(const child of childrens){
        if(child.token != "0x0000000000000000000000000000000000000000000000000000000000000000"){
          _result = await getKeysFromRequestedData(_data,nodeKey,child,_result)
        }
      }
    }

  }
  

  return _result
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
  window.secretKey = document.getElementById('privKey').value
  
  if(window.secretKey != ""){
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

window.ethereum.on('accountsChanged', function (accounts) {
  console.log("account changed : "+accounts[0])
  window.userWalletAddress = accounts[0]
})

//UTILITY
//*************************************************************************
function _capHash(capabilityList){
  hashed_res = []
  for (const el of capabilityList){
    hashed_res.push(mapping[el])
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

Number.prototype.toHHMMSS = function () {
  var sec_num = parseInt(this, 10); // don't forget the second param
  var hours   = Math.floor(sec_num / 3600);
  var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
  var seconds = sec_num - (hours * 3600) - (minutes * 60);

  if (hours   < 10) {hours   = "0"+hours;}
  if (minutes < 10) {minutes = "0"+minutes;}
  if (seconds < 10) {seconds = "0"+seconds;}
  return hours+':'+minutes+':'+seconds;
}

Number.prototype.HumanTime = function(){
  let unix_timestamp = this
// Create a new JavaScript Date object based on the timestamp
// multiplied by 1000 so that the argument is in milliseconds, not seconds.
var date = new Date(unix_timestamp * 1000);
// Hours part from the timestamp
var hours = date.getHours();
// Minutes part from the timestamp
var minutes = "0" + date.getMinutes();
// Seconds part from the timestamp
var seconds = "0" + date.getSeconds();

// Will display time in 10:30:23 format
return formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);

}

function _deltaToCSV(){
  out =""
  for(const el of window.timeDelta){
    out += el['transactionHash']+","+el['blockHash']+","+el["delta"]+"\n"
  }

  console.log(out)
}


