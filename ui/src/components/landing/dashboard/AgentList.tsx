"use client";

import { AgentListItem } from "./AgentListItem";
import { Agent } from "@/types/agents";

interface AgentsListProps {
  filteredAgentsList: Agent[];
  tabValue: string;
}

export function AgentList({ filteredAgentsList, tabValue }: AgentsListProps) {
  const getTabText = (tabValue: string) => {
    switch (tabValue) {
      case "all":
        return "Showing all agents";
      case "human":
        return "Showing human-verified agents";
      case "agent":
        return "Showing evaluated agents";
      default:
        return "Showing evaluated agents";
    }
  };

  const getTabCount = (tabValue: string) => {
    switch (tabValue) {
      case "all":
        return filteredAgentsList.length;
      case "human":
        return filteredAgentsList.filter((agent) => agent.humanVerified).length;
      case "agent":
        return filteredAgentsList.filter((agent) => agent.finalScore > 0)
          .length;
      default:
        return filteredAgentsList.length;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between p-4 bg-muted/50 rounded-lg">
        <p className="text-sm text-muted-foreground">{getTabText(tabValue)}</p>
        <span className="text-sm font-medium text-foreground">
          {getTabCount(tabValue)} agents
        </span>
      </div>

      <div className="space-y-2">
        {filteredAgentsList.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            No agent evaluations found for this tab
          </div>
        ) : (
          filteredAgentsList.map((agent, index) => (
            <AgentListItem key={index} agent={agent} />
          ))
        )}
      </div>
    </div>
  );
}
