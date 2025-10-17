export interface AttestationMetric {
  score: number;
  confidence: number;
  effective_score: number;
  evidence: string[];
  failures: string[];
  weight: number;
}

export interface Attestation {
  agent_id: string;
  evaluator: string;
  timestamp: string;
  final_score: number;
  overall_confidence: number;
  grade: string;
  metrics: {
    correctness: AttestationMetric;
    capabilities: AttestationMetric;
    domain: AttestationMetric;
  };
  signature?: {
    type: string;
    domain: {
      name: string;
      version: string;
      chainId: number;
    };
    message: string;
    signature: string;
  };
}
