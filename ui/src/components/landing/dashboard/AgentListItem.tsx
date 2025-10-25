import { AgentScorePieChart } from "@/components/landing/dashboard/AgentScorePieChart";
import { Agent } from "@/types/agents";
import Link from "next/link";
import Image from "next/image";

interface EvaluatedAgentListItemProps {
  agent: Agent;
}

export function AgentListItem({ agent }: EvaluatedAgentListItemProps) {
  const getGradeColor = (grade: string) => {
    if (grade.startsWith("A") || grade.startsWith("B+")) {
      return "text-green-600 bg-green-50";
    } else if (grade.startsWith("B") || grade.startsWith("C")) {
      return "text-blue-600 bg-blue-50";
    } else if (grade.startsWith("D")) {
      return "text-amber-600 bg-amber-50";
    } else {
      return "text-red-600 bg-red-50";
    }
  };

  return (
    <div className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-muted/30 transition-colors">
      <div className="flex items-center space-x-6">
        <div className="flex items-center justify-center w-8 h-8 bg-muted rounded-full">
          <span className="text-sm font-medium text-muted-foreground">
            <Image 
              src={agent.avatarHref} 
              alt="agent avatar" 
              width={32}
              height={32}
              className="rounded-full"
            />
            {/** # -> First letter if no image */}
          </span>
        </div>

        <div className="flex flex-col">
          <Link
            href={`/agent-evaluation-detail/${agent.evaluatedAgentAddress}`}
            className="font-medium text-foreground hover:text-blue-600 transition-colors hover:underline"
          >
            {agent.agentName}
          </Link>
          <a
            href={`https://agentverse.ai/agents/details/${agent.evaluatedAgentAddress}/profile`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-muted-foreground hover:text-blue-600 transition-colors hover:underline"
          >
            {agent.evaluatedAgentAddress.substring(0, 10)}...
          </a>
        </div>
      </div>

      <div className="flex items-center space-x-6">
        <div className="p-2">
          <AgentScorePieChart
            evalScore={{
              evaluatedAgentAddress: agent.evaluatedAgentAddress,
              evaluatorAgentAddress: agent.evaluatorAgentAddress,
              timestamp: agent.timestamp,
              finalScore: agent.finalScore,
              overallConfidence: agent.overallConfidence,
              grade: agent.grade,
              correctnessScore: agent.correctnessScore,
              correctnessConfidence: agent.correctnessConfidence,
              correctnessEffectiveScore: agent.correctnessEffectiveScore,
              correctnessWeight: agent.correctnessWeight,
              capabilitiesScore: agent.capabilitiesScore,
              capabilitiesConfidence: agent.capabilitiesConfidence,
              capabilitiesEffectiveScore: agent.capabilitiesEffectiveScore,
              capabilitiesWeight: agent.capabilitiesWeight,
              domainScore: agent.domainScore,
              domainConfidence: agent.domainConfidence,
              domainEffectiveScore: agent.domainEffectiveScore,
              domainWeight: agent.domainWeight,
              detailsCID: agent.detailsCID,
            }}
            size={64}
          />
        </div>

        <div className="flex flex-col items-center min-w-20">
          <span className="text-sm font-medium text-foreground">
            Final Score
          </span>
          <span className="text-xs text-muted-foreground">
            {agent.finalScore.toFixed(0)}%
          </span>
        </div>

        <div className="flex flex-col items-center min-w-20">
          <span className="text-sm font-medium text-foreground">
            Confidence
          </span>
          <span className="text-xs text-muted-foreground">
            {agent.overallConfidence.toFixed(0)}%
          </span>
        </div>
        <div className="flex flex-col items-center min-w-16">
          <span className="text-sm font-medium text-foreground">Grade</span>
          <span
            className={`text-xs px-2 py-1 rounded-full font-medium ${getGradeColor(
              agent.grade
            )}`}
          >
            {agent.grade}
          </span>
        </div>

        <div className="flex flex-col items-center min-w-24">
          <span className="text-sm font-medium text-foreground">Evaluator</span>
          <span className="text-xs text-muted-foreground">
            <a
              href={`https://agentverse.ai/agents/details/${agent.evaluatorAgentAddress}/profile`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-muted-foreground hover:text-blue-600 transition-colors hover:underline"
            >
              {agent.evaluatorAgentAddress.substring(0, 10)}...
            </a>
          </span>
        </div>
      </div>
    </div>
  );
}
