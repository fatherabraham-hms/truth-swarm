"use client";

import { useQuery } from "@tanstack/react-query";

export interface MetricDetail {
  score: number;
  confidence: number;
  effective_score: number;
  info: string[];
  evidence: string[];
  failures: string[];
  weight: number;
}

export interface EvaluationScoreWithDetails {
  evaluatedAgentAddress: string;
  evaluatorAgentAddress: string;
  timestamp: string;
  finalScore: number;
  overallConfidence: number;
  grade: string;
  metrics: {
    correctness: MetricDetail;
    capabilities: MetricDetail;
    domain: MetricDetail;
  };
}

const mockEvaluationDetails = (): EvaluationScoreWithDetails => ({
  evaluatedAgentAddress: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  evaluatorAgentAddress: "truth-swarm-metta-v1",
  timestamp: "2025-10-15T10:30:00Z",
  finalScore: 78.5,
  overallConfidence: 85.2,
  grade: "B+",
  metrics: {
    correctness: {
      score: 85.0,
      confidence: 92.0,
      effective_score: 78.2,
      info: [
        "TC-CAP-001: Produces a correct response to the question: What is the Base chainId?",
        "TC-CAP-002: Produces a correct response to the question: What is the Uniswap V3 Address?",
        "TC-CAP-004: Produces a correct response to the question: What is the liquidity calculation algorithm?",
      ],
      evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
      failures: ["TC-CAP-004: FAIL - No MEV protection"],
      weight: 0.15,
    },
    capabilities: {
      score: 92.0,
      confidence: 95.0,
      effective_score: 87.4,
      info: [
        "TC-CAP-001: Produces a correct response to the question: What is the Base chainId?",
        "TC-CAP-002: Produces a correct response to the question: What is the Uniswap V3 Address?",
        "TC-CAP-004: Produces a correct response to the question: What is the liquidity calculation algorithm?",
      ],
      evidence: ["TC-FUNC-001: 92% exact match", "TC-FUNC-002: 100% correct"],
      failures: ["TC-FUNC-003: 8% incorrect error messages"],
      weight: 0.2,
    },
    domain: {
      score: 75.0,
      confidence: 80.0,
      effective_score: 60.0,
      info: [
        "TC-CAP-001: Produces a correct response to the question: What is the Base chainId?",
        "TC-CAP-002: Produces a correct response to the question: What is the Uniswap V3 Address?",
        "TC-CAP-004: Produces a correct response to the question: What is the liquidity calculation algorithm?",
      ],
      evidence: ["TC-DOM-001: PASS", "TC-DOM-004: PASS"],
      failures: [
        "TC-DOM-005: FAIL - No MEV protection",
        "TC-DOM-002: WARN - Inconsistent liquidity warnings",
      ],
      weight: 0.2,
    },
  },
});

/**
 * React Query hook to fetch detailed evaluation data from IPFS
 * @param detailsCID - The IPFS CID containing the detailed evaluation
 */
export function useEvaluationDetails(detailsCID: string) {
  return useQuery<EvaluationScoreWithDetails>({
    queryKey: ["evaluation-details", detailsCID],
    queryFn: async () => {
      // Mock implementation - will fetch from IPFS later
      // TODO: Replace with actual IPFS fetch:
      // const response = await fetch(`https://ipfs.io/ipfs/${detailsCID}`);
      // return await response.json();
      //const ipfsData = getIpfsData(detailsCID);

      await new Promise((resolve) => setTimeout(resolve, 500));
      return mockEvaluationDetails(/** */);
    },
    staleTime: 1000 * 60 * 10, // 10 minutes
    retry: 1,
  });
}
