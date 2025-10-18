"use server";

import { AgentVerseInfo } from "@/types/agents";

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
      rating: data.rating || "",
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
