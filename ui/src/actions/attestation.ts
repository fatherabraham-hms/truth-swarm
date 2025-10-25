"use server";

import {
  Attestation,
  AgentEvaluationAttestation,
  HumanConfirmationAttestation,
} from "@/types/attestation";
import {
  createEvaluationScoreFromDecoded,
  AGENT_ATTESTATION_SCHEMA_UID,
  HUMAN_ATTESTATION_SCHEMA_UID,
  createHumanConfirmationFromDecoded,
} from "@/lib/attestation-utils";
import {
  decodeAgentAttestationData,
  decodeHumanAttestationData,
} from "@/lib/decode-attestation";

const EAS_GRAPHQL_URL = "https://sepolia.easscan.org/graphql";

export async function getAttestationByUid(
  attestationUid: string
): Promise<Attestation | null> {
  try {
    if (!attestationUid || !attestationUid.startsWith("0x")) {
      throw new Error("Invalid attestation UID format");
    }

    // Simplified GraphQL query (working format)
    const query = `{
      attestation(where: { id: "${attestationUid}" }) {
        id
        attester
        recipient
        revoked
        revocationTime
        expirationTime
        data
      }
    }`;

    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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

    const attestation = result.data?.attestation;
    if (!attestation) return null;

    return {
      uid: attestation.id,
      attester: attestation.attester,
      recipient: attestation.recipient,
      revoked: attestation.revoked,
      revocationTime: Number(attestation.revocationTime),
      expirationTime: Number(attestation.expirationTime),
      data: attestation.data,
    };
  } catch (error) {
    console.error("Error fetching attestation:", error);
    throw error;
  }
}

export async function getAgentEvaluationAttestations(options?: {
  limit?: number;
  skip?: number;
  orderBy?: "timeCreated" | "finalScore";
  orderDirection?: "asc" | "desc";
  where?: {
    attester?: string;
    recipient?: string;
    revoked?: boolean;
  };
}): Promise<AgentEvaluationAttestation[]> {
  try {
    const limit = options?.limit || 50;
    const skip = options?.skip || 0;
    const orderBy = options?.orderBy || "timeCreated";
    const orderDirection = options?.orderDirection || "desc";

    const whereConditions: string[] = [
      `schemaId: { equals: "${AGENT_ATTESTATION_SCHEMA_UID}" }`,
    ];

    if (options?.where?.attester) {
      whereConditions.push(`attester: { equals: "${options.where.attester}" }`);
    }
    if (options?.where?.recipient) {
      whereConditions.push(`recipient: { equals: "${options.where.recipient}" }`);
    }
    if (options?.where?.revoked !== undefined) {
      whereConditions.push(`revoked: { equals: ${options.where.revoked} }`);
    }

    const whereClause = whereConditions.join(", ");

    const query = `{
      attestations(
        where: { ${whereClause} }
        orderBy: [{ ${orderBy}: ${orderDirection} }]
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
        timeCreated
        txid
      }
    }`;

    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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

    const attestations = result.data?.attestations || [];
    const transformedAttestations: AgentEvaluationAttestation[] = [];

    for (const attestation of attestations) {
      try {
        const decodedData = decodeAgentAttestationData(attestation.data);
        const evaluationScore = createEvaluationScoreFromDecoded(decodedData);
        const isRevoked = attestation.revoked && attestation.revocationTime < Date.now();

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
        console.error(`Failed to decode attestation ${attestation.id}:`, error);
      }
    }

    return transformedAttestations;
  } catch (error) {
    console.error("Error fetching attestations:", error);
    throw error;
  }
}

export async function getHumanConfirmationAttestations(options?: {
  limit?: number;
  skip?: number;
  orderBy?: "timeCreated";
  orderDirection?: "asc" | "desc";
  where?: {
    attester?: string;
    recipient?: string;
    revoked?: boolean;
  };
}): Promise<HumanConfirmationAttestation[]> {
  try {
    const limit = options?.limit || 50;
    const skip = options?.skip || 0;
    const orderBy = options?.orderBy || "timeCreated";
    const orderDirection = options?.orderDirection || "desc";

    const whereConditions: string[] = [
      `schemaId: { equals: "${HUMAN_ATTESTATION_SCHEMA_UID}" }`,
    ];

    if (options?.where?.attester) {
      whereConditions.push(`attester: { equals: "${options.where.attester}" }`);
    }
    if (options?.where?.recipient) {
      whereConditions.push(`recipient: { equals: "${options.where.recipient}" }`);
    }
    if (options?.where?.revoked !== undefined) {
      whereConditions.push(`revoked: { equals: ${options.where.revoked} }`);
    }

    const whereClause = whereConditions.join(", ");

    const query = `{
      attestations(
        where: { ${whereClause} }
        orderBy: [{ ${orderBy}: ${orderDirection} }]
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
        timeCreated
        txid
      }
    }`;

    const response = await fetch(EAS_GRAPHQL_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
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

    const attestations = result.data?.attestations || [];
    const transformedAttestations: HumanConfirmationAttestation[] = [];

    for (const attestation of attestations) {
      try {
        const decodedData = decodeHumanAttestationData(attestation.data);
        const humanConfirmation = createHumanConfirmationFromDecoded(decodedData);
        const isRevoked = attestation.revoked && attestation.revocationTime < Date.now();

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
        console.error(`Failed to decode attestation ${attestation.id}:`, error);
      }
    }

    return transformedAttestations;
  } catch (error) {
    console.error("Error fetching attestations:", error);
    throw error;
  }
}


