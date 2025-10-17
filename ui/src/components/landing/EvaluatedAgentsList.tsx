"use client";

import {
  EvaluatedAgent,
  EvaluatedAgentListItem,
} from "./EvaluatedAgentListItems";

interface EvaluatedAgentsListProps {
  filteredAgentsList: EvaluatedAgent[];
  tabValue: string;
}

export function EvaluatedAgentsList({
  filteredAgentsList,
  tabValue,
}: EvaluatedAgentsListProps) {
  const getTabText = (tabValue: string) => {
    switch (tabValue) {
      case "all":
        return "Showing all evaluated agents";
      case "account":
        return "Showing human-verified agents only";
      case "wip":
        return "Showing agents currently being evaluated";
      default:
        return "Showing evaluated agents";
    }
  };

  const getTabCount = (tabValue: string) => {
    switch (tabValue) {
      case "all":
        return filteredAgentsList.length;
      case "account":
        return filteredAgentsList.filter(
          (agent) =>
            agent.jsonAttestation && agent.jsonAttestation.final_score >= 80
        ).length;
      case "wip":
        return filteredAgentsList.filter(
          (agent) =>
            agent.jsonAttestation && agent.jsonAttestation.final_score > 0
        ).length;
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
            No agents found for this tab
          </div>
        ) : (
          filteredAgentsList.map((agent, index) => (
            <EvaluatedAgentListItem key={index} agent={agent} />
          ))
        )}
      </div>
    </div>
  );
}
