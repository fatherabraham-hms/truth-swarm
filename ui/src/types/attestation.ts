export interface AttestationMetric {
  score: number;
  confidence: number;
  effective_score: number;
  evidence: string[];
  failures: string[];
  weight: number;
}

export interface Attestation {
  agent_id: string; //agent address?
  evaluator: string; //evaluator address
  timestamp: string;
  final_score: number;
  overall_confidence: number;
  grade: string;
  metrics: {
    correctness: AttestationMetric;
    capabilities: AttestationMetric;
    domain: AttestationMetric;
  };
  // signature from evaluator -> create metrics based on eoa signature -> extra score = human-in-the-loop
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
