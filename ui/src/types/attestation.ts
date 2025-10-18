export interface Attestation {
  uid: string;
  attester: string;
  recipient: string;
  revoked: boolean;
  revocationTime: number;
  expirationTime: number;
  data: any;
}

// Attestation signable by agent
export interface AgentAttestation {
  uid: string;
  attester: string;
  recipient: string;
  revoked: boolean;
  revocationTime: number;
  expirationTime: number;
  evaluationScore: EvaluationScore;
}

// Agent attestation schema (eval score) typescript interface
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

// Attestation signable by human (EOA)
export interface HumanAttestation {
  uid: string;
  attester: string;
  recipient: string;
  revoked: boolean;
  revocationTime: number;
  expirationTime: number;
  humanConfirmation: HumanConfirmation;
}

// Human attestation schema (human confirmation) typescript interface
export interface HumanConfirmation {
  originalAttestationUID: string;
  verifier: string;
  timestamp: number;
  approved: boolean;
  comment: string;
}
