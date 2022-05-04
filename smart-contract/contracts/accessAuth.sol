// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract accessAuth is Ownable(){

    struct updateData{
        bytes32 from;
        bytes32 to;
        bytes32 token;
        bytes32 label;
    }

    struct node{
        bytes32 id;
        bytes32 token;
    }

    mapping(bytes32 => node[]) catalogue;
    mapping(address => string[]) capabilityList;
    mapping(bytes32 => bytes32) labels;

    event CapabilityListUpdated(
        address indexed _buyer,
        uint price,
        string[] oldCababilityList,
        string[] newCapabilityList
    );

    event UpdateData(updateData[]);


    function buyResources(string[] memory _resources) external payable {
        string[] memory oldCap = capabilityList[msg.sender];

        for(uint i=0; i < _resources.length; i++){
            capabilityList[msg.sender].push(_resources[i]); 
        }
        
        payable(owner()).transfer(msg.value);

        emit CapabilityListUpdated(msg.sender, msg.value, oldCap,capabilityList[msg.sender]);
    }

    function updateCatalogue(updateData[] memory _updateData) onlyOwner() external{
        node memory tempNode;
        uint idx;

        for(uint i=0; i < _updateData.length; i++){
            bytes32 from = _updateData[i].from;
            bytes32 to = _updateData[i].to;

            tempNode.id = to;
            tempNode.token = _updateData[i].token;
            (tempNode,idx) = _updateElementsInNode(catalogue[from],tempNode);

            if(idx > catalogue[from].length){
                catalogue[from].push(tempNode);
            }else{
                catalogue[from][idx] = tempNode;
            }

            labels[to] = _updateData[i].label;
        }

        emit UpdateData(_updateData);
    }


    function _updateElementsInNode(node[] memory _node,node memory _data) private pure returns(node memory,uint){
        for(uint i=0; i < _node.length; i++){
            if(_node[i].id == _data.id){
                _node[i].token = _data.token;
                return (_data,i);
            }
        }

        return (_data,_node.length+1);
    }

    function getCapabilityListByAddress(address _buyer) external view returns(string[] memory) {
        return capabilityList[_buyer];
    }

    function getTokens(bytes32 _from) external view returns(node[] memory){
        return catalogue[_from];
    }

    function getLabel(bytes32 _edge) external view returns(bytes32){
        return labels[_edge];
    }


}