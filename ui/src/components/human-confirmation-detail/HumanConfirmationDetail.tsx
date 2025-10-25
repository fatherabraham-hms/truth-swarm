"use client";

import {
  useHumanAttestations,
  useAgentAttestations,
} from "@/hooks/useAttestation";
import { useEffect, useState } from "react";
import Link from "next/link";
import {
  CheckCircle2,
  XCircle,
  MessageSquare,
  Calendar,
  User,
  ExternalLink,
} from "lucide-react";
import { AgentEvaluationAttestation, HumanConfirmationAttestation } from "@/types/attestation";

interface HumanConfirmationDetailProps {
  uid: string;
}

export function HumanConfirmationDetail({ uid }: HumanConfirmationDetailProps) {
  const humanAttestationsQuery = useHumanAttestations();
  const agentAttestationsQuery = useAgentAttestations();

  const [attestation, setAttestation] = useState<HumanConfirmationAttestation | null>(null);
  const [originalAttestation, setOriginalAttestation] =
    useState<AgentEvaluationAttestation | null>(null);

  useEffect(() => {
    if (humanAttestationsQuery.data) {
      const found = humanAttestationsQuery.data.find((att) => att.uid === uid);
      if (found) {
        setAttestation(found);

        // Find the original agent attestation
        if (agentAttestationsQuery.data) {
          const original = agentAttestationsQuery.data.find(
            (agentAtt) =>
              agentAtt.uid === found.humanConfirmation.originalAttestationUID
          );
          setOriginalAttestation(original || null);
        }
      }
    }
  }, [uid, humanAttestationsQuery.data, agentAttestationsQuery.data]);

  const isLoading =
    humanAttestationsQuery.isLoading || agentAttestationsQuery.isLoading;

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="flex items-center justify-center py-12">
          <div className="text-muted-foreground">
            Loading attestation details...
          </div>
        </div>
      </div>
    );
  }

  if (!attestation) {
    return (
      <div className="max-w-4xl mx-auto p-8">
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="text-xl font-semibold">Attestation not found</div>
          <p className="text-muted-foreground">
            No human verification found with this UID.
          </p>
          <Link
            href="/"
            className="text-sm text-blue-600 hover:text-blue-700 underline"
          >
            ← Back to agents list
          </Link>
        </div>
      </div>
    );
  }

  const { humanConfirmation } = attestation;
  const hasComment =
    humanConfirmation.comment && humanConfirmation.comment.trim() !== "";

  return (
    <div className="max-w-4xl mx-auto p-8 space-y-6">
      {/* Back Button */}
      <Link
        href="/"
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <span className="mr-2">←</span>
        Back to agents list
      </Link>

      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Human Verification Details</h1>
        <p className="text-muted-foreground">
          View detailed information about this human verification attestation
        </p>
      </div>

      {/* Verification Decision Card */}
      <div className="p-6 border border-border rounded-lg bg-card">
        <div className="flex items-start gap-4">
          <div
            className={`p-3 rounded-full ${
              humanConfirmation.approved ? "bg-green-100" : "bg-red-100"
            }`}
          >
            {humanConfirmation.approved ? (
              <CheckCircle2 className="h-8 w-8 text-green-600" />
            ) : (
              <XCircle className="h-8 w-8 text-red-600" />
            )}
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-semibold mb-2">
              {humanConfirmation.approved ? "Approved" : "Rejected"}
            </h2>
            <p className="text-muted-foreground">
              This evaluation was{" "}
              {humanConfirmation.approved ? "approved" : "rejected"} by a human
              verifier
            </p>
          </div>
        </div>
      </div>

      {/* Comment Section */}
      {hasComment && (
        <div className="p-6 border border-border rounded-lg bg-muted/30">
          <div className="flex items-start gap-3">
            <MessageSquare className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold mb-2">Verifier Comment</h3>
              <p className="text-muted-foreground whitespace-pre-wrap">
                {humanConfirmation.comment}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Verification Details */}
      <div className="p-6 border border-border rounded-lg bg-card space-y-4">
        <h3 className="text-lg font-semibold">Verification Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start gap-3">
            <User className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-sm text-muted-foreground mb-1">
                Verifier Address
              </div>
              <a
                href={`https://sepolia.etherscan.io/address/${humanConfirmation.verifier}`}
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-sm text-blue-600 hover:text-blue-700 underline break-all"
              >
                {humanConfirmation.verifier}
              </a>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Calendar className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-sm text-muted-foreground mb-1">
                Verification Date
              </div>
              <div className="text-sm">
                {new Date(humanConfirmation.timestamp * 1000).toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Attestation Metadata */}
      <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-4">
        <h3 className="text-lg font-semibold">Attestation Metadata</h3>
        <div className="space-y-3 text-sm">
          <div>
            <span className="text-muted-foreground">Attestation UID:</span>
            <div className="font-mono text-xs mt-1 break-all">
              {attestation.uid}
            </div>
          </div>

          <div>
            <span className="text-muted-foreground">
              Original Evaluation UID:
            </span>
            <div className="flex items-center gap-2 mt-1">
              <code className="font-mono text-xs break-all flex-1">
                {humanConfirmation.originalAttestationUID}
              </code>
            </div>
          </div>

          <div>
            <span className="text-muted-foreground">
              Attester (Transaction Sender):
            </span>
            <a
              href={`https://sepolia.etherscan.io/address/${attestation.attester}`}
              target="_blank"
              rel="noopener noreferrer"
              className="font-mono text-xs mt-1 text-blue-600 hover:text-blue-700 underline block break-all"
            >
              {attestation.attester}
            </a>
          </div>

          <div>
            <span className="text-muted-foreground">View Attestation:</span>
            <a
              href={`https://sepolia.easscan.org/attestation/view/${attestation.uid}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-700 underline text-xs mt-1 flex items-center gap-1"
            >
              View on EAS Scan
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>
      </div>

      {/* Original Evaluation Preview */}
      {originalAttestation && (
        <div className="p-6 border border-border rounded-lg bg-card">
          <h3 className="text-lg font-semibold mb-4">
            Original Evaluation Preview
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-muted-foreground">Final Score</div>
              <div className="text-2xl font-bold">
                {originalAttestation.evaluationScore.finalScore.toFixed(1)}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Grade</div>
              <div className="text-2xl font-bold">
                {originalAttestation.evaluationScore.grade}
              </div>
            </div>
            <div>
              <div className="text-sm text-muted-foreground">Confidence</div>
              <div className="text-2xl font-bold">
                {originalAttestation.evaluationScore.overallConfidence.toFixed(
                  1
                )}
                %
              </div>
            </div>
            <div>
              <Link
                href={`/agents/${originalAttestation.evaluationScore.evaluatedAgentAddress}`}
                className="inline-flex items-center justify-center h-full px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 border border-blue-600 rounded-md hover:bg-blue-50 transition-colors"
              >
                View Full Evaluation
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
