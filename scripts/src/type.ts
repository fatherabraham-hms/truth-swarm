export const schema = `(
    string evaluatedAgentAddress,
    string evaluatorAgentAddress,
    uint256 timestamp,
    uint256 finalScore,
    uint8 overallConfidence,
    string grade,
    uint256 correctnessScore,
    uint8 correctnessConfidence,
    uint256 correctnessEffectiveScore,
    uint8 correctnessWeight,
    uint256 capabilitiesScore,
    uint8 capabilitiesConfidence,
    uint256 capabilitiesEffectiveScore,
    uint8 capabilitiesWeight,
    uint256 domainScore,
    uint8 domainConfidence,
    uint256 domainEffectiveScore,
    uint8 domainWeight,
    string detailsCID
  )`;

export const encodingSchema = `string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID`;

export interface EvaluationScore {
  evaluatedAgentAddress: string;
  evaluatorAgentAddress: string;
  timestamp: number;
  finalScore: number;
  overallConfidence: number;
  grade: string;
  correctnessScore: number;
  correctnessConfidence: number;
  correctnessEffectiveScore: number;
  correctnessWeight: number;
  capabilitiesScore: number;
  capabilitiesConfidence: number;
  capabilitiesEffectiveScore: number;
  capabilitiesWeight: number;
  domainScore: number;
  domainConfidence: number;
  domainEffectiveScore: number;
  domainWeight: number;
  detailsCID: string;
}

// Type for the raw decoded data from EAS SDK
export interface DecodedSchemaValue {
  name: string;
  type: string;
  value: any; // Can be string, bigint, number, boolean, or complex objects
}

export interface DecodedSchemaField {
  name: string;
  type: string;
  signature: string;
  value: DecodedSchemaValue;
}

export type DecodedSchemaData = DecodedSchemaField[];
