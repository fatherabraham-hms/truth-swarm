// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import {SchemaResolver} from "../lib/eas-contracts/contracts/resolver/SchemaResolver.sol";
import {IEAS} from "../lib/eas-contracts/contracts/IEAS.sol";



/// @title AttesterResolver
/// @notice A sample schema resolver that checks whether the attestation is from a specific attester.
contract AttesterResolver is SchemaResolver {
    address[] private immutable _targetAttesters;

    constructor(IEAS eas, address[] memory targetAttesters) SchemaResolver(eas) {
        _targetAttesters = targetAttesters;
    }

    function getTargetAttesters() external view returns (address[] memory) {
        return _targetAttesters;
    }
    function add_attesters(address new_attester) external {
        _targetAttesters.push(new_attester);
    }

    function onAttest(Attestation calldata attestation, uint256 /*value*/) internal view override returns (bool) {
        for (uint256 i = 0; i < _targetAttesters.length; i++) {
            if (attestation.attester == _targetAttesters[i]) {
                return true;
            }
        }
        return false;
    }
/// Not used in this resolver, so we just return true.
    function onRevoke(Attestation calldata /*attestation*/, uint256 /*value*/) internal pure override returns (bool) {
        return true;
    }
}