import { ethers } from "ethers";

const abi = [
  // Constructor
  "constructor(address registry)",

  // Errors
  "error AccessDenied()",
  "error AlreadyRevoked()",
  "error AlreadyRevokedOffchain()",
  "error AlreadyTimestamped()",
  "error InsufficientValue()",
  "error InvalidAttestation()",
  "error InvalidAttestations()",
  "error InvalidExpirationTime()",
  "error InvalidLength()",
  "error InvalidOffset()",
  "error InvalidRegistry()",
  "error InvalidRevocation()",
  "error InvalidRevocations()",
  "error InvalidSchema()",
  "error InvalidSignature()",
  "error InvalidVerifier()",
  "error Irrevocable()",
  "error NotFound()",
  "error NotPayable()",
  "error WrongSchema()",

  // Events
  "event Attested(address indexed recipient, address indexed attester, bytes32 uid, bytes32 indexed schema)",
  "event Revoked(address indexed recipient, address indexed attester, bytes32 uid, bytes32 indexed schema)",
  "event RevokedOffchain(address indexed revoker, bytes32 indexed data, uint64 indexed timestamp)",
  "event Timestamped(bytes32 indexed data, uint64 indexed timestamp)",

  // View Functions
  "function VERSION() view returns (string)",
  "function getAttestTypeHash() pure returns (bytes32)",
  "function getAttestation(bytes32 uid) view returns (tuple(bytes32 uid, bytes32 schema, uint64 time, uint64 expirationTime, uint64 revocationTime, bytes32 refUID, address recipient, address attester, bool revocable, bytes data))",
  "function getDomainSeparator() view returns (bytes32)",
  "function getNonce(address account) view returns (uint256)",
  "function getRevokeOffchain(address revoker, bytes32 data) view returns (uint64)",
  "function getRevokeTypeHash() pure returns (bytes32)",
  "function getSchemaRegistry() view returns (address)",
  "function getTimestamp(bytes32 data) view returns (uint64)",
  "function isAttestationValid(bytes32 uid) view returns (bool)",

  // Attestation Functions
  "function attest(tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value) data) request) payable returns (bytes32)",
  "function attestByDelegation(tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value) data, tuple(uint8 v, bytes32 r, bytes32 s) signature, address attester) delegatedRequest) payable returns (bytes32)",
  "function multiAttest(tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value)[] data)[] multiRequests) payable returns (bytes32[])",
  "function multiAttestByDelegation(tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value)[] data, tuple(uint8 v, bytes32 r, bytes32 s)[] signatures, address attester)[] multiDelegatedRequests) payable returns (bytes32[])",

  // Revocation Functions
  "function revoke(tuple(bytes32 schema, tuple(bytes32 uid, uint256 value) data) request) payable",
  "function revokeByDelegation(tuple(bytes32 schema, tuple(bytes32 uid, uint256 value) data, tuple(uint8 v, bytes32 r, bytes32 s) signature, address revoker) delegatedRequest) payable",
  "function multiRevoke(tuple(bytes32 schema, tuple(bytes32 uid, uint256 value)[] data)[] multiRequests) payable",
  "function multiRevokeByDelegation(tuple(bytes32 schema, tuple(bytes32 uid, uint256 value)[] data, tuple(uint8 v, bytes32 r, bytes32 s)[] signatures, address revoker)[] multiDelegatedRequests) payable",
  "function revokeOffchain(bytes32 data) returns (uint64)",
  "function multiRevokeOffchain(bytes32[] data) returns (uint64)",

  // Timestamp Functions
  "function timestamp(bytes32 data) returns (uint64)",
  "function multiTimestamp(bytes32[] data) returns (uint64)",
];

export const EAS_INTERFACE = new ethers.Interface(abi);
