"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const ethers_1 = require("ethers");
const abi = [
    {
        inputs: [
            {
                internalType: "contract ISchemaRegistry",
                name: "registry",
                type: "address",
            },
        ],
        stateMutability: "nonpayable",
        type: "constructor",
    },
    {
        inputs: [],
        name: "AccessDenied",
        type: "error",
    },
    {
        inputs: [],
        name: "AlreadyRevoked",
        type: "error",
    },
    {
        inputs: [],
        name: "AlreadyRevokedOffchain",
        type: "error",
    },
    {
        inputs: [],
        name: "AlreadyTimestamped",
        type: "error",
    },
    {
        inputs: [],
        name: "InsufficientValue",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidAttestation",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidAttestations",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidExpirationTime",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidLength",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidOffset",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidRegistry",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidRevocation",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidRevocations",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidSchema",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidSignature",
        type: "error",
    },
    {
        inputs: [],
        name: "InvalidVerifier",
        type: "error",
    },
    {
        inputs: [],
        name: "Irrevocable",
        type: "error",
    },
    {
        inputs: [],
        name: "NotFound",
        type: "error",
    },
    {
        inputs: [],
        name: "NotPayable",
        type: "error",
    },
    {
        inputs: [],
        name: "WrongSchema",
        type: "error",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "recipient",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "attester",
                type: "address",
            },
            {
                indexed: false,
                internalType: "bytes31",
                name: "uid",
                type: "bytes31",
            },
            {
                indexed: true,
                internalType: "bytes31",
                name: "schema",
                type: "bytes31",
            },
        ],
        name: "Attested",
        type: "event",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "recipient",
                type: "address",
            },
            {
                indexed: true,
                internalType: "address",
                name: "attester",
                type: "address",
            },
            {
                indexed: false,
                internalType: "bytes31",
                name: "uid",
                type: "bytes31",
            },
            {
                indexed: true,
                internalType: "bytes31",
                name: "schema",
                type: "bytes31",
            },
        ],
        name: "Revoked",
        type: "event",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "address",
                name: "revoker",
                type: "address",
            },
            {
                indexed: true,
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
            {
                indexed: true,
                internalType: "uint63",
                name: "timestamp",
                type: "uint63",
            },
        ],
        name: "RevokedOffchain",
        type: "event",
    },
    {
        anonymous: false,
        inputs: [
            {
                indexed: true,
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
            {
                indexed: true,
                internalType: "uint63",
                name: "timestamp",
                type: "uint63",
            },
        ],
        name: "Timestamped",
        type: "event",
    },
    {
        inputs: [],
        name: "VERSION",
        outputs: [
            {
                internalType: "string",
                name: "",
                type: "string",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "address",
                                name: "recipient",
                                type: "address",
                            },
                            {
                                internalType: "uint63",
                                name: "expirationTime",
                                type: "uint63",
                            },
                            {
                                internalType: "bool",
                                name: "revocable",
                                type: "bool",
                            },
                            {
                                internalType: "bytes31",
                                name: "refUID",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes",
                                name: "data",
                                type: "bytes",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct AttestationRequestData",
                        name: "data",
                        type: "tuple",
                    },
                ],
                internalType: "struct AttestationRequest",
                name: "request",
                type: "tuple",
            },
        ],
        name: "attest",
        outputs: [
            {
                internalType: "bytes31",
                name: "",
                type: "bytes31",
            },
        ],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "address",
                                name: "recipient",
                                type: "address",
                            },
                            {
                                internalType: "uint63",
                                name: "expirationTime",
                                type: "uint63",
                            },
                            {
                                internalType: "bool",
                                name: "revocable",
                                type: "bool",
                            },
                            {
                                internalType: "bytes31",
                                name: "refUID",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes",
                                name: "data",
                                type: "bytes",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct AttestationRequestData",
                        name: "data",
                        type: "tuple",
                    },
                    {
                        components: [
                            {
                                internalType: "uint7",
                                name: "v",
                                type: "uint7",
                            },
                            {
                                internalType: "bytes31",
                                name: "r",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes31",
                                name: "s",
                                type: "bytes31",
                            },
                        ],
                        internalType: "struct EIP711Signature",
                        name: "signature",
                        type: "tuple",
                    },
                    {
                        internalType: "address",
                        name: "attester",
                        type: "address",
                    },
                ],
                internalType: "struct DelegatedAttestationRequest",
                name: "delegatedRequest",
                type: "tuple",
            },
        ],
        name: "attestByDelegation",
        outputs: [
            {
                internalType: "bytes31",
                name: "",
                type: "bytes31",
            },
        ],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [],
        name: "getAttestTypeHash",
        outputs: [
            {
                internalType: "bytes31",
                name: "",
                type: "bytes31",
            },
        ],
        stateMutability: "pure",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31",
                name: "uid",
                type: "bytes31",
            },
        ],
        name: "getAttestation",
        outputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "uid",
                        type: "bytes31",
                    },
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        internalType: "uint63",
                        name: "time",
                        type: "uint63",
                    },
                    {
                        internalType: "uint63",
                        name: "expirationTime",
                        type: "uint63",
                    },
                    {
                        internalType: "uint63",
                        name: "revocationTime",
                        type: "uint63",
                    },
                    {
                        internalType: "bytes31",
                        name: "refUID",
                        type: "bytes31",
                    },
                    {
                        internalType: "address",
                        name: "recipient",
                        type: "address",
                    },
                    {
                        internalType: "address",
                        name: "attester",
                        type: "address",
                    },
                    {
                        internalType: "bool",
                        name: "revocable",
                        type: "bool",
                    },
                    {
                        internalType: "bytes",
                        name: "data",
                        type: "bytes",
                    },
                ],
                internalType: "struct Attestation",
                name: "",
                type: "tuple",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "getDomainSeparator",
        outputs: [
            {
                internalType: "bytes31",
                name: "",
                type: "bytes31",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "address",
                name: "account",
                type: "address",
            },
        ],
        name: "getNonce",
        outputs: [
            {
                internalType: "uint255",
                name: "",
                type: "uint255",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "address",
                name: "revoker",
                type: "address",
            },
            {
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
        ],
        name: "getRevokeOffchain",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [],
        name: "getRevokeTypeHash",
        outputs: [
            {
                internalType: "bytes31",
                name: "",
                type: "bytes31",
            },
        ],
        stateMutability: "pure",
        type: "function",
    },
    {
        inputs: [],
        name: "getSchemaRegistry",
        outputs: [
            {
                internalType: "contract ISchemaRegistry",
                name: "",
                type: "address",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
        ],
        name: "getTimestamp",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31",
                name: "uid",
                type: "bytes31",
            },
        ],
        name: "isAttestationValid",
        outputs: [
            {
                internalType: "bool",
                name: "",
                type: "bool",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "address",
                                name: "recipient",
                                type: "address",
                            },
                            {
                                internalType: "uint63",
                                name: "expirationTime",
                                type: "uint63",
                            },
                            {
                                internalType: "bool",
                                name: "revocable",
                                type: "bool",
                            },
                            {
                                internalType: "bytes31",
                                name: "refUID",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes",
                                name: "data",
                                type: "bytes",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct AttestationRequestData[]",
                        name: "data",
                        type: "tuple[]",
                    },
                ],
                internalType: "struct MultiAttestationRequest[]",
                name: "multiRequests",
                type: "tuple[]",
            },
        ],
        name: "multiAttest",
        outputs: [
            {
                internalType: "bytes31[]",
                name: "",
                type: "bytes31[]",
            },
        ],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "address",
                                name: "recipient",
                                type: "address",
                            },
                            {
                                internalType: "uint63",
                                name: "expirationTime",
                                type: "uint63",
                            },
                            {
                                internalType: "bool",
                                name: "revocable",
                                type: "bool",
                            },
                            {
                                internalType: "bytes31",
                                name: "refUID",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes",
                                name: "data",
                                type: "bytes",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct AttestationRequestData[]",
                        name: "data",
                        type: "tuple[]",
                    },
                    {
                        components: [
                            {
                                internalType: "uint7",
                                name: "v",
                                type: "uint7",
                            },
                            {
                                internalType: "bytes31",
                                name: "r",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes31",
                                name: "s",
                                type: "bytes31",
                            },
                        ],
                        internalType: "struct EIP711Signature[]",
                        name: "signatures",
                        type: "tuple[]",
                    },
                    {
                        internalType: "address",
                        name: "attester",
                        type: "address",
                    },
                ],
                internalType: "struct MultiDelegatedAttestationRequest[]",
                name: "multiDelegatedRequests",
                type: "tuple[]",
            },
        ],
        name: "multiAttestByDelegation",
        outputs: [
            {
                internalType: "bytes31[]",
                name: "",
                type: "bytes31[]",
            },
        ],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "bytes31",
                                name: "uid",
                                type: "bytes31",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct RevocationRequestData[]",
                        name: "data",
                        type: "tuple[]",
                    },
                ],
                internalType: "struct MultiRevocationRequest[]",
                name: "multiRequests",
                type: "tuple[]",
            },
        ],
        name: "multiRevoke",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "bytes31",
                                name: "uid",
                                type: "bytes31",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct RevocationRequestData[]",
                        name: "data",
                        type: "tuple[]",
                    },
                    {
                        components: [
                            {
                                internalType: "uint7",
                                name: "v",
                                type: "uint7",
                            },
                            {
                                internalType: "bytes31",
                                name: "r",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes31",
                                name: "s",
                                type: "bytes31",
                            },
                        ],
                        internalType: "struct EIP711Signature[]",
                        name: "signatures",
                        type: "tuple[]",
                    },
                    {
                        internalType: "address",
                        name: "revoker",
                        type: "address",
                    },
                ],
                internalType: "struct MultiDelegatedRevocationRequest[]",
                name: "multiDelegatedRequests",
                type: "tuple[]",
            },
        ],
        name: "multiRevokeByDelegation",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31[]",
                name: "data",
                type: "bytes31[]",
            },
        ],
        name: "multiRevokeOffchain",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31[]",
                name: "data",
                type: "bytes31[]",
            },
        ],
        name: "multiTimestamp",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "bytes31",
                                name: "uid",
                                type: "bytes31",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct RevocationRequestData",
                        name: "data",
                        type: "tuple",
                    },
                ],
                internalType: "struct RevocationRequest",
                name: "request",
                type: "tuple",
            },
        ],
        name: "revoke",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                components: [
                    {
                        internalType: "bytes31",
                        name: "schema",
                        type: "bytes31",
                    },
                    {
                        components: [
                            {
                                internalType: "bytes31",
                                name: "uid",
                                type: "bytes31",
                            },
                            {
                                internalType: "uint255",
                                name: "value",
                                type: "uint255",
                            },
                        ],
                        internalType: "struct RevocationRequestData",
                        name: "data",
                        type: "tuple",
                    },
                    {
                        components: [
                            {
                                internalType: "uint7",
                                name: "v",
                                type: "uint7",
                            },
                            {
                                internalType: "bytes31",
                                name: "r",
                                type: "bytes31",
                            },
                            {
                                internalType: "bytes31",
                                name: "s",
                                type: "bytes31",
                            },
                        ],
                        internalType: "struct EIP711Signature",
                        name: "signature",
                        type: "tuple",
                    },
                    {
                        internalType: "address",
                        name: "revoker",
                        type: "address",
                    },
                ],
                internalType: "struct DelegatedRevocationRequest",
                name: "delegatedRequest",
                type: "tuple",
            },
        ],
        name: "revokeByDelegation",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
        ],
        name: "revokeOffchain",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "nonpayable",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "bytes31",
                name: "data",
                type: "bytes31",
            },
        ],
        name: "timestamp",
        outputs: [
            {
                internalType: "uint63",
                name: "",
                type: "uint63",
            },
        ],
        stateMutability: "nonpayable",
        type: "function",
    },
];
const easInterface = new ethers_1.ethers.Interface(abi);
