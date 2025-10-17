import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { PieChart } from "@/components/ui/pie-chart";
import { Attestation } from "@/types/attestation";
import Link from "next/link";

export interface EvaluatedAgent {
  name: string;
  jsonAttestation: Attestation;
}

interface EvaluatedAgentListItemProps {
  agent: EvaluatedAgent;
}

export function EvaluatedAgentListItem({ agent }: EvaluatedAgentListItemProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return "#10b981"; // green-500
    if (score >= 60) return "#3b82f6"; // blue-500
    if (score >= 40) return "#f59e0b"; // amber-500
    return "#ef4444"; // red-500
  };

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

  const attestation = agent.jsonAttestation;

  return (
    <div className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-muted/30 transition-colors">
      <div className="flex items-center space-x-6">
        <div className="flex items-center justify-center w-8 h-8 bg-muted rounded-full">
          <span className="text-sm font-medium text-muted-foreground">#</span>
        </div>

        <div className="flex flex-col">
          <Link
            href={`/agents/${attestation.agent_id}`}
            className="font-medium text-foreground hover:text-blue-600 transition-colors hover:underline"
          >
            {agent.name}
          </Link>
          <span className="text-sm text-muted-foreground">
            {attestation.agent_id.substring(0, 10)}...
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-6">
        <HoverCard>
          <HoverCardTrigger asChild>
            <button className="p-2 hover:bg-muted rounded-lg transition-colors">
              <PieChart size={64} attestation={attestation} />
            </button>
          </HoverCardTrigger>
          <HoverCardContent className="w-96">
            <div className="space-y-4">
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="font-semibold text-base">
                    Performance Metrics
                  </h4>
                  <p className="text-xs text-muted-foreground mt-1">
                    {attestation.evaluator}
                  </p>
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold">{attestation.grade}</div>
                  <div className="text-xs text-muted-foreground">
                    {attestation.final_score.toFixed(1)}/100
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                {Object.entries(attestation.metrics).map(([key, metric]) => (
                  <div key={key} className="space-y-1.5">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium capitalize">
                        {key}
                      </span>
                      <span className="text-sm font-semibold">
                        {metric.effective_score.toFixed(1)}
                      </span>
                    </div>
                    <div className="flex gap-2 items-center">
                      <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          className="h-full transition-all"
                          style={{
                            width: `${metric.effective_score}%`,
                            backgroundColor: getScoreColor(
                              metric.effective_score
                            ),
                          }}
                        />
                      </div>
                      <span className="text-xs text-muted-foreground w-16 text-right">
                        {metric.confidence.toFixed(0)}% conf
                      </span>
                    </div>
                    {metric.failures.length > 0 && (
                      <div className="text-xs text-muted-foreground pl-1">
                        ⚠ {metric.failures.length} failure(s)
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="pt-2 border-t border-border">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Overall Confidence</span>
                  <span className="font-medium">
                    {attestation.overall_confidence.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </HoverCardContent>
        </HoverCard>

        <div className="flex flex-col items-center min-w-20">
          <span className="text-sm font-medium text-foreground">
            Confidence
          </span>
          <span className="text-xs text-muted-foreground">
            {attestation.overall_confidence.toFixed(0)}%
          </span>
        </div>

        <div className="flex flex-col items-center min-w-24">
          <span className="text-sm font-medium text-foreground">Evaluator</span>
          <span className="text-xs text-muted-foreground">
            {attestation.evaluator.split("-")[0]}
          </span>
        </div>

        <div className="flex flex-col items-center min-w-16">
          <span className="text-sm font-medium text-foreground">Grade</span>
          <span
            className={`text-xs px-2 py-1 rounded-full font-medium ${getGradeColor(
              attestation.grade
            )}`}
          >
            {attestation.grade}
          </span>
        </div>
      </div>
    </div>
  );
}
