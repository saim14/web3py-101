// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {

    uint256 favouriteNumber;

    struct People {
        uint256 favouriteNumber;
        string name;
    }

    People[] public people; // Array type
    mapping(string => uint256) public nameToFavouriteNumber; // Python Dictionary type

    function store(uint256 _favouriteNumber) public returns(uint256){
        favouriteNumber = _favouriteNumber;
        return _favouriteNumber;
    }

    function get() public view returns(uint256){ // no transaction/gas need to provided for view keyword
        return favouriteNumber;
    }
    
    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People( _favouriteNumber, _name)); // pushing to the array
        nameToFavouriteNumber[_name] = _favouriteNumber; // adding to the dictionary 
    }
}