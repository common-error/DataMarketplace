// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract accessAuth is Ownable(){

    
    struct updateData{
        bytes2 from;
        bytes2 to;
        bytes32 token;
        bytes32 label;
    }

    struct node{
        bytes2 id;
        bytes32 token;
    }

    mapping(bytes2 => node[]) catalogue;
    mapping(address => string[]) capabilityList;
    mapping(bytes32 => bytes32) labels;

    event CapabilityListUpdated(
        address indexed _buyer,
        uint price,
        string[] BoughtResources
    );

    event UpdateData(updateData[]);


    /** 
       @notice Updates a user's capability list (after a payment) adding the new purchased resources to the list. The ETH tokens are directly transfered to the owner of the contract. The capability list is a list of strings where a string identifies a resource
       @param _resources List of strings
    */
    function buyResources(string[] memory _resources) external payable {
        //string[] memory oldCap = capabilityList[msg.sender];
        uint arrayLen = _resources.length;
        for(uint i=0; i < arrayLen; i++){
            capabilityList[msg.sender].push(_resources[i]); 
        }
        
        payable(owner()).transfer(msg.value);

        emit CapabilityListUpdated(msg.sender, msg.value,_resources);
    }


    /**
        @notice Thanks to the changes in the local KDS the catalog is updated allowing a buyer to access the recources according to his capability list. It also adds the labels for the key derivation.
        @param _updateData List of tuple of the form: (from,to,token,label)
     */
    function updateCatalogue(updateData[] memory _updateData) onlyOwner() external{
        node memory tempNode;
        uint idx;
        uint arrayLen = _updateData.length;
        node[] memory tempCatalogue;

        for(uint i=0; i < arrayLen; i++){
            bytes2 from = _updateData[i].from;
            bytes2 to = _updateData[i].to;
            tempCatalogue = catalogue[from];

            tempNode.id = to;
            tempNode.token = _updateData[i].token;
            (tempNode,idx) = _updateElementsInNode(tempCatalogue,tempNode);

            if(idx > tempCatalogue.length){
                catalogue[from].push(tempNode);
            }else{
                catalogue[from][idx] = tempNode;
            }

            
            labels[to] = _updateData[i].label;
            
            
        }

        emit UpdateData(_updateData);
    }

    /**
        @notice A node can have a bunch of nodes connected to it. This function tries to find if a new node (_data) is already connected and then the value is changed, otherwise it must be pushed as a new node.
        @param _node List of nodes connected to a parent node. For example the node "abc" may be connected to the nodes "a,b,c"
        @param _data Data of a node that needs to be changed or added
        @return A tuple with the node and the position index 
    */
    function _updateElementsInNode(node[] memory _node,node memory _data) private pure returns(node memory,uint){
        uint len = _node.length;
        for(uint i=0; i < len; i++){
            if(_node[i].id == _data.id){
                //_node[i].token = _data.token;
                return (_data,i);
            }
        }

        return (_data,_node.length+1);
    }

    function getCapabilityListByAddress(address _buyer) external view returns(string[] memory) {
        return capabilityList[_buyer];
    }

    function getTokens(bytes2 _from) external view returns(node[] memory){
        return catalogue[_from];
    }

    function getLabel(bytes32 _edge) external view returns(bytes32){
        return labels[_edge];
    }


}