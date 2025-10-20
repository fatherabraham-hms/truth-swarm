"use server";

import { EAS, SchemaEncoder } from "@ethereum-attestation-service/eas-sdk";
import { ethers } from "ethers";
import {
  AgentAttestation,
  Attestation,
  HumanAttestation,
} from "@/types/attestation";
import {
  createEvaluationScoreFromDecoded,
  EAS_CONTRACT_ADDRESS,
  AGENT_ATTESTATION_SCHEMA,
  AGENT_ATTESTATION_SCHEMA_UID,
  HUMAN_ATTESTATION_SCHEMA_UID,
  HUMAN_ATTESTATION_SCHEMA,
  createHumanConfirmationFromDecoded,
} from "@/lib/attestation-utils";

// ATTESTATION BY ID
export async function getAttestationByUid(
  attestationUid: string
): Promise<Attestation | null> {
  try {
    // Validate UID format
    if (!attestationUid || !attestationUid.startsWith("0x")) {
      throw new Error("Invalid attestation UID format");
    }

    // Set up provider (read-only, no private key needed for reading)
    const rpcUrl = process.env.SEPOLIA_RPC;
    if (!rpcUrl) {
      throw new Error("SEPOLIA_RPC environment variable not set");
    }

    const provider = new ethers.JsonRpcProvider(rpcUrl);
    const eas = new EAS(EAS_CONTRACT_ADDRESS);
    eas.connect(provider);

    // Fetch attestation
    const attestation = await eas.getAttestation(attestationUid);

    // Check if attestation exists
    if (
      !attestation ||
      attestation.uid ===
        "0x0000000000000000000000000000000000000000000000000000000000000000"
    ) {
      return null;
    }

    // Convert to typed EvaluationScore
    const isRevoked = await eas.isAttestationRevoked(attestationUid);

    // Return combined attestation data
    return {
      uid: attestation.uid,
      attester: attestation.attester,
      recipient: attestation.recipient,
      revoked: isRevoked,
      revocationTime: Number(attestation.revocationTime),
      expirationTime: Number(attestation.expirationTime),
      data: attestation.data,
    };
  } catch (error) {
    console.error("Error fetching attestation:", error);
    throw error;
  }
}

// AGENT ATTESTATIONS
export async function getAgentAttestations(options?: {
  limit?: number;
  skip?: number;
  orderBy?: "timeCreated" | "finalScore";
  orderDirection?: "asc" | "desc";
  where?: {
    attester?: string;
    recipient?: string;
    revoked?: boolean;
  };
}): Promise<AgentAttestation[]> {
  try {
    const limit = options?.limit || 50;
    const skip = options?.skip || 0;
    const orderBy = options?.orderBy || "timeCreated";
    const orderDirection = options?.orderDirection || "desc";

    // Build GraphQL where clause
    const whereConditions: string[] = [
      `schemaId: { equals: "${AGENT_ATTESTATION_SCHEMA_UID}" }`,
    ];

    if (options?.where?.attester) {
      whereConditions.push(`attester: { equals: "${options.where.attester}" }`);
    }
    if (options?.where?.recipient) {
      whereConditions.push(
        `recipient: { equals: "${options.where.recipient}" }`
      );
    }
    if (options?.where?.revoked !== undefined) {
      whereConditions.push(`revoked: { equals: ${options.where.revoked} }`);
    }

    const whereClause = whereConditions.join(", ");

    // GraphQL query for EAS
    const query = `
      query Attestations {
        attestations(
          where: { ${whereClause} }
          orderBy: { ${orderBy}: ${orderDirection} }
          take: ${limit}
          skip: ${skip}
        ) {
          id
          attester
          recipient
          revoked
          revocationTime
          expirationTime
          data
          decodedDataJson
          timeCreated
          txid
        }
      }
    `;

    // Fetch from EAS GraphQL endpoint
    const EAS_GRAPHQL_URL = "https://sepolia.easscan.org/graphql";
    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
      next: { revalidate: 60 }, // Cache for 60 seconds
    });

    if (!response.ok) {
      throw new Error(`GraphQL request failed: ${response.statusText}`);
    }

    const result = await response.json();

    if (result.errors) {
      console.error("GraphQL errors:", result.errors);
      throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
    }

    const attestations = result.data?.attestations || [];

    // Transform GraphQL response to AttestationWithScore
    const dataDecoder = new SchemaEncoder(AGENT_ATTESTATION_SCHEMA);
    const transformedAttestations: AgentAttestation[] = [];

    for (const attestation of attestations) {
      try {
        // Decode the attestation data
        const decodedData = dataDecoder.decodeData(attestation.data);

        // Convert to typed EvaluationScore
        const evaluationScore = createEvaluationScoreFromDecoded(decodedData);

        const isRevoked =
          attestation.revoked && attestation.revocationTime < Date.now();

        transformedAttestations.push({
          uid: attestation.id,
          attester: attestation.attester,
          recipient: attestation.recipient,
          revoked: isRevoked,
          revocationTime: Number(attestation.revocationTime),
          expirationTime: Number(attestation.expirationTime),
          evaluationScore,
        });
      } catch (error) {
        // Log but don't fail entire query if one attestation fails to decode
        console.error(`Failed to decode attestation ${attestation.id}:`, error);
      }
    }

    return transformedAttestations;
  } catch (error) {
    console.error("Error fetching attestations:", error);
    throw error;
  }
}

export async function getAgentAttestationsCount(where?: {
  attester?: string;
  recipient?: string;
  revoked?: boolean;
}): Promise<number> {
  try {
    // Build GraphQL where clause
    const whereConditions: string[] = [
      `schemaId: { equals: "${AGENT_ATTESTATION_SCHEMA_UID}" }`,
    ];

    if (where?.attester) {
      whereConditions.push(`attester: { equals: "${where.attester}" }`);
    }
    if (where?.recipient) {
      whereConditions.push(`recipient: { equals: "${where.recipient}" }`);
    }
    if (where?.revoked !== undefined) {
      whereConditions.push(`revoked: { equals: ${where.revoked} }`);
    }

    const whereClause = whereConditions.join(", ");

    const query = `
      query AttestationsCount {
        attestationsCount(
          where: { ${whereClause} }
        )
      }
    `;

    const EAS_GRAPHQL_URL = "https://sepolia.easscan.org/graphql";
    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
      next: { revalidate: 60 },
    });

    if (!response.ok) {
      throw new Error(`GraphQL request failed: ${response.statusText}`);
    }

    const result = await response.json();

    if (result.errors) {
      console.error("GraphQL errors:", result.errors);
      throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
    }

    return result.data?.attestationsCount || 0;
  } catch (error) {
    console.error("Error fetching attestations count:", error);
    throw error;
  }
}

//  HUMAN ATTESTATIONS
export async function getHumanAttestations(options?: {
  limit?: number;
  skip?: number;
  orderBy?: "timeCreated" | "finalScore";
  orderDirection?: "asc" | "desc";
  where?: {
    attester?: string;
    recipient?: string;
    revoked?: boolean;
  };
}): Promise<HumanAttestation[]> {
  try {
    const limit = options?.limit || 50;
    const skip = options?.skip || 0;
    const orderBy = options?.orderBy || "timeCreated";
    const orderDirection = options?.orderDirection || "desc";

    // Build GraphQL where clause
    const whereConditions: string[] = [
      `schemaId: { equals: "${HUMAN_ATTESTATION_SCHEMA_UID}" }`,
    ];

    if (options?.where?.attester) {
      whereConditions.push(`attester: { equals: "${options.where.attester}" }`);
    }
    if (options?.where?.recipient) {
      whereConditions.push(
        `recipient: { equals: "${options.where.recipient}" }`
      );
    }
    if (options?.where?.revoked !== undefined) {
      whereConditions.push(`revoked: { equals: ${options.where.revoked} }`);
    }

    const whereClause = whereConditions.join(", ");

    // GraphQL query for EAS
    const query = `
      query Attestations {
        attestations(
          where: { ${whereClause} }
          orderBy: { ${orderBy}: ${orderDirection} }
          take: ${limit}
          skip: ${skip}
        ) {
          id
          attester
          recipient
          revoked
          revocationTime
          expirationTime
          data
          decodedDataJson
          timeCreated
          txid
        }
      }
    `;

    // Fetch from EAS GraphQL endpoint
    const EAS_GRAPHQL_URL = "https://sepolia.easscan.org/graphql";
    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
      next: { revalidate: 60 }, // Cache for 60 seconds
    });

    if (!response.ok) {
      throw new Error(`GraphQL request failed: ${response.statusText}`);
    }

    const result = await response.json();

    if (result.errors) {
      console.error("GraphQL errors:", result.errors);
      throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
    }

    const attestations = result.data?.attestations || [];

    // Transform GraphQL response to AttestationWithScore
    const dataDecoder = new SchemaEncoder(HUMAN_ATTESTATION_SCHEMA);
    const transformedAttestations: HumanAttestation[] = [];

    for (const attestation of attestations) {
      try {
        // Decode the attestation data
        const decodedData = dataDecoder.decodeData(attestation.data);

        // Convert to typed EvaluationScore
        const humanConfirmation =
          createHumanConfirmationFromDecoded(decodedData);

        const isRevoked =
          attestation.revoked && attestation.revocationTime < Date.now();

        transformedAttestations.push({
          uid: attestation.id,
          attester: attestation.attester,
          recipient: attestation.recipient,
          revoked: isRevoked,
          revocationTime: Number(attestation.revocationTime),
          expirationTime: Number(attestation.expirationTime),
          humanConfirmation,
        });
      } catch (error) {
        // Log but don't fail entire query if one attestation fails to decode
        console.error(`Failed to decode attestation ${attestation.id}:`, error);
      }
    }

    return transformedAttestations;
  } catch (error) {
    console.error("Error fetching attestations:", error);
    throw error;
  }
}
