// Type for the raw decoded data from EAS SDK
export interface DecodedSchemaValue {
  name: string;
  type: string;
  value: unknown; // Can be string, bigint, number, boolean, or complex objects
}

export interface DecodedSchemaField {
  name: string;
  type: string;
  signature: string;
  value: DecodedSchemaValue;
}

export type DecodedSchemaData = DecodedSchemaField[];

// GraphQL response types
export interface GraphQLAttestationResponse {
  attestations: GraphQLAttestation[];
}

export interface GraphQLAttestation {
  id: string;
  attester: string;
  recipient: string;
  revoked: boolean;
  revocationTime: number;
  expirationTime: number;
  data: string;
  decodedDataJson: string;
  timeCreated: number;
  txid: string;
}

// Options for fetching attestations
export interface GetAttestationsOptions {
  limit?: number;
  skip?: number;
  orderBy?: "timeCreated" | "finalScore";
  orderDirection?: "asc" | "desc";
  where?: {
    attester?: string;
    recipient?: string;
    revoked?: boolean;
  };
}
