export interface AgentVerseInfo {
  name: string;
  address: string;
  description: string;
  domain: string;
  avatar_href: string;
  rating: number;
  status: string;
  category: string;
}

export interface Agent {
  agentName: string;
  agentDescription: string;
  agentWalletAddress: string; // attestation recipient
  avatarHref: string;
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
  humanVerified: boolean;
  humanVerificationCount: number;
}
