// SPDX-License-Identifier: MIT

pragma solidity ^0.8.28;

import "./lib/eas-contracts/contracts/IEAS.sol";

/// @title MockEAS
/// @notice A simplified EAS implementation for testing
contract MockEAS is IEAS {
    mapping(bytes32 => Attestation) private _attestations;
    mapping(bytes32 => bool) private _attestationExists;
    
    ISchemaRegistry private _schemaRegistry;
    
    constructor() {
        // Initialize with a null registry - will be set later
    }
    
    function setSchemaRegistry(address registryAddress) external {
        _schemaRegistry = ISchemaRegistry(registryAddress);
    }
    
    function attest(AttestationRequest calldata request) external payable override returns (bytes32) {
        bytes32 uid = keccak256(abi.encodePacked(
            request.schema,
            request.data,
            request.expirationTime,
            request.revocable,
            request.refUID,
            request.value,
            request.deadline,
            request.recipient,
            msg.sender,
            block.timestamp
        ));
        
        Attestation memory attestation = Attestation({
            uid: uid,
            schema: request.schema,
            time: uint64(block.timestamp),
            expirationTime: request.expirationTime,
            revocationTime: 0,
            refUID: request.refUID,
            recipient: request.recipient,
            attester: msg.sender,
            revocable: request.revocable,
            data: request.data
        });
        
        _attestations[uid] = attestation;
        _attestationExists[uid] = true;
        
        emit Attested(
            uid,
            request.schema,
            msg.sender,
            request.recipient,
            request.expirationTime,
            request.revocable,
            request.refUID,
            request.data,
            request.value
        );
        
        return uid;
    }
    
    function attestByDelegation(AttestationRequestData calldata delegatedRequest) external payable override returns (bytes32) {
        // Simplified implementation for testing
        AttestationRequest memory request = AttestationRequest({
            schema: delegatedRequest.schema,
            data: delegatedRequest.data,
            expirationTime: delegatedRequest.expirationTime,
            revocable: delegatedRequest.revocable,
            refUID: delegatedRequest.refUID,
            value: delegatedRequest.value,
            deadline: delegatedRequest.deadline,
            recipient: delegatedRequest.recipient
        });
        
        return this.attest(request);
    }
    
    function revoke(RevocationRequest calldata request) external payable override {
        require(_attestationExists[request.uid], "Attestation does not exist");
        require(_attestations[request.uid].attester == msg.sender, "Not the attester");
        require(_attestations[request.uid].revocable, "Attestation is not revocable");
        
        _attestations[request.uid].revocationTime = uint64(block.timestamp);
    }
    
    function revokeByDelegation(RevocationRequestData calldata delegatedRequest) external payable override {
        RevocationRequest memory request = RevocationRequest({
            uid: delegatedRequest.uid,
            value: delegatedRequest.value,
            deadline: delegatedRequest.deadline
        });
        
        this.revoke(request);
    }
    
    function isAttestationValid(bytes32 uid) external view override returns (bool) {
        return _attestationExists[uid] && _attestations[uid].revocationTime == 0;
    }
    
    function getAttestation(bytes32 uid) external view override returns (Attestation memory) {
        require(_attestationExists[uid], "Attestation does not exist");
        return _attestations[uid];
    }
    
    function getSchemaRegistry() external view override returns (ISchemaRegistry) {
        return _schemaRegistry;
    }
}

/// @title MockSchemaRegistry
/// @notice A simplified schema registry for testing
contract MockSchemaRegistry is ISchemaRegistry {
    mapping(bytes32 => SchemaRecord) private _schemas;
    mapping(bytes32 => bool) private _schemaExists;
    
    function register(string calldata schema, bool revocable) external override returns (bytes32) {
        bytes32 uid = keccak256(abi.encodePacked(schema, revocable, msg.sender, block.timestamp));
        
        SchemaRecord memory record = SchemaRecord({
            uid: uid,
            schema: keccak256(bytes(schema)),
            revocable: revocable,
            registerer: msg.sender
        });
        
        _schemas[uid] = record;
        _schemaExists[uid] = true;
        
        emit Registered(uid, msg.sender, record);
        
        return uid;
    }
    
    function isRegistered(bytes32 uid) external view override returns (bool) {
        return _schemaExists[uid];
    }
    
    function getSchema(bytes32 uid) external view override returns (SchemaRecord memory) {
        require(_schemaExists[uid], "Schema does not exist");
        return _schemas[uid];
    }
}