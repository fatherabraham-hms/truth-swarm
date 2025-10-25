"use client";

import { useMemo } from "react";
import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { History, Eye } from "lucide-react";
import { AgentList } from "./dashboard/AgentList";
import { AttestationWatcher } from "./dashboard/AttestationWatcher";
import { useAgents } from "@/hooks/useAgents";
import {
  useAgentAttestations,
  useHumanAttestations,
} from "@/hooks/useAttestation";

export function Dashboard() {
  const agentAttestationsQuery = useAgentAttestations();
  const humanAttestationsQuery = useHumanAttestations();

  const agentAttestations = useMemo(
    () => agentAttestationsQuery.data || [],
    [agentAttestationsQuery.data]
  );
  const humanAttestations = useMemo(
    () => humanAttestationsQuery.data || [],
    [humanAttestationsQuery.data]
  );

  const {
    agents,
    isLoading: isLoadingAgents,
    error: agentsError,
  } = useAgents(agentAttestations, humanAttestations);



  if (
    agentAttestationsQuery.isLoading ||
    humanAttestationsQuery.isLoading ||
    isLoadingAgents
  ) {
    return (
      <div className="px-10 py-8">
        <div className="text-center text-muted-foreground">
          Loading agents...
        </div>
      </div>
    );
  }

  if (
    agentAttestationsQuery.error ||
    humanAttestationsQuery.error ||
    agentsError
  ) {
    return (
      <div className="px-10 py-8">
        <div className="text-center text-red-500">
          Error loading agents. Please try again.
        </div>
      </div>
    );
  }

  if (!agentAttestationsQuery.data || !humanAttestationsQuery.data) {
    return (
      <div className="px-10 py-8">
        <div className="text-center text-muted-foreground">
          No data available
        </div>
      </div>
    );
  }

  const getAllAgents = () => agents;

  const getHumanVerifiedAgents = () =>
    agents.filter((agent) => agent.humanVerified);

  const getEvaluatedAgents = () =>
    agents.filter((agent) => agent.finalScore > 0);

  return (
    <>
      {/* Blockscout SDK: Real-time attestation event monitoring with toast notifications */}
      <AttestationWatcher />
      
      <div className="px-10 mx-auto">
        {/** Header with Blockscout Transaction History */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl text-foreground">Evaluated Agents</h2>
          

        </div>

        {/** Search & Filter */}
        <div className="grid grid-cols-12 mb-4">
          <div className="col-span-8">
            <Input placeholder="Search evaluated agents" />
          </div>
          <div className="col-span-4 flex justify-start pl-4 space-x-2">
            <span className="mt-1.5">filter</span>
            <Select>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Agent Type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="light">DeFi</SelectItem>
                <SelectItem value="dark">Weather</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

      {/** Agents List with metrics */}
      <div>
        <Tabs defaultValue="all" className="w-full">
          <TabsList>
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="human">Human verified</TabsTrigger>
            <TabsTrigger value="agent">Evaluated</TabsTrigger>
          </TabsList>
          <TabsContent value="all">
            <AgentList filteredAgentsList={getAllAgents()} tabValue="all" />
          </TabsContent>
          <TabsContent value="human">
            <AgentList
              filteredAgentsList={getHumanVerifiedAgents()}
              tabValue="human"
            />
          </TabsContent>
          <TabsContent value="agent">
            <AgentList
              filteredAgentsList={getEvaluatedAgents()}
              tabValue="agent"
            />
          </TabsContent>
        </Tabs>
      </div>
      </div>
    </>
  );
}
