// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract accessAuth is Ownable(){

    struct catalogueEntry{
        string from;
        string to;
        bytes32 token;
    }

    mapping(bytes32 => mapping(bytes32 => bytes32)) catalogue;
    mapping(address => uint[]) capabilityList;

    event capabilityListUpdated(
        address indexed _buyer,
        uint price,
        uint[] oldCababilityList,
        uint[] newCapabilityList
    );
    event CatalogueUpdated(catalogueEntry[] _resources);


    function buyResources(uint[] memory _resources) external payable {
        uint[] memory oldCap = capabilityList[msg.sender];

        for(uint i=0; i < _resources.length; i++){
            capabilityList[msg.sender].push(_resources[i]); 
        }
        
        payable(owner()).transfer(msg.value);

        emit capabilityListUpdated(msg.sender, msg.value, oldCap,capabilityList[msg.sender]);
    }

    function updateCatalogue(catalogueEntry[] memory _catalogueEntries) onlyOwner() external{

        for(uint i=0; i < _catalogueEntries.length; i++){
            bytes32 from = keccak256(abi.encodePacked(_catalogueEntries[i].from));
            bytes32 to = keccak256(abi.encodePacked(_catalogueEntries[i].to));
            catalogue[from][to] = _catalogueEntries[i].token;
        }

        emit CatalogueUpdated(_catalogueEntries);
    }

    function getCapabilityListByAddress(address _buyer) external view returns(uint[] memory) {
        return capabilityList[_buyer];
    }

    function getToken(string memory _from, string memory _to) external view returns(bytes32){
        bytes32 from = keccak256(abi.encodePacked(_from));
        bytes32 to = keccak256(abi.encodePacked(_to));

        return catalogue[from][to];
    }


}