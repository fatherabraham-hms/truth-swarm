// Sepolia testnet addresses
export const EAS_CONTRACT_ADDRESS =
  "0xC2679fBD37d54388Ce493F1DB75320D236e1815e" as const;

// Schema UIDs
export const AGENT_ATTESTATION_SCHEMA_UID =
  "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc" as const;

export const HUMAN_ATTESTATION_SCHEMA_UID =
  "0x35bf5bfce7eaa219f46c086d4d60bfe96affaa42a0d2ae1abf17057e6607007d" as const;

// EAS Contract ABI (minimal - only attest function)
export const EAS_ABI = [
  {
    inputs: [
      {
        components: [
          {
            internalType: "bytes32",
            name: "schema",
            type: "bytes32",
          },
          {
            components: [
              {
                internalType: "address",
                name: "recipient",
                type: "address",
              },
              {
                internalType: "uint64",
                name: "expirationTime",
                type: "uint64",
              },
              {
                internalType: "bool",
                name: "revocable",
                type: "bool",
              },
              {
                internalType: "bytes32",
                name: "refUID",
                type: "bytes32",
              },
              {
                internalType: "bytes",
                name: "data",
                type: "bytes",
              },
              {
                internalType: "uint256",
                name: "value",
                type: "uint256",
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
        internalType: "bytes32",
        name: "",
        type: "bytes32",
      },
    ],
    stateMutability: "payable",
    type: "function",
  },
] as const;
