"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, ExternalLink } from "lucide-react";
import {
  useEvaluationDetails,
  EvaluationScoreWithDetails,
  MetricDetail
} from "@/hooks/useEvaluationDetails";
import { HumanAttestationDialog } from "./HCAConfirmationDialog";

interface EvaluationDetailsOverviewProps {
  detailsCID: string;
  attestationUID: string;
  agentName: string;
  onVerificationSuccess?: () => void;
}

export function EvaluationDetailsOverview({
  detailsCID,
  attestationUID,
  agentName,
  onVerificationSuccess,
}: EvaluationDetailsOverviewProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const { data: details, isLoading } = useEvaluationDetails(detailsCID);

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600";
    if (score >= 60) return "text-yellow-600";
    if (score >= 40) return "text-amber-600";
    return "text-red-600";
  };

  const MetricDetails = ({
    name,
    metric,
  }: {
    name: string;
    metric: MetricDetail;
  }) => (
    <div className="space-y-3 p-4 bg-card rounded-lg border border-border">
      <div className="flex justify-between items-start">
        <h4 className="font-semibold text-sm">{name}</h4>
        <span className={`text-lg font-bold ${getScoreColor(metric.score)}`}>
          {metric.score.toFixed(1)}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <div>
          <span className="text-muted-foreground">Confidence:</span>
          <span className="ml-2 font-medium">
            {metric.confidence.toFixed(1)}%
          </span>
        </div>
        <div>
          <span className="text-muted-foreground">Weight:</span>
          <span className="ml-2 font-medium">
            {(metric.weight * 100).toFixed(0)}%
          </span>
        </div>
        <div className="col-span-2">
          <span className="text-muted-foreground">Effective Score:</span>
          <span className="ml-2 font-medium">
            {metric.effective_score.toFixed(1)}
          </span>
        </div>
      </div>

      {metric.info.length > 0 && (
        <div className="space-y-1">
          <div className="text-xs font-medium text-muted-foreground">Info:</div>
          <ul className="text-xs space-y-1">
            {metric.info.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-gray-600 mt-0.5">!</span>
                <span className="flex-1">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {metric.evidence.length > 0 && (
        <div className="space-y-1">
          <div className="text-xs font-medium text-muted-foreground">
            Evidence:
          </div>
          <ul className="text-xs space-y-1">
            {metric.evidence.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-green-600 mt-0.5">✓</span>
                <span className="flex-1">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {metric.failures.length > 0 && (
        <div className="space-y-1">
          <div className="text-xs font-medium text-muted-foreground">
            Failures:
          </div>
          <ul className="text-xs space-y-1">
            {metric.failures.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-red-600 mt-0.5">✗</span>
                <span className="flex-1">{item}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );

  return (
    <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 hover:bg-muted rounded transition-colors"
            aria-label={isExpanded ? "Collapse details" : "Expand details"}
          >
            {isExpanded ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </button>
          <h3 className="text-lg font-semibold">Detailed Evaluation Metrics</h3>
          <a
            href={`https://ipfs.io/ipfs/${detailsCID}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-foreground transition-colors"
            title="View on IPFS"
          >
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>
        <HumanAttestationDialog
          attestationUID={attestationUID}
          agentName={agentName}
          onSuccess={onVerificationSuccess}
        />
      </div>

      {/* Expandable Content */}
      {isExpanded && (
        <div className="space-y-4">
          {isLoading ? (
            <div className="text-sm text-muted-foreground text-center py-8">
              Loading detailed metrics...
            </div>
          ) : details ? (
            <>
              <div className="text-xs text-muted-foreground space-y-1 pb-2 border-b border-border">
                <div>
                  <span>Evaluator:</span>
                  <span className="ml-2 font-mono">{details.evaluatorAgentAddress}</span>
                </div>
                <div>
                  <span>Evaluated:</span>
                  <span className="ml-2">
                    {new Date(details.timestamp).toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="space-y-3">
                <MetricDetails
                  name="Correctness"
                  metric={details.metrics.correctness}
                />
                <MetricDetails
                  name="Capabilities"
                  metric={details.metrics.capabilities}
                />
                <MetricDetails name="Domain" metric={details.metrics.domain} />
              </div>
            </>
          ) : (
            <div className="text-sm text-muted-foreground text-center py-8">
              No detailed metrics available
            </div>
          )}
        </div>
      )}
    </div>
  );
}
