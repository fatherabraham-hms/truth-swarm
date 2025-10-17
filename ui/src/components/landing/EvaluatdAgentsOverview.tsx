import { Input } from "../ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { EvaluatedAgent } from "./EvaluatedAgentListItems";
import { EvaluatedAgentsList } from "./EvaluatedAgentsList";
import { Attestation } from "@/types/attestation";

const mockAgent1: EvaluatedAgent = {
  name: "mettalex dex",
  jsonAttestation: {
    agent_id: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    evaluator: "truth-swarm-metta-v1",
    timestamp: "2025-10-15T10:30:00Z",
    final_score: 78.5,
    overall_confidence: 85.2,
    grade: "B+",
    metrics: {
      correctness: {
        score: 85.0,
        confidence: 92.0,
        effective_score: 78.2,
        evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
        failures: ["TC-CAP-004: FAIL - No MEV protection"],
        weight: 0.15,
      },
      capabilities: {
        score: 92.0,
        confidence: 95.0,
        effective_score: 87.4,
        evidence: ["TC-FUNC-001: 92% exact match", "TC-FUNC-002: 100% correct"],
        failures: ["TC-FUNC-003: 8% incorrect error messages"],
        weight: 0.2,
      },
      domain: {
        score: 75.0,
        confidence: 80.0,
        effective_score: 60.0,
        evidence: ["TC-DOM-001: PASS", "TC-DOM-004: PASS"],
        failures: [
          "TC-DOM-005: FAIL - No MEV protection",
          "TC-DOM-002: WARN - Inconsistent liquidity warnings",
        ],
        weight: 0.2,
      },
    },
  } as Attestation,
};

const mockAgent2: EvaluatedAgent = {
  name: "unadivsooor",
  jsonAttestation: {
    agent_id: "0x8f3a21B0C5e0F6C8D9A5B4C3D2E1F0A9B8C7D6E5",
    evaluator: "truth-swarm-metta-v1",
    timestamp: "2025-10-14T14:20:00Z",
    final_score: 32.8,
    overall_confidence: 75.5,
    grade: "F",
    metrics: {
      correctness: {
        score: 25.0,
        confidence: 85.0,
        effective_score: 21.2,
        evidence: ["TC-CAP-001: FAIL"],
        failures: [
          "TC-CAP-002: FAIL - Incorrect data format",
          "TC-CAP-003: FAIL - Missing validations",
          "TC-CAP-004: FAIL - Security vulnerabilities",
        ],
        weight: 0.15,
      },
      capabilities: {
        score: 40.0,
        confidence: 70.0,
        effective_score: 28.0,
        evidence: ["TC-FUNC-002: 40% correct"],
        failures: [
          "TC-FUNC-001: FAIL - Poor accuracy",
          "TC-FUNC-003: FAIL - Inconsistent responses",
        ],
        weight: 0.2,
      },
      domain: {
        score: 45.0,
        confidence: 72.0,
        effective_score: 32.4,
        evidence: ["TC-DOM-003: PASS"],
        failures: [
          "TC-DOM-001: FAIL - Domain knowledge gaps",
          "TC-DOM-002: FAIL - Incorrect terminology",
        ],
        weight: 0.2,
      },
    },
  } as Attestation,
};

const mockAgent3: EvaluatedAgent = {
  name: "weather oracle",
  jsonAttestation: {
    agent_id: "0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b",
    evaluator: "truth-swarm-metta-v1",
    timestamp: "2025-10-16T08:15:00Z",
    final_score: 91.3,
    overall_confidence: 94.7,
    grade: "A",
    metrics: {
      correctness: {
        score: 95.0,
        confidence: 98.0,
        effective_score: 93.1,
        evidence: [
          "TC-CAP-001: PASS",
          "TC-CAP-002: PASS",
          "TC-CAP-003: PASS",
          "TC-CAP-004: PASS",
        ],
        failures: [],
        weight: 0.15,
      },
      capabilities: {
        score: 92.0,
        confidence: 96.0,
        effective_score: 88.3,
        evidence: [
          "TC-FUNC-001: 95% exact match",
          "TC-FUNC-002: 100% correct",
          "TC-FUNC-003: 98% accurate",
        ],
        failures: [],
        weight: 0.2,
      },
      domain: {
        score: 90.0,
        confidence: 92.0,
        effective_score: 82.8,
        evidence: ["TC-DOM-001: PASS", "TC-DOM-002: PASS", "TC-DOM-003: PASS"],
        failures: ["TC-DOM-004: WARN - Minor edge case handling"],
        weight: 0.2,
      },
    },
  } as Attestation,
};

const mockAgent4: EvaluatedAgent = {
  name: "price feed",
  jsonAttestation: {
    agent_id: "0x9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e",
    evaluator: "truth-swarm-metta-v1",
    timestamp: "2025-10-13T16:45:00Z",
    final_score: 68.2,
    overall_confidence: 81.3,
    grade: "C+",
    metrics: {
      correctness: {
        score: 70.0,
        confidence: 85.0,
        effective_score: 59.5,
        evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS"],
        failures: ["TC-CAP-003: FAIL - Latency issues"],
        weight: 0.15,
      },
      capabilities: {
        score: 75.0,
        confidence: 88.0,
        effective_score: 66.0,
        evidence: ["TC-FUNC-001: 78% exact match", "TC-FUNC-002: 85% correct"],
        failures: ["TC-FUNC-003: WARN - Occasional timeouts"],
        weight: 0.2,
      },
      domain: {
        score: 65.0,
        confidence: 78.0,
        effective_score: 50.7,
        evidence: ["TC-DOM-001: PASS"],
        failures: [
          "TC-DOM-002: FAIL - Limited market coverage",
          "TC-DOM-003: WARN - Price staleness",
        ],
        weight: 0.2,
      },
    },
  } as Attestation,
};

const mockAgent5: EvaluatedAgent = {
  name: "data aggregator",
  jsonAttestation: {
    agent_id: "0x5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0b9a8f7e6d",
    evaluator: "truth-swarm-metta-v1",
    timestamp: "2025-10-17T12:00:00Z",
    final_score: 82.7,
    overall_confidence: 88.9,
    grade: "B",
    metrics: {
      correctness: {
        score: 88.0,
        confidence: 93.0,
        effective_score: 81.8,
        evidence: ["TC-CAP-001: PASS", "TC-CAP-002: PASS", "TC-CAP-003: PASS"],
        failures: [],
        weight: 0.15,
      },
      capabilities: {
        score: 85.0,
        confidence: 91.0,
        effective_score: 77.3,
        evidence: ["TC-FUNC-001: 87% exact match", "TC-FUNC-002: 95% correct"],
        failures: ["TC-FUNC-003: WARN - Minor formatting issues"],
        weight: 0.2,
      },
      domain: {
        score: 78.0,
        confidence: 84.0,
        effective_score: 65.5,
        evidence: ["TC-DOM-001: PASS", "TC-DOM-002: PASS"],
        failures: ["TC-DOM-003: WARN - Limited source diversity"],
        weight: 0.2,
      },
    },
  } as Attestation,
};

const mockAgents = [mockAgent1, mockAgent2, mockAgent3, mockAgent4, mockAgent5];

export function EvaluatedAgentsOverview() {
  const getAllAgents = () => mockAgents;
  const getHumanVerifiedAgents = () =>
    mockAgents.filter(
      (agent) =>
        agent.jsonAttestation && agent.jsonAttestation.final_score >= 80
    );
  const getEvaluatedAgents = () =>
    mockAgents.filter(
      (agent) => agent.jsonAttestation && agent.jsonAttestation.final_score > 0
    );

  return (
    <div className="px-10">
      {/** Search & Filter */}
      <h2 className="text-xl text-foreground mb-4 ">Evaluated Agents</h2>

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
            <TabsTrigger value="account">Human verified</TabsTrigger>
            <TabsTrigger value="wip">Evaluated</TabsTrigger>
          </TabsList>
          <TabsContent value="all">
            <EvaluatedAgentsList
              filteredAgentsList={getAllAgents()}
              tabValue="all"
            />
          </TabsContent>
          <TabsContent value="account">
            <EvaluatedAgentsList
              filteredAgentsList={getHumanVerifiedAgents()}
              tabValue="account"
            />
          </TabsContent>
          <TabsContent value="wip">
            <EvaluatedAgentsList
              filteredAgentsList={getEvaluatedAgents()}
              tabValue="wip"
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
