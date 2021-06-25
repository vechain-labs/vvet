// SPDX-License-Identifier: GPL-3.0-only
pragma solidity ^0.8.0;

// VTHO Box tracks the in-and-out of user's VET
// And updates user's vtho balance accordingly.

// It can also track the in-and-out of user's VTHO.

// uint104 - safe for vtho to operate another 100 years.
contract VTHOBox {

    struct User {
        uint40 lastUpdatedTime;
        uint104 vetBalance;
        uint104 vthoBalance;
    }

    mapping(address => User) private users;

    function addVET(address addr, uint104 amount) internal {
        _update(addr);
        users[addr].vetBalance += amount;
    }

    function removeVET(address addr, uint104 amount) internal {
        _update(addr);
        users[addr].vetBalance -= amount;
    }

    function vetBalance(address addr) public view returns (uint104 amount) {
        return users[addr].vetBalance;
    }

    function addVTHO(address addr, uint104 amount) internal {
        _update(addr);
        users[addr].vthoBalance += amount;
    }

    function removeVTHO(address addr, uint104 amount) internal {
        _update(addr);
        users[addr].vthoBalance -= amount;
    }

    function vthoBalance(address addr) public returns (uint104 amount) {
        _update(addr);
        return users[addr].vthoBalance;
    }

    // Sync the vtho balance that the address has
    // up till current block (timestamp)
    function _update(address addr) internal {
        if (users[addr].lastUpdatedTime > 0) {
            assert(users[addr].lastUpdatedTime <= uint40(block.timestamp));
            users[addr].vthoBalance += calculateVTHO(
                users[addr].lastUpdatedTime,
                uint40(block.timestamp),
                users[addr].vetBalance
            );
        }

        users[addr].lastUpdatedTime = uint40(block.timestamp);
    }

    // Calculate vtho generated between time t1 and t2
    // @param t1 Time in seconds
    // @param t2 Time in seconds
    // @param vetBalance VET in wei
    // @return vtho generated in wei
    function calculateVTHO(
        uint40 t1,
        uint40 t2,
        uint104 vetAmount
    ) public pure returns (uint104 vtho) {
        require(t1 < t2);
        return ((vetAmount * 5) / (10**9)) * (t2 - t1);
    }
}
