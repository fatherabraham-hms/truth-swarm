/**
 * Decode attestation data using ethers (no EAS SDK)
 */

import { ethers } from "ethers";
import type { DecodedSchemaData } from "@/types/utils";

export function decodeAgentAttestationData(data: string): DecodedSchemaData {
  const abiCoder = ethers.AbiCoder.defaultAbiCoder();
  
  const schema = [
    { name: "evaluatedAgentAddress", type: "string" },
    { name: "evaluatorAgentAddress", type: "string" },
    { name: "timestamp", type: "uint256" },
    { name: "finalScore", type: "uint256" },
    { name: "overallConfidence", type: "uint8" },
    { name: "grade", type: "string" },
    { name: "correctnessScore", type: "uint256" },
    { name: "correctnessConfidence", type: "uint8" },
    { name: "correctnessEffectiveScore", type: "uint256" },
    { name: "correctnessWeight", type: "uint8" },
    { name: "capabilitiesScore", type: "uint256" },
    { name: "capabilitiesConfidence", type: "uint8" },
    { name: "capabilitiesEffectiveScore", type: "uint256" },
    { name: "capabilitiesWeight", type: "uint8" },
    { name: "domainScore", type: "uint256" },
    { name: "domainConfidence", type: "uint8" },
    { name: "domainEffectiveScore", type: "uint256" },
    { name: "domainWeight", type: "uint8" },
    { name: "detailsCID", type: "string" },
  ];

  const types = schema.map(s => s.type);
  const decoded = abiCoder.decode(types, data);

  // Convert to DecodedSchemaData format
  return schema.map((field, index) => ({
    name: field.name,
    type: field.type,
    signature: field.type,
    value: {
      name: field.name,
      type: field.type,
      value: decoded[index],
    },
  }));
}

export function decodeHumanAttestationData(data: string): DecodedSchemaData {
  const abiCoder = ethers.AbiCoder.defaultAbiCoder();
  
  const schema = [
    { name: "originalAttestationUID", type: "bytes32" },
    { name: "verifier", type: "address" },
    { name: "timestamp", type: "uint64" },
    { name: "approved", type: "bool" },
    { name: "comment", type: "string" },
  ];

  const types = schema.map(s => s.type);
  const decoded = abiCoder.decode(types, data);

  // Convert to DecodedSchemaData format
  return schema.map((field, index) => ({
    name: field.name,
    type: field.type,
    signature: field.type,
    value: {
      name: field.name,
      type: field.type,
      value: decoded[index],
    },
  }));
}

