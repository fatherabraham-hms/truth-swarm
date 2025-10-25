export interface Attestation {
  uid: string;
  attester: string;
  recipient: string;
  revoked: boolean;
  revocationTime: number;
  expirationTime: number;
  data?: string;
}

export interface AgentEvaluationAttestation extends Attestation {
  evaluationScore: EvaluationScore;
}

export interface HumanConfirmationAttestation extends Attestation {
  humanConfirmation: HumanConfirmation;
}

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

export interface HumanConfirmation {
  originalAttestationUID: string;
  verifier: string;
  timestamp: number;
  approved: boolean;
  comment: string;
}
