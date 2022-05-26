// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;
import "@openzeppelin/contracts/access/Ownable.sol";

contract accessAuth is Ownable(){

    bytes32 KDS_Hash;
    mapping(address => string[]) capabilityList;

    event CapabilityListUpdated(
        address indexed _buyer,
        uint price,
        string[] BoughtResources
    );

    event UpdateKDS(bytes32 KDS_Hash);


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
        @notice Updates the KDS's hash
        @param _newKDS_Hash Hash of the updated KDS
     */
    function updateKDS_Hash(bytes32 _newKDS_Hash) onlyOwner() external{
        KDS_Hash = _newKDS_Hash;
        emit UpdateKDS(_newKDS_Hash);
    }

    function getCapabilityListByAddress(address _buyer) external view returns(string[] memory) {
        return capabilityList[_buyer];
    }

    function getKDS_Hash() external view returns(bytes32){
        return KDS_Hash;
    }


}