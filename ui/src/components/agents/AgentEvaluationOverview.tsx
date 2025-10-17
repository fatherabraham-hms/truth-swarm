"use client";

import { Attestation } from "@/types/attestation";
import { useEffect, useState } from "react";
import Link from "next/link";

interface AgentEvaluationOverviewProps {
  address: string;
}

export function AgentEvaluationOverview({
  address,
}: AgentEvaluationOverviewProps) {
  const [attestation, setAttestation] = useState<Attestation | null>(null);
  const [loading, setLoading] = useState(true);
  const [agentName, setAgentName] = useState<string>("");

  useEffect(() => {
    fetchAgentData(address);
  }, [address]);

  const fetchAgentData = async (agentAddress: string) => {
    // Mock data fetch - replace with actual API call
    setLoading(true);
    // Simulated API call
    setTimeout(() => {
      // You would fetch the actual data here based on the address
      const mockData = getMockAttestationByAddress(agentAddress);
      setAttestation(mockData.attestation);
      setAgentName(mockData.name);
      setLoading(false);
    }, 500);
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "#10b981"; // green
    if (score >= 60) return "#3b82f6"; // blue
    if (score >= 40) return "#f59e0b"; // amber
    return "#ef4444"; // red
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex items-center justify-center py-12">
          <div className="text-muted-foreground">Loading agent details...</div>
        </div>
      </div>
    );
  }

  if (!attestation) {
    return (
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="text-xl font-semibold">Agent not found</div>
          <Link
            href="/"
            className="text-sm text-blue-600 hover:text-blue-700 underline"
          >
            ← Back to agents list
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-8 space-y-8">
      {/* Back Button */}
      <Link
        href="/"
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <span className="mr-2">←</span>
        Back to agents list
      </Link>

      {/* Header Section */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">{agentName}</h1>
        <p className="text-muted-foreground font-mono text-sm break-all">
          {address}
        </p>
      </div>

      {/* Overall Score Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">Final Score</div>
          <div className="text-4xl font-bold">
            {attestation.final_score.toFixed(1)}
          </div>
          <div className="text-sm text-muted-foreground mt-1">out of 100</div>
        </div>

        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">Grade</div>
          <div className="text-4xl font-bold">{attestation.grade}</div>
        </div>

        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">Confidence</div>
          <div className="text-4xl font-bold">
            {attestation.overall_confidence.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Metrics Breakdown */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Performance Metrics</h2>

        {Object.entries(attestation.metrics).map(([key, metric]) => (
          <div
            key={key}
            className="p-6 border border-border rounded-lg bg-card space-y-4"
          >
            <div className="flex justify-between items-center">
              <h3 className="text-xl font-semibold capitalize">{key}</h3>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  {metric.effective_score.toFixed(1)}
                </div>
                <div className="text-sm text-muted-foreground">
                  Score: {metric.score} | Conf: {metric.confidence}%
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="h-4 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full transition-all"
                  style={{
                    width: `${metric.effective_score}%`,
                    backgroundColor: getScoreColor(metric.effective_score),
                  }}
                />
              </div>
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Weight: {(metric.weight * 100).toFixed(0)}%</span>
                <span>{metric.effective_score.toFixed(1)}%</span>
              </div>
            </div>

            {/* Evidence */}
            {metric.evidence.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-medium">Evidence</h4>
                <ul className="space-y-1">
                  {metric.evidence.map((item, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-muted-foreground flex items-start"
                    >
                      <span className="mr-2 text-green-600">✓</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Failures */}
            {metric.failures.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-sm font-medium text-red-600">Failures</h4>
                <ul className="space-y-1">
                  {metric.failures.map((item, idx) => (
                    <li
                      key={idx}
                      className="text-sm text-red-600/80 flex items-start"
                    >
                      <span className="mr-2">✗</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Metadata */}
      <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-2">
        <h3 className="text-lg font-semibold mb-4">Evaluation Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Evaluator:</span>
            <span className="ml-2 font-mono">{attestation.evaluator}</span>
          </div>
          <div>
            <span className="text-muted-foreground">Timestamp:</span>
            <span className="ml-2">
              {new Date(attestation.timestamp).toLocaleString()}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

// Mock function - replace with actual data fetching
function getMockAttestationByAddress(address: string): {
  name: string;
  attestation: Attestation;
} {
  // This should query your backend or state management
  // For now, returning mock data based on the address
  const mockAgents: Record<string, { name: string; attestation: Attestation }> =
    {
      "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb": {
        name: "mettalex dex",
        attestation: {
          agent_id: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
          evaluator: "truth-swarm-metta-v1",
          timestamp: "2025-10-15T10:30:00Z",
          final_score: 78.5,
          overall_confidence: 85.2,
          grade: "B+",
          metrics: {
            correctness: {
              score: 85.0,
              confidence: 92.0,
              effective_score: 78.2,
              evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
              failures: ["TC-CAP-004: FAIL - No MEV protection"],
              weight: 0.15,
            },
            capabilities: {
              score: 92.0,
              confidence: 95.0,
              effective_score: 87.4,
              evidence: [
                "TC-FUNC-001: 92% exact match",
                "TC-FUNC-002: 100% correct",
              ],
              failures: ["TC-FUNC-003: 8% incorrect error messages"],
              weight: 0.2,
            },
            domain: {
              score: 75.0,
              confidence: 80.0,
              effective_score: 60.0,
              evidence: ["TC-DOM-001: PASS", "TC-DOM-004: PASS"],
              failures: [
                "TC-DOM-005: FAIL - No MEV protection",
                "TC-DOM-002: WARN - Inconsistent liquidity warnings",
              ],
              weight: 0.2,
            },
          },
        },
      },
      "0x8f3a21B0C5e0F6C8D9A5B4C3D2E1F0A9B8C7D6E5": {
        name: "unadivsooor",
        attestation: {
          agent_id: "0x8f3a21B0C5e0F6C8D9A5B4C3D2E1F0A9B8C7D6E5",
          evaluator: "truth-swarm-metta-v1",
          timestamp: "2025-10-14T14:20:00Z",
          final_score: 32.8,
          overall_confidence: 75.5,
          grade: "F",
          metrics: {
            correctness: {
              score: 25.0,
              confidence: 85.0,
              effective_score: 21.2,
              evidence: ["TC-CAP-001: FAIL"],
              failures: [
                "TC-CAP-002: FAIL - Incorrect data format",
                "TC-CAP-003: FAIL - Missing validations",
                "TC-CAP-004: FAIL - Security vulnerabilities",
              ],
              weight: 0.15,
            },
            capabilities: {
              score: 40.0,
              confidence: 70.0,
              effective_score: 28.0,
              evidence: ["TC-FUNC-002: 40% correct"],
              failures: [
                "TC-FUNC-001: FAIL - Poor accuracy",
                "TC-FUNC-003: FAIL - Inconsistent responses",
              ],
              weight: 0.2,
            },
            domain: {
              score: 45.0,
              confidence: 72.0,
              effective_score: 32.4,
              evidence: ["TC-DOM-003: PASS"],
              failures: [
                "TC-DOM-001: FAIL - Domain knowledge gaps",
                "TC-DOM-002: FAIL - Incorrect terminology",
              ],
              weight: 0.2,
            },
          },
        },
      },
      "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b": {
        name: "weather oracle",
        attestation: {
          agent_id: "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
          evaluator: "truth-swarm-metta-v1",
          timestamp: "2025-10-16T08:15:00Z",
          final_score: 91.3,
          overall_confidence: 94.7,
          grade: "A",
          metrics: {
            correctness: {
              score: 95.0,
              confidence: 98.0,
              effective_score: 93.1,
              evidence: [
                "TC-CAP-001: PASS",
                "TC-CAP-002: PASS",
                "TC-CAP-003: PASS",
                "TC-CAP-004: PASS",
              ],
              failures: [],
              weight: 0.15,
            },
            capabilities: {
              score: 92.0,
              confidence: 96.0,
              effective_score: 88.3,
              evidence: [
                "TC-FUNC-001: 95% exact match",
                "TC-FUNC-002: 100% correct",
                "TC-FUNC-003: 98% accurate",
              ],
              failures: [],
              weight: 0.2,
            },
            domain: {
              score: 90.0,
              confidence: 92.0,
              effective_score: 82.8,
              evidence: [
                "TC-DOM-001: PASS",
                "TC-DOM-002: PASS",
                "TC-DOM-003: PASS",
              ],
              failures: ["TC-DOM-004: WARN - Minor edge case handling"],
              weight: 0.2,
            },
          },
        },
      },
      "0x9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e": {
        name: "price feed",
        attestation: {
          agent_id: "0x9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e",
          evaluator: "truth-swarm-metta-v1",
          timestamp: "2025-10-13T16:45:00Z",
          final_score: 68.2,
          overall_confidence: 81.3,
          grade: "C+",
          metrics: {
            correctness: {
              score: 70.0,
              confidence: 85.0,
              effective_score: 59.5,
              evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
              failures: ["TC-CAP-003: FAIL - Latency issues"],
              weight: 0.15,
            },
            capabilities: {
              score: 75.0,
              confidence: 88.0,
              effective_score: 66.0,
              evidence: [
                "TC-FUNC-001: 78% exact match",
                "TC-FUNC-002: 85% correct",
              ],
              failures: ["TC-FUNC-003: WARN - Occasional timeouts"],
              weight: 0.2,
            },
            domain: {
              score: 65.0,
              confidence: 78.0,
              effective_score: 50.7,
              evidence: ["TC-DOM-001: PASS"],
              failures: [
                "TC-DOM-002: FAIL - Limited market coverage",
                "TC-DOM-003: WARN - Price staleness",
              ],
              weight: 0.2,
            },
          },
        },
      },
      "0x5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d": {
        name: "data aggregator",
        attestation: {
          agent_id: "0x5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d",
          evaluator: "truth-swarm-metta-v1",
          timestamp: "2025-10-17T12:00:00Z",
          final_score: 82.7,
          overall_confidence: 88.9,
          grade: "B",
          metrics: {
            correctness: {
              score: 88.0,
              confidence: 93.0,
              effective_score: 81.8,
              evidence: [
                "TC-CAP-001: PASS",
                "TC-CAP-002: PASS",
                "TC-CAP-003: PASS",
              ],
              failures: [],
              weight: 0.15,
            },
            capabilities: {
              score: 85.0,
              confidence: 91.0,
              effective_score: 77.3,
              evidence: [
                "TC-FUNC-001: 87% exact match",
                "TC-FUNC-002: 95% correct",
              ],
              failures: ["TC-FUNC-003: WARN - Minor formatting issues"],
              weight: 0.2,
            },
            domain: {
              score: 78.0,
              confidence: 84.0,
              effective_score: 65.5,
              evidence: ["TC-DOM-001: PASS", "TC-DOM-002: PASS"],
              failures: ["TC-DOM-003: WARN - Limited source diversity"],
              weight: 0.2,
            },
          },
        },
      },
    };

  // Return the mock data if found, otherwise return a default
  return (
    mockAgents[address] || {
      name: "Unknown Agent",
      attestation: {
        agent_id: address,
        evaluator: "truth-swarm-metta-v1",
        timestamp: new Date().toISOString(),
        final_score: 0,
        overall_confidence: 0,
        grade: "N/A",
        metrics: {
          correctness: {
            score: 0,
            confidence: 0,
            effective_score: 0,
            evidence: [],
            failures: ["No data available"],
            weight: 0.15,
          },
          capabilities: {
            score: 0,
            confidence: 0,
            effective_score: 0,
            evidence: [],
            failures: ["No data available"],
            weight: 0.2,
          },
          domain: {
            score: 0,
            confidence: 0,
            effective_score: 0,
            evidence: [],
            failures: ["No data available"],
            weight: 0.2,
          },
        },
      },
    }
  );
}
