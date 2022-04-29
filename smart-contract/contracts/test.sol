// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract test is Ownable(){

    struct catalogueEntry{
        bytes32 from;
        bytes32 to;
        bytes32 token;
    }

    mapping(bytes32 => mapping(bytes32 => bytes32)) catalogue;
    mapping(address => string[]) capabilityList;

    event capabilityListUpdated(
        address indexed _buyer,
        uint price,
        string[] oldCababilityList,
        string[] newCapabilityList
    );
    event CatalogueUpdated(catalogueEntry[] _resources);


    function buyResources(string[] memory _resources) external payable {
        string[] memory oldCap = capabilityList[msg.sender];

        for(uint i=0; i < _resources.length; i++){
            capabilityList[msg.sender].push(_resources[i]); 
        }
        
        payable(owner()).transfer(msg.value);

        emit capabilityListUpdated(msg.sender, msg.value, oldCap,capabilityList[msg.sender]);
    }

    function updateCatalogue(catalogueEntry[] memory _catalogueEntries) onlyOwner() external{

        for(uint i=0; i < _catalogueEntries.length; i++){
            bytes32 from = _catalogueEntries[i].from;
            bytes32 to = _catalogueEntries[i].to;
            catalogue[from][to] = _catalogueEntries[i].token;
        }

        emit CatalogueUpdated(_catalogueEntries);
    }

    function getCapabilityListByAddress(address _buyer) external view returns(string[] memory) {
        return capabilityList[_buyer];
    }

    function getToken(bytes32 _from, bytes32 _to) external view returns(bytes32){
        return catalogue[_from][_to];
    }


}