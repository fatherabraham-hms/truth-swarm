"use client";

import { useEffect, useState } from "react";
import { AgentEvaluationAttestation, HumanConfirmationAttestation } from "@/types/attestation";
import { Agent } from "@/types/agents";
import { fetchMultipleAgentverseInfo } from "@/actions/agentverse";

export function useAgents(
  agentAttestations: AgentEvaluationAttestation[],
  humanAttestations: HumanConfirmationAttestation[]
): {
  agents: Agent[];
  isLoading: boolean;
  error: Error | null;
} {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    async function buildAgents() {
      try {
        setIsLoading(true);
        setError(null);

        if (agentAttestations.length === 0) {
          setAgents([]);
          setIsLoading(false);
          return;
        }

        const uniqueAddresses = new Set<string>();
        agentAttestations.forEach((att) => {
          uniqueAddresses.add(att.evaluationScore.evaluatedAgentAddress);
        });

        const agentverseInfoMap = await fetchMultipleAgentverseInfo(
          Array.from(uniqueAddresses)
        );

        const humanVerificationCounts = new Map<string, number>();
        humanAttestations.forEach((humanAtt) => {
          if (humanAtt.humanConfirmation.approved) {
            const uid = humanAtt.humanConfirmation.originalAttestationUID;
            humanVerificationCounts.set(
              uid,
              (humanVerificationCounts.get(uid) || 0) + 1
            );
          }
        });

        const builtAgents: Agent[] = agentAttestations.map((attestation) => {
          const evalScore = attestation.evaluationScore;
          const agentverseInfo = agentverseInfoMap.get(
            evalScore.evaluatedAgentAddress
          );

          const humanVerifications =
            humanVerificationCounts.get(attestation.uid) || 0;

          return {
            agentName: agentverseInfo?.name || "Unknown Agent",
            agentDescription: agentverseInfo?.description || "",
            agentWalletAddress: attestation.recipient,
            avatarHref: agentverseInfo?.avatar_href || "",
            evaluatedAgentAddress: evalScore.evaluatedAgentAddress,
            evaluatorAgentAddress: evalScore.evaluatorAgentAddress,
            timestamp: evalScore.timestamp,
            finalScore: evalScore.finalScore,
            overallConfidence: evalScore.overallConfidence,
            grade: evalScore.grade,
            correctnessScore: evalScore.correctnessScore,
            correctnessConfidence: evalScore.correctnessConfidence,
            correctnessEffectiveScore: evalScore.correctnessEffectiveScore,
            correctnessWeight: evalScore.correctnessWeight,
            capabilitiesScore: evalScore.capabilitiesScore,
            capabilitiesConfidence: evalScore.capabilitiesConfidence,
            capabilitiesEffectiveScore: evalScore.capabilitiesEffectiveScore,
            capabilitiesWeight: evalScore.capabilitiesWeight,
            domainScore: evalScore.domainScore,
            domainConfidence: evalScore.domainConfidence,
            domainEffectiveScore: evalScore.domainEffectiveScore,
            domainWeight: evalScore.domainWeight,
            detailsCID: evalScore.detailsCID,
            humanVerified: humanVerifications >= 3,
            humanVerificationCount: humanVerifications,
          };
        });

        setAgents(builtAgents);
      } catch (err) {
        console.error("Error building agents:", err);
        setError(err instanceof Error ? err : new Error("Unknown error"));
      } finally {
        setIsLoading(false);
      }
    }

    buildAgents();
  }, [agentAttestations, humanAttestations]);

  return { agents, isLoading, error };
}
