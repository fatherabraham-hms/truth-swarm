import { DecodedSchemaData } from "@/types/utils";
import { EvaluationScore, HumanConfirmation } from "@/types/attestation";

// Schema definition matching scripts/src/type.ts
export const AGENT_ATTESTATION_SCHEMA_UID =
  process.env.NEXT_PUBLIC_AGENT_SCHEMA_UID ||
  "0xba70975168bf5ec3052382a30dcadf24dc26085cea4c33b7964480ca28a40695";
export const AGENT_ATTESTATION_SCHEMA =
  "string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID";

export const HUMAN_ATTESTATION_SCHEMA_UID =
  "0x35bf5bfce7eaa219f46c086d4d60bfe96affaa42a0d2ae1abf17057e6607007d";
export const HUMAN_ATTESTATION_SCHEMA =
  "bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment";

// EAS contract addresses and endpoints
export const EAS_CONTRACT_ADDRESS =
  "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; // Sepolia Testnet
export const EAS_GRAPHQL_URL = "https://sepolia.easscan.org/graphql";

/**
 * Creates an EvaluationScore object from decoded EAS attestation data
 * This is a client-side version of the function in scripts/src/utils.ts
 */
export function createEvaluationScoreFromDecoded(
  decodedData: DecodedSchemaData
): EvaluationScore {
  // Create a map for easy field access
  const fieldMap = new Map<string, unknown>();
  decodedData.forEach((field) => {
    fieldMap.set(field.name, field.value.value);
  });

  // Helper to get and validate required field
  const getField = (
    name: string,
    expectedType: string
  ): bigint | number | string => {
    if (!fieldMap.has(name)) {
      throw new Error(`Missing required field: ${name}`);
    }
    const value = fieldMap.get(name);

    // Type validation
    const actualType = typeof value === "bigint" ? "bigint" : typeof value;
    if (
      expectedType === "numeric" &&
      actualType !== "bigint" &&
      actualType !== "number"
    ) {
      throw new Error(
        `Field ${name} expected bigint or number, got ${actualType}`
      );
    }
    if (expectedType === "string" && actualType !== "string") {
      throw new Error(`Field ${name} expected string, got ${actualType}`);
    }

    return value as bigint | number | string;
  };

  // Helper to convert BigInt or number to number with validation
  const toNumber = (
    value: bigint | number,
    fieldName: string,
    max?: number
  ): number => {
    const num = typeof value === "bigint" ? Number(value) : value;
    if (max !== undefined && num > max) {
      throw new Error(`Field ${fieldName} value ${num} exceeds maximum ${max}`);
    }
    if (num < 0) {
      throw new Error(`Field ${fieldName} value ${num} cannot be negative`);
    }
    return num;
  };

  // Extract and validate all fields
  const evaluatedAgentAddress = getField(
    "evaluatedAgentAddress",
    "string"
  ) as string;
  const evaluatorAgentAddress = getField(
    "evaluatorAgentAddress",
    "string"
  ) as string;
  const timestamp = toNumber(
    getField("timestamp", "numeric") as bigint | number,
    "timestamp"
  );
  const finalScore = toNumber(
    getField("finalScore", "numeric") as bigint | number,
    "finalScore",
    100
  );
  const overallConfidence = toNumber(
    getField("overallConfidence", "numeric") as bigint | number,
    "overallConfidence",
    10
  );
  const grade = getField("grade", "string") as string;

  const correctnessScore = toNumber(
    getField("correctnessScore", "numeric") as bigint | number,
    "correctnessScore",
    100
  );
  const correctnessConfidence = toNumber(
    getField("correctnessConfidence", "numeric") as bigint | number,
    "correctnessConfidence",
    10
  );
  const correctnessEffectiveScore = toNumber(
    getField("correctnessEffectiveScore", "numeric") as bigint | number,
    "correctnessEffectiveScore",
    100
  );
  const correctnessWeight = toNumber(
    getField("correctnessWeight", "numeric") as bigint | number,
    "correctnessWeight",
    100
  );

  const capabilitiesScore = toNumber(
    getField("capabilitiesScore", "numeric") as bigint | number,
    "capabilitiesScore",
    100
  );
  const capabilitiesConfidence = toNumber(
    getField("capabilitiesConfidence", "numeric") as bigint | number,
    "capabilitiesConfidence",
    10
  );
  const capabilitiesEffectiveScore = toNumber(
    getField("capabilitiesEffectiveScore", "numeric") as bigint | number,
    "capabilitiesEffectiveScore",
    100
  );
  const capabilitiesWeight = toNumber(
    getField("capabilitiesWeight", "numeric") as bigint | number,
    "capabilitiesWeight",
    100
  );

  const domainScore = toNumber(
    getField("domainScore", "numeric") as bigint | number,
    "domainScore",
    100
  );
  const domainConfidence = toNumber(
    getField("domainConfidence", "numeric") as bigint | number,
    "domainConfidence",
    10
  );
  const domainEffectiveScore = toNumber(
    getField("domainEffectiveScore", "numeric") as bigint | number,
    "domainEffectiveScore",
    100
  );
  const domainWeight = toNumber(
    getField("domainWeight", "numeric") as bigint | number,
    "domainWeight",
    100
  );

  const detailsCID = getField("detailsCID", "string") as string;

  // Additional validation
  if (evaluatedAgentAddress.length === 0) {
    throw new Error("evaluatedAgentAddress cannot be empty");
  }
  if (evaluatorAgentAddress.length === 0) {
    throw new Error("evaluatorAgentAddress cannot be empty");
  }
  if (detailsCID.length === 0) {
    throw new Error("detailsCID cannot be empty");
  }

  // Validate weights sum to 100 (optional but good practice)
  const totalWeight = correctnessWeight + capabilitiesWeight + domainWeight;
  if (totalWeight !== 100) {
    console.warn(`Warning: Total weights (${totalWeight}) do not sum to 100`);
  }

  return {
    evaluatedAgentAddress,
    evaluatorAgentAddress,
    timestamp,
    finalScore,
    overallConfidence,
    grade,
    correctnessScore,
    correctnessConfidence,
    correctnessEffectiveScore,
    correctnessWeight,
    capabilitiesScore,
    capabilitiesConfidence,
    capabilitiesEffectiveScore,
    capabilitiesWeight,
    domainScore,
    domainConfidence,
    domainEffectiveScore,
    domainWeight,
    detailsCID,
  };
}

/**
 * Creates a HumanConfirmation object from decoded EAS attestation data
 */
export function createHumanConfirmationFromDecoded(
  decodedData: DecodedSchemaData
): HumanConfirmation {
  // Create a map for easy field access
  const fieldMap = new Map<string, unknown>();
  decodedData.forEach((field) => {
    fieldMap.set(field.name, field.value.value);
  });

  // Helper to get and validate required field
  const getField = (name: string, expectedType: string): unknown => {
    if (!fieldMap.has(name)) {
      throw new Error(`Missing required field: ${name}`);
    }
    const value = fieldMap.get(name);

    // Type validation
    const actualType = typeof value === "bigint" ? "bigint" : typeof value;
    if (
      expectedType === "numeric" &&
      actualType !== "bigint" &&
      actualType !== "number"
    ) {
      throw new Error(
        `Field ${name} expected bigint or number, got ${actualType}`
      );
    }
    if (expectedType === "string" && actualType !== "string") {
      throw new Error(`Field ${name} expected string, got ${actualType}`);
    }
    if (expectedType === "boolean" && actualType !== "boolean") {
      throw new Error(`Field ${name} expected boolean, got ${actualType}`);
    }

    return value;
  };

  // Helper to convert BigInt or number to number
  const toNumber = (value: bigint | number, fieldName: string): number => {
    const num = typeof value === "bigint" ? Number(value) : value;
    if (num < 0) {
      throw new Error(`Field ${fieldName} value ${num} cannot be negative`);
    }
    return num;
  };

  // Extract and validate all fields
  const originalAttestationUID = getField(
    "originalAttestationUID",
    "string"
  ) as string;
  const verifier = getField("verifier", "string") as string;
  const timestamp = toNumber(
    getField("timestamp", "numeric") as bigint | number,
    "timestamp"
  );
  const approved = getField("approved", "boolean") as boolean;
  const comment = getField("comment", "string") as string;

  // Additional validation
  if (originalAttestationUID.length === 0) {
    throw new Error("originalAttestationUID cannot be empty");
  }
  if (verifier.length === 0) {
    throw new Error("verifier cannot be empty");
  }

  return {
    originalAttestationUID,
    verifier,
    timestamp,
    approved,
    comment,
  };
}
