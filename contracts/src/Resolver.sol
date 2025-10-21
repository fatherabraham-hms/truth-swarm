// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {SchemaResolver} from "../lib/eas-contracts/contracts/resolver/SchemaResolver.sol";
import {IEAS, Attestation} from "../lib/eas-contracts/contracts/IEAS.sol";
import {Ownable} from "../lib/openzeppelin-contracts/contracts/access/Ownable.sol";

/// @title TruthSwarmResolver
/// @notice A schema resolver that validates attestations from whitelisted agents
/// @dev Implements a whitelist pattern with owner-controlled access management
contract TruthSwarmResolver is SchemaResolver, Ownable {
    /// @notice Emitted when an attester is added to the whitelist
    event AttesterAdded(address indexed attester);

    /// @notice Emitted when an attester is removed from the whitelist
    event AttesterRemoved(address indexed attester);

    /// @notice Mapping of whitelisted attesters
    mapping(address => bool) private _whitelistedAttesters;

    /// @notice Array to track all whitelisted addresses for enumeration
    address[] private _attesterList;

    /// @notice Thrown when trying to add an already whitelisted attester
    error AttesterAlreadyWhitelisted(address attester);

    /// @notice Thrown when trying to remove a non-whitelisted attester
    error AttesterNotWhitelisted(address attester);

    /// @notice Thrown when zero address is provided
    error ZeroAddress();

    /// @notice Initializes the resolver with EAS instance and initial whitelist
    /// @param eas The EAS contract instance
    /// @param initialAttesters Array of addresses to be initially whitelisted
    constructor(IEAS eas, address[] memory initialAttesters) SchemaResolver(eas) Ownable(msg.sender) {
        for (uint256 i = 0; i < initialAttesters.length; i++) {
            address attester = initialAttesters[i];
            if (attester != address(0) && !_whitelistedAttesters[attester]) {
                _whitelistedAttesters[attester] = true;
                _attesterList.push(attester);
                emit AttesterAdded(attester);
            }
        }
    }

    /// @notice Adds an attester to the whitelist
    /// @param attester The address to whitelist
    function addAttester(address attester) external onlyOwner {
        if (attester == address(0)) revert ZeroAddress();
        if (_whitelistedAttesters[attester]) revert AttesterAlreadyWhitelisted(attester);

        _whitelistedAttesters[attester] = true;
        _attesterList.push(attester);
        emit AttesterAdded(attester);
    }

    /// @notice Removes an attester from the whitelist
    /// @param attester The address to remove
    function removeAttester(address attester) external onlyOwner {
        if (!_whitelistedAttesters[attester]) revert AttesterNotWhitelisted(attester);

        _whitelistedAttesters[attester] = false;

        // Remove from array (swap with last element and pop)
        for (uint256 i = 0; i < _attesterList.length; i++) {
            if (_attesterList[i] == attester) {
                _attesterList[i] = _attesterList[_attesterList.length - 1];
                _attesterList.pop();
                break;
            }
        }

        emit AttesterRemoved(attester);
    }

    /// @notice Checks if an address is whitelisted
    /// @param attester The address to check
    /// @return True if the address is whitelisted
    function isWhitelisted(address attester) external view returns (bool) {
        return _whitelistedAttesters[attester];
    }

    /// @notice Returns all whitelisted attesters
    /// @return Array of whitelisted addresses
    function getWhitelistedAttesters() external view returns (address[] memory) {
        return _attesterList;
    }

    /// @notice Returns the number of whitelisted attesters
    function getWhitelistedCount() external view returns (uint256) {
        return _attesterList.length;
    }

    /// @notice Validates attestations from whitelisted attesters only
    /// @param attestation The attestation data
    /// @return True if attestation is from a whitelisted attester
    function onAttest(
        Attestation calldata attestation,
        uint256 /*value*/
    )
        internal
        view
        override
        returns (bool)
    {
        return _whitelistedAttesters[attestation.attester];
    }

    /// @notice Validates revocations (currently allows all)
    /// @dev Override this if you need custom revocation logic
    function onRevoke(
        Attestation calldata,
        /*attestation*/
        uint256 /*value*/
    )
        internal
        pure
        override
        returns (bool)
    {
        return true;
    }
}
