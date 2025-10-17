import React from "react";
import { Attestation } from "@/types/attestation";

interface PieChartProps {
  size?: number;
  className?: string;
  attestation: Attestation;
}

export function PieChart({
  size = 80,
  className = "",
  attestation,
}: PieChartProps) {
  const getScoreColor = (score: number): string => {
    if (score >= 80) return "#10b981"; // green-500
    if (score >= 60) return "#3b82f6"; // blue-500
    if (score >= 40) return "#f59e0b"; // amber-500
    return "#ef4444"; // red-500
  };

  const metrics = [
    { name: "Correctness", data: attestation.metrics.correctness },
    { name: "Capabilities", data: attestation.metrics.capabilities },
    { name: "Domain", data: attestation.metrics.domain },
  ];

  // Calculate total weight for proper proportions
  const totalWeight = metrics.reduce((sum, m) => sum + m.data.weight, 0);

  // Gap between slices (in percentage of the circle)
  const gapPercentage = 2;
  const totalGaps = metrics.length * gapPercentage;
  const availablePercentage = 100 - totalGaps;

  return (
    <div
      className={`relative ${className}`}
      style={{ width: size, height: size }}
    >
      <svg viewBox="0 0 100 100" className="transform -rotate-90 w-full h-full">
        {metrics.map((metric, i) => {
          // Calculate the percentage of the circle this metric occupies (excluding gaps)
          const slicePercentage =
            (metric.data.weight / totalWeight) * availablePercentage;

          // Calculate the starting position including all previous slices and gaps
          const prevSlicesTotal = metrics.slice(0, i).reduce((sum, m) => {
            return sum + (m.data.weight / totalWeight) * availablePercentage;
          }, 0);
          const prevGaps = i * gapPercentage;

          const strokeDasharray = `${slicePercentage} ${100 - slicePercentage}`;
          const strokeDashoffset = -(
            prevSlicesTotal +
            prevGaps +
            gapPercentage / 2
          );

          return (
            <circle
              key={i}
              cx="50"
              cy="50"
              r="15.915" // radius where circumference = 100 (2πr = 100, so r ≈ 15.915)
              fill="transparent"
              stroke={getScoreColor(metric.data.effective_score)}
              strokeWidth="31.83"
              strokeDasharray={strokeDasharray}
              strokeDashoffset={strokeDashoffset}
              className="transition-all duration-300"
            />
          );
        })}
      </svg>

      {/* Center text showing final score */}
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-sm font-bold text-foreground">
          {Math.round(attestation.final_score)}
        </span>
      </div>
    </div>
  );
}
