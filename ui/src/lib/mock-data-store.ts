/**
 * Shared Mock Data Store
 * 
 * This module provides a centralized store for mock data that can be
 * dynamically updated when new agent evaluations are completed.
 * Data persists across UI restarts by using localStorage in browser.
 */

import { AgentAttestation, HumanAttestation } from "@/types/attestation";
import { AgentVerseInfo } from "@/types/agents";

// Storage keys for persistence
const STORAGE_KEYS = {
  AGENT_ATTESTATIONS: 'truth-swarm-mock-agent-attestations',
  HUMAN_ATTESTATIONS: 'truth-swarm-mock-human-attestations',
  AGENT_INFO: 'truth-swarm-mock-agent-info'
};

// Base mock data that starts with some initial agents
const DEFAULT_AGENT_ATTESTATIONS: AgentAttestation[] = [
  {
    uid: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    attester: "0xAb2DdD48A457b9FE1f7FeE45C6ce0f3D1062A1EA",
    recipient: "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    revoked: false,
    revocationTime: 0,
    expirationTime: 0,
    evaluationScore: {
      evaluatedAgentAddress: "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y",
      evaluatorAgentAddress: "agent1qf4au6rzaauxhy2jze6v85rspgvredx9m42p0e0cukz0hv4dh2sqjuhujpp",
      timestamp: Math.floor(Date.now() / 1000) - 3600,
      finalScore: 87,
      overallConfidence: 85,
      grade: "A",
      correctnessScore: 90,
      correctnessConfidence: 88,
      correctnessEffectiveScore: 36,
      correctnessWeight: 40,
      capabilitiesScore: 85,
      capabilitiesConfidence: 82,
      capabilitiesEffectiveScore: 25,
      capabilitiesWeight: 30,
      domainScore: 88,
      domainConfidence: 85,
      domainEffectiveScore: 26,
      domainWeight: 30,
      detailsCID: "bafkreicryptoagent1evaluationdetails123456789"
    }
  },
  {
    uid: "0x2345678901bcdef12345678901bcdef12345678901bcdef12345678901bcdef1",
    attester: "0xAb2DdD48A457b9FE1f7FeE45C6ce0f3D1062A1EA",
    recipient: "0x842d35Cc6634C0532925a3b8D4C9db96C4b4d8b7",
    revoked: false,
    revocationTime: 0,
    expirationTime: 0,
    evaluationScore: {
      evaluatedAgentAddress: "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
      evaluatorAgentAddress: "agent1qf4au6rzaauxhy2jze6v85rspgvredx9m42p0e0cukz0hv4dh2sqjuhujpp",
      timestamp: Math.floor(Date.now() / 1000) - 7200,
      finalScore: 78,
      overallConfidence: 80,
      grade: "B+",
      correctnessScore: 82,
      correctnessConfidence: 85,
      correctnessEffectiveScore: 33,
      correctnessWeight: 40,
      capabilitiesScore: 75,
      capabilitiesConfidence: 78,
      capabilitiesEffectiveScore: 22,
      capabilitiesWeight: 30,
      domainScore: 77,
      domainConfidence: 77,
      domainEffectiveScore: 23,
      domainWeight: 30,
      detailsCID: "bafkreidefiagent2evaluationdetails234567890"
    }
  }
];

const DEFAULT_HUMAN_ATTESTATIONS: HumanAttestation[] = [
  {
    uid: "0x4567890123def1234567890123def1234567890123def1234567890123def123",
    attester: "0x1234567890123456789012345678901234567890",
    recipient: "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    revoked: false,
    revocationTime: 0,
    expirationTime: 0,
    humanConfirmation: {
      originalAttestationUID: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
      approved: true,
      confidence: 90,
      reasoning: "Agent performed well in crypto trading tasks",
      timestamp: Math.floor(Date.now() / 1000) - 1800
    }
  },
  {
    uid: "0x5678901234ef12345678901234ef12345678901234ef12345678901234ef1234",
    attester: "0x2345678901234567890123456789012345678901",
    recipient: "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    revoked: false,
    revocationTime: 0,
    expirationTime: 0,
    humanConfirmation: {
      originalAttestationUID: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
      approved: true,
      confidence: 85,
      reasoning: "Good performance in DeFi protocols",
      timestamp: Math.floor(Date.now() / 1000) - 2700
    }
  }
];

const DEFAULT_AGENT_INFO: Record<string, AgentVerseInfo> = {
  "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y": {
    name: "CryptoTrader Pro",
    address: "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y",
    description: "Advanced AI agent specializing in cryptocurrency trading, DeFi protocols, and portfolio management. Provides real-time market analysis and automated trading strategies.",
    domain: "crypto",
    avatar_href: "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=100&h=100&fit=crop&crop=center",
    rating: 4.8,
    status: "active",
    category: "crypto"
  },
  "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac": {
    name: "DeFi Protocol Manager",
    address: "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
    description: "Specialized DeFi agent for yield farming, liquidity provision, and automated protocol interactions. Optimizes returns across multiple DeFi platforms.",
    domain: "defi",
    avatar_href: "https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=100&h=100&fit=crop&crop=center",
    rating: 4.6,
    status: "active",
    category: "defi"
  }
};

// Helper functions for localStorage
function saveToStorage<T>(key: string, data: T): void {
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.warn('Failed to save to localStorage:', error);
    }
  }
}

function loadFromStorage<T>(key: string, defaultValue: T): T {
  if (typeof window !== 'undefined') {
    try {
      const stored = localStorage.getItem(key);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (error) {
      console.warn('Failed to load from localStorage:', error);
    }
  }
  return defaultValue;
}

// Agent name templates for generating new agents
const AGENT_NAME_TEMPLATES = [
  "AI Trading Assistant", "Blockchain Analyzer", "Smart Contract Expert", 
  "Crypto Portfolio Manager", "DeFi Yield Optimizer", "NFT Marketplace Bot",
  "Cross-Chain Bridge Agent", "Liquidity Provider Bot", "Price Oracle Agent",
  "Staking Rewards Optimizer", "DEX Arbitrage Bot", "Wallet Security Auditor"
];

const AGENT_DESCRIPTIONS = [
  "Advanced AI agent specializing in automated trading strategies and market analysis.",
  "Professional blockchain analysis agent with expertise in transaction monitoring and security.",
  "Smart contract development and auditing agent with comprehensive security knowledge.",
  "Portfolio management agent optimizing crypto investments across multiple strategies.",
  "DeFi yield farming specialist maximizing returns through automated protocol interactions.",
  "NFT marketplace agent facilitating trading and collection management.",
  "Cross-chain bridge agent enabling seamless asset transfers between blockchains.",
  "Liquidity provision specialist optimizing capital efficiency in DeFi protocols.",
  "Price oracle agent providing accurate market data for decentralized applications.",
  "Staking rewards optimizer maximizing passive income through strategic delegation.",
  "DEX arbitrage bot identifying and executing profitable trading opportunities.",
  "Wallet security auditor ensuring safe storage and transaction practices."
];

const AGENT_CATEGORIES = ["crypto", "defi", "trading", "security", "nft", "staking"];
const AGENT_DOMAINS = ["crypto", "defi", "trading", "security", "nft", "staking"];

// Generate a random agent name and description
function generateAgentProfile(): { name: string; description: string; category: string; domain: string } {
  const nameTemplate = AGENT_NAME_TEMPLATES[Math.floor(Math.random() * AGENT_NAME_TEMPLATES.length)];
  const description = AGENT_DESCRIPTIONS[Math.floor(Math.random() * AGENT_DESCRIPTIONS.length)];
  const category = AGENT_CATEGORIES[Math.floor(Math.random() * AGENT_CATEGORIES.length)];
  const domain = AGENT_DOMAINS[Math.floor(Math.random() * AGENT_DOMAINS.length)];
  
  return { name: nameTemplate, description, category, domain };
}

// Generate a random wallet address
function generateWalletAddress(): string {
  const chars = '0123456789abcdef';
  let result = '0x';
  for (let i = 0; i < 40; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
}

// Generate a random agent address
function generateAgentAddress(): string {
  const chars = '0123456789abcdefghijklmnopqrstuvwxyz';
  let result = 'agent1';
  for (let i = 0; i < 59; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
}

// Generate a random UID
function generateUID(): string {
  const chars = '0123456789abcdef';
  let result = '0x';
  for (let i = 0; i < 64; i++) {
    result += chars[Math.floor(Math.random() * chars.length)];
  }
  return result;
}

// Generate agent profile from meTTa categorization data
function generateProfileFromMetta(mettaCategorization: any) {
  const primaryCategory = mettaCategorization?.primary_category?.category || "General Purpose";
  const confidence = mettaCategorization?.primary_category?.confidence || 0.8;
  
  // Map meTTa categories to more user-friendly names and descriptions
  const categoryMap: Record<string, { name: string; description: string; domain: string }> = {
    "General Purpose": {
      name: "General Purpose Agent",
      description: "A versatile AI agent capable of handling multiple types of tasks and domains",
      domain: "Multi-domain"
    },
    "Specialized": {
      name: "Specialized Agent", 
      description: "An AI agent focused on specific tasks within a particular domain",
      domain: "Specialized"
    },
    "Trading": {
      name: "Trading Agent",
      description: "An AI agent specialized in cryptocurrency trading and market analysis",
      domain: "Finance"
    },
    "DeFi": {
      name: "DeFi Agent",
      description: "An AI agent focused on decentralized finance protocols and yield optimization",
      domain: "Finance"
    },
    "Research": {
      name: "Research Agent",
      description: "An AI agent designed for data analysis and research tasks",
      domain: "Research"
    },
    "Communication": {
      name: "Communication Agent",
      description: "An AI agent specialized in natural language processing and communication",
      domain: "Communication"
    }
  };
  
  const mapped = categoryMap[primaryCategory] || categoryMap["General Purpose"];
  
  return {
    name: mapped.name,
    description: mapped.description,
    domain: mapped.domain,
    category: primaryCategory
  };
}

// Generate random evaluation scores
function generateEvaluationScores() {
  const correctnessScore = Math.floor(Math.random() * 20) + 75; // 75-95
  const capabilitiesScore = Math.floor(Math.random() * 20) + 70; // 70-90
  const domainScore = Math.floor(Math.random() * 20) + 75; // 75-95
  
  const correctnessWeight = 40;
  const capabilitiesWeight = 30;
  const domainWeight = 30;
  
  const correctnessEffective = Math.floor((correctnessScore * correctnessWeight) / 100);
  const capabilitiesEffective = Math.floor((capabilitiesScore * capabilitiesWeight) / 100);
  const domainEffective = Math.floor((domainScore * domainWeight) / 100);
  
  const finalScore = correctnessEffective + capabilitiesEffective + domainEffective;
  
  let grade: string;
  if (finalScore >= 90) grade = "A+";
  else if (finalScore >= 85) grade = "A";
  else if (finalScore >= 80) grade = "B+";
  else if (finalScore >= 75) grade = "B";
  else grade = "C+";
  
  return {
    correctnessScore,
    capabilitiesScore,
    domainScore,
    correctnessEffectiveScore: correctnessEffective,
    capabilitiesEffectiveScore: capabilitiesEffective,
    domainEffectiveScore: domainEffective,
    finalScore,
    grade,
    correctnessConfidence: Math.floor(Math.random() * 10) + 80, // 80-90
    capabilitiesConfidence: Math.floor(Math.random() * 10) + 75, // 75-85
    domainConfidence: Math.floor(Math.random() * 10) + 80, // 80-90
    overallConfidence: Math.floor(Math.random() * 10) + 80 // 80-90
  };
}

// Initialize in-memory arrays from localStorage on module load
let mockAgentAttestations: AgentAttestation[] = [];
let mockHumanAttestations: HumanAttestation[] = [];
let mockAgentInfo: Record<string, AgentVerseInfo> = {};

// Initialize from localStorage if available (browser environment only)
if (typeof window !== 'undefined') {
  try {
    mockAgentAttestations = loadFromStorage(STORAGE_KEYS.AGENT_ATTESTATIONS, DEFAULT_AGENT_ATTESTATIONS);
    mockHumanAttestations = loadFromStorage(STORAGE_KEYS.HUMAN_ATTESTATIONS, DEFAULT_HUMAN_ATTESTATIONS);
    mockAgentInfo = loadFromStorage(STORAGE_KEYS.AGENT_INFO, DEFAULT_AGENT_INFO);
    console.log(`🔧 Initialized mock data from localStorage: ${mockAgentAttestations.length} agents`);
  } catch (error) {
    console.warn('Failed to load from localStorage, using defaults:', error);
    mockAgentAttestations = [...DEFAULT_AGENT_ATTESTATIONS];
    mockHumanAttestations = [...DEFAULT_HUMAN_ATTESTATIONS];
    mockAgentInfo = { ...DEFAULT_AGENT_INFO };
  }
} else {
  // Server-side fallback - always use defaults
  mockAgentAttestations = [...DEFAULT_AGENT_ATTESTATIONS];
  mockHumanAttestations = [...DEFAULT_HUMAN_ATTESTATIONS];
  mockAgentInfo = { ...DEFAULT_AGENT_INFO };
  console.log(`🔧 Server-side: Using default mock data: ${mockAgentAttestations.length} agents`);
}

// Add a new evaluated agent to the mock data
export function addNewEvaluatedAgent(evaluatedAgentAddress: string, evaluationData?: any) {
  console.log(`🔧 Adding new evaluated agent: ${evaluatedAgentAddress}`);
  console.log(`🔧 Evaluation data received:`, evaluationData);
  
  // Generate agent profile (use meTTa data if available)
  const profile = evaluationData?.mettaCategorization 
    ? generateProfileFromMetta(evaluationData.mettaCategorization)
    : generateAgentProfile();
  const walletAddress = generateWalletAddress();
  const attestationUID = generateUID();
  
  // Use actual evaluation data if provided, otherwise generate random scores
  let scores;
  if (evaluationData && evaluationData.finalScore !== undefined) {
    // Use actual evaluation data from the agent
    scores = {
      correctnessScore: evaluationData.correctnessScore || 85,
      capabilitiesScore: evaluationData.capabilitiesScore || 80,
      domainScore: evaluationData.domainScore || 85,
      correctnessEffectiveScore: evaluationData.correctnessEffectiveScore || 34,
      capabilitiesEffectiveScore: evaluationData.capabilitiesEffectiveScore || 24,
      domainEffectiveScore: evaluationData.domainEffectiveScore || 26,
      finalScore: evaluationData.finalScore,
      grade: evaluationData.grade || "B",
      correctnessConfidence: evaluationData.correctnessConfidence || 85,
      capabilitiesConfidence: evaluationData.capabilitiesConfidence || 80,
      domainConfidence: evaluationData.domainConfidence || 85,
      overallConfidence: evaluationData.overallConfidence || 85
    };
  } else {
    // Fallback to random scores if no evaluation data
    scores = generateEvaluationScores();
  }
  
  // Create new agent attestation
  const newAttestation: AgentAttestation = {
    uid: attestationUID,
    attester: "0xAb2DdD48A457b9FE1f7FeE45C6ce0f3D1062A1EA",
    recipient: walletAddress,
    revoked: false,
    revocationTime: 0,
    expirationTime: 0,
    evaluationScore: {
      evaluatedAgentAddress,
      evaluatorAgentAddress: "agent1qf4au6rzaauxhy2jze6v85rspgvredx9m42p0e0cukz0hv4dh2sqjuhujpp",
      timestamp: Math.floor(Date.now() / 1000),
      finalScore: scores.finalScore,
      overallConfidence: scores.overallConfidence,
      grade: scores.grade,
      correctnessScore: scores.correctnessScore,
      correctnessConfidence: scores.correctnessConfidence,
      correctnessEffectiveScore: scores.correctnessEffectiveScore,
      correctnessWeight: 40,
      capabilitiesScore: scores.capabilitiesScore,
      capabilitiesConfidence: scores.capabilitiesConfidence,
      capabilitiesEffectiveScore: scores.capabilitiesEffectiveScore,
      capabilitiesWeight: 30,
      domainScore: scores.domainScore,
      domainConfidence: scores.domainConfidence,
      domainEffectiveScore: scores.domainEffectiveScore,
      domainWeight: 30,
      detailsCID: `bafkreimock${Math.floor(Math.random() * 10000)}evaluation${Date.now()}`
    }
  };
  
  // Add to mock data
  mockAgentAttestations.unshift(newAttestation); // Add to beginning for newest first
  console.log(`🔧 Added attestation, total agents now: ${mockAgentAttestations.length}`);
  
  // Create agent info
  const newAgentInfo: AgentVerseInfo = {
    name: profile.name,
    address: evaluatedAgentAddress,
    description: profile.description,
    domain: profile.domain,
    avatar_href: `https://images.unsplash.com/photo-${Math.floor(Math.random() * 10000000000000000)}?w=100&h=100&fit=crop&crop=center`,
    rating: Math.floor(Math.random() * 20) / 10 + 3.5, // 3.5-5.5
    status: "active",
    category: profile.category
  };
  
  mockAgentInfo[evaluatedAgentAddress] = newAgentInfo;
  console.log(`🔧 Added agent info for ${evaluatedAgentAddress}, total agent info entries: ${Object.keys(mockAgentInfo).length}`);
  
  // Optionally add human attestations (30% chance)
  if (Math.random() < 0.3) {
    const humanAttestationUID = generateUID();
    const humanAttestation: HumanAttestation = {
      uid: humanAttestationUID,
      attester: generateWalletAddress(),
      recipient: walletAddress,
      revoked: false,
      revocationTime: 0,
      expirationTime: 0,
      humanConfirmation: {
        originalAttestationUID: attestationUID,
        approved: Math.random() > 0.1, // 90% approval rate
        confidence: Math.floor(Math.random() * 20) + 75, // 75-95
        reasoning: "Agent demonstrated good performance in evaluation tasks",
        timestamp: Math.floor(Date.now() / 1000) - Math.floor(Math.random() * 3600)
      }
    };
    
    mockHumanAttestations.unshift(humanAttestation);
  }
  
  // Save to localStorage for persistence (browser only)
  if (typeof window !== 'undefined') {
    try {
      saveToStorage(STORAGE_KEYS.AGENT_ATTESTATIONS, mockAgentAttestations);
      saveToStorage(STORAGE_KEYS.HUMAN_ATTESTATIONS, mockHumanAttestations);
      saveToStorage(STORAGE_KEYS.AGENT_INFO, mockAgentInfo);
      console.log(`🔧 Saved to localStorage: ${mockAgentAttestations.length} agents`);
    } catch (error) {
      console.warn('Failed to save to localStorage:', error);
    }
  } else {
    console.log(`🔧 Server-side: Added agent but not saving to localStorage`);
  }
  
  console.log(`✅ Added new agent: ${profile.name} (${scores.finalScore}/100, ${scores.grade})`);
  
  return {
    attestation: newAttestation,
    agentInfo: newAgentInfo
  };
}

// Getter functions for the mock data (use in-memory arrays that are updated)
export function getMockAgentAttestations(): AgentAttestation[] {
  console.log(`🔧 getMockAgentAttestations called, returning ${mockAgentAttestations.length} agents`);
  return [...mockAgentAttestations];
}

export function getMockHumanAttestations(): HumanAttestation[] {
  return [...mockHumanAttestations];
}

export function getMockAgentInfo(address: string): AgentVerseInfo | null {
  return mockAgentInfo[address] || null;
}

export function getAllMockAgentInfo(): Record<string, AgentVerseInfo> {
  return { ...mockAgentInfo };
}

// Clear all mock data (useful for testing)
export function clearMockData(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(STORAGE_KEYS.AGENT_ATTESTATIONS);
    localStorage.removeItem(STORAGE_KEYS.HUMAN_ATTESTATIONS);
    localStorage.removeItem(STORAGE_KEYS.AGENT_INFO);
    console.log('🧹 Cleared all mock data');
  }
}
