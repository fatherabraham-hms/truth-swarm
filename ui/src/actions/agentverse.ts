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

/**
 * Fetch agent information from Agentverse API
 * @param address - The agent address to fetch
 * @returns AgentVerseInfo or null if not found
 */
export async function fetchAgentverseInfo(
  address: string
): Promise<AgentVerseInfo | null> {
  try {
    const response = await fetch(
      `https://agentverse.ai/v1/search/agents/${address}`,
      {
        next: { revalidate: 3600 }, // Cache for 1 hour
      }
    );

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
    // Agentverse agents typically expose HTTP endpoints
    // The endpoint format is: https://agentverse.ai/v1beta1/engine/chat
    const response = await fetch("https://agentverse.ai/v1beta1/engine/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        agent_address: agentAddress,
        message: {
          type: "text",
          content: message,
        },
        session_id: sessionId || generateSessionId(),
      }),
      cache: "no-store", // Don't cache chat responses
    });

    if (!response.ok) {
      throw new Error(
        `Agent communication failed: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    return {
      response:
        data.message?.content || data.response || "No response from agent",
      sessionId: data.session_id || sessionId || generateSessionId(),
    };
  } catch (error) {
    console.error(`Failed to send message to agent ${agentAddress}:`, error);

    // Return a fallback response for demo purposes
    return {
      response: `I'm having trouble connecting to the agent right now. This is a simulated response for development. You asked: "${message}"`,
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
