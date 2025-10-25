"use server";

import { AgentVerseInfo } from "@/types/agents";

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

const AGENTVERSE_AGENT_INFO_URL = `https://agentverse.ai/v1/search/agents`;

export async function fetchAgentverseInfo(
  address: string
): Promise<AgentVerseInfo | null> {
  try {
    const response = await fetch(`${AGENTVERSE_AGENT_INFO_URL}/${address}`, {
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

export async function fetchMultipleAgentverseInfo(
  addresses: string[]
): Promise<Map<string, AgentVerseInfo>> {
  const results = new Map<string, AgentVerseInfo>();

  const promises = addresses.map(async (address) => {
    const info = await fetchAgentverseInfo(address);
    if (info) {
      results.set(address, info);
    }
  });

  await Promise.all(promises);

  return results;
}

export async function sendMessageToAgent(
  message: string,
  sessionId?: string
): Promise<{ response: string; sessionId: string }> {
  try {
    // process.env.EVALUATOR_AGENT_ADDRESS
    const agentAddress =
      "agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4";
    const agentverseApiKey = process.env.AGENTVERSE_API_KEY;

    if (!agentverseApiKey) {
      throw new Error("AGENTVERSE_API_KEY environment variable is required");
    }

    // Use Agentverse messaging API
    const response = await fetch(
      `https://agentverse.ai/v1/agents/${agentAddress}/message`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${agentverseApiKey}`,
        },
        body: JSON.stringify({
          message: message,
          session_id: sessionId || generateSessionId(),
        }),
        cache: "no-store",
      }
    );

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
      response: `❌ Could not connect to the Agentverse agent. Make sure:
1. Your AGENTVERSE_API_KEY is set correctly
2. The agent is deployed and running on Agentverse
3. The agent address is correct: agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4

Error: ${error instanceof Error ? error.message : "Unknown error"}`,
      sessionId: sessionId || generateSessionId(),
    };
  }
}

function generateSessionId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}
