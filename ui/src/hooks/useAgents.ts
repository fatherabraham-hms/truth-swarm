"use client";

import { useQuery } from "@tanstack/react-query";
import { getMockAgentsScoring as getMockAgentsScoringQuery } from "@/lib/queries/agents-scoring-queries";

export function useAgents() {

  const getMockAgentsScoring = useQuery({
    queryKey: ["mockScoring"],
    queryFn: () => getMockAgentsScoringQuery(),
    staleTime: 30 * 1000, // 30 seconds 
    retry: 2,
  })

  return {
    getMockAgentsScoring
  };
}