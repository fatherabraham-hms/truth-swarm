"use server";

import { AgentVerseInfo } from "@/types/agents";

// Types for chat interaction
export interface ChatMessage {
  role: "user" | "agent";
  content: string;
  timestamp: number;
}

export interface AgentChatSession {
  sessionId: string;
  agentAddress: string;
  messages: ChatMessage[];
}

// Url defintions

const agentInfoUrl = `https://agentverse.ai/v1/search/agents`;

/**
 * Fetch agent information from Agentverse API
 * @param address - The agent address to fetch
 * @returns AgentVerseInfo or null if not found
 */
export async function fetchAgentverseInfo(
  address: string
): Promise<AgentVerseInfo | null> {
  try {
    const response = await fetch(`${agentInfoUrl}/${address}`, {
      next: { revalidate: 3600 }, // Cache for 1 hour
    });

    if (!response.ok) {
      console.warn(`Agent ${address} not found in Agentverse`);
      return null;
    }

    const data = await response.json();

    return {
      name: data.name || "Unknown Agent",
      address: data.address || address,
      description: data.description || "",
      domain: data.domain || "",
      avatar_href: data.avatar_href || "",
      rating: data.rating || 0,
      status: data.status || "unknown",
      category: data.category || "",
    };
  } catch (error) {
    console.error(`Failed to fetch agent ${address}:`, error);
    return null;
  }
}

/**
 * Fetch multiple agent information from Agentverse API
 * @param addresses - Array of agent addresses to fetch
 * @returns Map of address to AgentVerseInfo
 */
export async function fetchMultipleAgentverseInfo(
  addresses: string[]
): Promise<Map<string, AgentVerseInfo>> {
  const results = new Map<string, AgentVerseInfo>();

  // Fetch all agents in parallel
  const promises = addresses.map(async (address) => {
    const info = await fetchAgentverseInfo(address);
    if (info) {
      results.set(address, info);
    }
  });

  await Promise.all(promises);

  return results;
}

/**
 * Send a message to an agent and get a response
 * This uses the Agentverse webhook/endpoint for the agent
 * @param agentAddress - The agent's address
 * @param message - The message to send
 * @param sessionId - Optional session ID for continuity
 * @returns The agent's response
 */
export async function sendMessageToAgent(
  agentAddress: string,
  message: string,
  sessionId?: string
): Promise<{ response: string; sessionId: string }> {
  try {
    const evaluatorUrl =
      process.env.NEXT_PUBLIC_EVALUATOR_AGENT_URL || "http://localhost:8000";

    // Send message to agent's chat endpoint (with ASI:1 integration)
    const response = await fetch(`${evaluatorUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        session_id: sessionId || generateSessionId(),
      }),
      cache: "no-store",
    });

    if (!response.ok) {
      throw new Error(
        `Agent communication failed: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    return {
      response: data.response,
      sessionId: data.session_id || sessionId || generateSessionId(),
    };
  } catch (error) {
    console.error(`Failed to communicate with evaluator:`, error);

    return {
      response: `❌ Could not connect to the evaluator agent. Make sure it's running at ${
        process.env.NEXT_PUBLIC_EVALUATOR_AGENT_URL || "http://localhost:8000"
      }

Error: ${error instanceof Error ? error.message : "Unknown error"}`,
      sessionId: sessionId || generateSessionId(),
    };
  }
}

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}

export async function getSampleAgentAddress(): Promise<string> {
  return "agent1qw254tc8q3mcmrseem0pmhu2jd0j7urn2e9cd5tgcg88kmy9wkqhysksdwf";
}

/**
 * Test connection to the local evaluator agent
 * Useful for debugging connectivity issues
 */
export async function testAgentConnection(): Promise<{
  connected: boolean;
  agentAddress?: string;
  error?: string;
}> {
  try {
    const evaluatorUrl =
      process.env.NEXT_PUBLIC_EVALUATOR_AGENT_URL || "http://localhost:8000";

    const response = await fetch(evaluatorUrl, {
      method: "GET",
      cache: "no-store",
    });

    if (response.ok) {
      return {
        connected: true,
        agentAddress: process.env.NEXT_PUBLIC_EVALUATOR_AGENT_ADDRESS,
      };
    }

    return {
      connected: false,
      error: `Agent responded with status: ${response.status}`,
    };
  } catch (error) {
    return {
      connected: false,
      error:
        error instanceof Error ? error.message : "Unknown connection error",
    };
  }
}
