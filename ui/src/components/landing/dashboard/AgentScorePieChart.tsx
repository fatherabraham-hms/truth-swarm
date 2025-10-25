"use client";

import { Pie, PieChart } from "recharts";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { EvaluationScore } from "@/types/attestation";

interface AgentScorePieChartProps {
  evalScore: EvaluationScore;
  size?: number;
}

export function AgentScorePieChart({
  evalScore,
  size = 80,
}: AgentScorePieChartProps) {
  // Color function based on effective score
  const getScoreColor = (effectiveScore: number): string => {
    if (effectiveScore >= 80) return "#10b981"; // green
    if (effectiveScore >= 60) return "#eab308"; // yellow
    return "#ef4444"; // red
  };

  // Prepare chart data from the evaluation score
  const chartData = [
    {
      metric: "Correctness",
      value: evalScore.correctnessWeight,
      effectiveScore: evalScore.correctnessEffectiveScore,
      score: evalScore.correctnessScore,
      confidence: evalScore.correctnessConfidence,
      fill: getScoreColor(evalScore.correctnessEffectiveScore),
    },
    {
      metric: "Capabilities",
      value: evalScore.capabilitiesWeight,
      effectiveScore: evalScore.capabilitiesEffectiveScore,
      score: evalScore.capabilitiesScore,
      confidence: evalScore.capabilitiesConfidence,
      fill: getScoreColor(evalScore.capabilitiesEffectiveScore),
    },
    {
      metric: "Domain",
      value: evalScore.domainWeight,
      effectiveScore: evalScore.domainEffectiveScore,
      score: evalScore.domainScore,
      confidence: evalScore.domainConfidence,
      fill: getScoreColor(evalScore.domainEffectiveScore),
    },
  ];

  const chartConfig = {
    value: {
      label: "Weight",
    },
    Correctness: {
      label: "Correctness",
    },
    Capabilities: {
      label: "Capabilities",
    },
    Domain: {
      label: "Domain",
    },
  } satisfies ChartConfig;

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <button className="relative hover:opacity-80 transition-opacity">
          <div style={{ width: size, height: size }}>
            <ChartContainer config={chartConfig} className="w-full h-full">
              <PieChart>
                <Pie
                  data={chartData}
                  dataKey="value"
                  nameKey="metric"
                  cx="50%"
                  cy="50%"
                  outerRadius="90%"
                  paddingAngle={2}
                />
              </PieChart>
            </ChartContainer>
          </div>
        </button>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <h4 className="font-semibold text-base">Performance Metrics</h4>
              <p className="text-xs text-muted-foreground mt-1">
                Evaluation Score Breakdown
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold">{evalScore.grade}</div>
              <div className="text-xs text-muted-foreground">
                {evalScore.finalScore.toFixed(1)}/100
              </div>
            </div>
          </div>

          <div className="space-y-3">
            {chartData.map((item) => (
              <div key={item.metric} className="space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium">{item.metric}</span>
                  <span className="text-sm font-semibold">
                    {item.effectiveScore.toFixed(1)}
                  </span>
                </div>
                <div className="flex gap-2 items-center">
                  <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full transition-all"
                      style={{
                        width: `${item.effectiveScore}%`,
                        backgroundColor: item.fill,
                      }}
                    />
                  </div>
                  <span className="text-xs text-muted-foreground w-16 text-right">
                    {item.confidence.toFixed(0)}% conf
                  </span>
                </div>
                <div className="text-xs text-muted-foreground pl-1">
                  Score: {item.score.toFixed(1)} • Weight:{" "}
                  {item.value.toFixed(2)}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-border">
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Overall Confidence</span>
              <span className="font-medium">
                {evalScore.overallConfidence.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
}
