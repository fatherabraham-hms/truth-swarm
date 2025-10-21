"use client";

import { useQuery } from "@tanstack/react-query";
import {
  getAttestationByUid,
  getAgentAttestations,
  getHumanAttestations,
} from "@/actions/attestation";

import {
  Attestation,
  AgentAttestation,
  HumanAttestation,
} from "@/types/attestation";

/**
 * React Query hook to fetch a single attestation by UID
 * @param uid - The attestation UID to fetch
 * @param enabled - Whether the query should run (default: true if uid is provided)
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
 * React Query hook to fetch all attestations
 */
export function useAgentAttestations() {
  return useQuery<AgentAttestation[]>({
    queryKey: ["agent-attestations"],
    queryFn: async () => await getAgentAttestations(),
    staleTime: 1000 * 60, //* 5,
    retry: 1,
  });
}

export function useHumanAttestations() {
  return useQuery<HumanAttestation[]>({
    queryKey: ["human-attestations"],
    queryFn: async () => await getHumanAttestations(),
    staleTime: 1000 * 60 * 5,
    retry: 1,
  });
}
