"use client";

import { useQuery } from "@tanstack/react-query";
import {
  getAttestationByUid,
  getAgentEvaluationAttestations,
  getHumanConfirmationAttestations
} from "@/actions/attestation";

import {
  Attestation,
  AgentEvaluationAttestation,
  HumanConfirmationAttestation,
} from "@/types/attestation";

/**
 * Attestation hooks integrated with React Query for efficient caching and refetching.
 * 
 * Query keys:
 * - ["attestation", uid] - Single attestation by UID
 * - ["agent-attestations"] - All agent evaluation attestations
 * - ["human-attestations"] - All human confirmation attestations
 * 
 * These queries are automatically invalidated by:
 * 1. AttestationWatcher (Dashboard) when new attestations are detected
 * 2. HCAConfirmationDialog when human confirmations are submitted
 * 
 * The invalidation triggers refetch and UI updates seamlessly with Blockscout SDK integration.
 */

export function useAttestationByUID(uid?: string, enabled: boolean = true) {
  return useQuery<Attestation | null, Error>({
    queryKey: ["attestation", uid],
    queryFn: async () => {
      if (!uid) {
        return null;
      }
      return await getAttestationByUid(uid);
    },
    enabled: enabled && !!uid,
    staleTime: 1000 * 60 * 5, // 5 minutes
    retry: 1,
  });
}

/**
 * Fetches all agent evaluation attestations.
 * Automatically refetches when:
 * - New attestations are detected by AttestationWatcher
 * - Manual invalidation via queryClient.invalidateQueries({ queryKey: ["agent-attestations"] })
 */
export function useAgentAttestations() {
  return useQuery<AgentEvaluationAttestation[]>({
    queryKey: ["agent-attestations"],
    queryFn: async () => await getAgentEvaluationAttestations(),
    staleTime: 1000 * 60,
    retry: 1,
  });
}

/**
 * Fetches all human confirmation attestations.
 * Automatically refetches when:
 * - New confirmations are submitted via HCAConfirmationDialog
 * - New attestations are detected by AttestationWatcher
 * - Manual invalidation via queryClient.invalidateQueries({ queryKey: ["human-attestations"] })
 */
export function useHumanAttestations() {
  return useQuery<HumanConfirmationAttestation[]>({
    queryKey: ["human-attestations"],
    queryFn: async () => await getHumanConfirmationAttestations(),
    staleTime: 1000 * 60,
    retry: 1,
  });
}
