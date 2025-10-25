"use client";

import { AgentEvaluationAttestation } from "@/types/attestation";
import { useEffect, useState } from "react";
import Link from "next/link";
import {
  useAgentAttestations,
  useHumanAttestations,
} from "@/hooks/useAttestation";
import { fetchAgentverseInfo } from "@/actions/agentverse";
import { AgentVerseInfo } from "@/types/agents";
import { HumanConfirmationsOverview } from "./HumanConfirmationsOverview";
import { EvaluationDetailsOverview } from "./EvaluationDetailsOverview";


interface AgentEvaluationDetailProps {
  address: string;
}

export function AgentEvaluationDetail({
  address,
}: AgentEvaluationDetailProps) {
  const agentAttestationsQuery = useAgentAttestations();
  const humanAttestationsQuery = useHumanAttestations();


  const [agentInfo, setAgentInfo] = useState<AgentVerseInfo | null>(null);
  const [attestation, setAttestation] = useState<AgentEvaluationAttestation | null>(null);
  const [humanVerificationCount, setHumanVerificationCount] = useState(0);
  const [isLoadingAgentInfo, setIsLoadingAgentInfo] = useState(true);

  useEffect(() => {
    if (agentAttestationsQuery.data && humanAttestationsQuery.data) {
      const agentAttestation = agentAttestationsQuery.data.find(
        (att) => att.evaluationScore.evaluatedAgentAddress === address
      );

      if (agentAttestation) {
        setAttestation(agentAttestation);

        // Count human verifications for this attestation
        const verifications = humanAttestationsQuery.data.filter(
          (humanAtt) =>
            humanAtt.humanConfirmation.originalAttestationUID ===
              agentAttestation.uid && humanAtt.humanConfirmation.approved
        ).length;
        setHumanVerificationCount(verifications);

        fetchAgentverseInfo(address).then((info) => {
          if (info) {
            setAgentInfo({
              ...info,
            });
          }
          setIsLoadingAgentInfo(false);
        });
      } else {
        setIsLoadingAgentInfo(false);
      }
    }
  }, [address, agentAttestationsQuery.data, humanAttestationsQuery.data]);

  const isLoading =
    agentAttestationsQuery.isLoading ||
    humanAttestationsQuery.isLoading ||
    isLoadingAgentInfo;

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex items-center justify-center py-12">
          <div className="text-muted-foreground">Loading agent details...</div>
        </div>
      </div>
    );
  }

  if (!attestation) {
    return (
      <div className="max-w-6xl mx-auto p-8">
        <div className="flex flex-col items-center justify-center py-12 space-y-4">
          <div className="text-xl font-semibold">Agent not found</div>
          <p className="text-muted-foreground">
            No evaluation data found for this agent address.
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

  const evalScore = attestation.evaluationScore;

  const agentName = agentInfo?.name || "Unknown Agent";
  const isHumanVerified = humanVerificationCount >= 3;

  return (
    <div className="max-w-6xl mx-auto p-8 space-y-8">
      {/* Back Button */}
      <Link
        href="/"
        className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <span className="mr-2">←</span>
        Back to agents list
      </Link>

      {/* Header Section */}
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <h1 className="text-3xl font-bold">{agentName}</h1>
          {isHumanVerified && (
            <span className="px-3 py-1 text-xs font-semibold bg-green-100 text-green-800 rounded-full">
              Human Verified ({humanVerificationCount})
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          <a
            href={`https://agentverse.ai/agents/details/${address}/profile`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground font-mono text-sm break-all hover:text-blue-600 transition-colors hover:underline"
          >
            {address}
          </a>
          {agentInfo?.status && (
            <div
              className={`h-2 w-2 rounded-full ${
                agentInfo.status === "active" ? "bg-green-500" : "bg-red-500"
              }`}
              title={`Status: ${agentInfo.status}`}
            />
          )}
          {agentInfo?.rating && agentInfo.rating > 0 && (
            <span className="text-xs text-muted-foreground">
              ({agentInfo.rating}/5)
            </span>
          )}
        </div>

        {agentInfo?.description && (
          <p className="text-muted-foreground mt-2">{agentInfo.description}</p>
        )}
      </div>

      {/* Overall Score Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">Final Score</div>
          <div className="text-4xl font-bold">
            {evalScore.finalScore.toFixed(1)}
          </div>
          <div className="text-sm text-muted-foreground mt-1">out of 100</div>
        </div>

        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">Grade</div>
          <div className="text-4xl font-bold">{evalScore.grade}</div>
        </div>

        <div className="p-6 border border-border rounded-lg bg-card">
          <div className="text-sm text-muted-foreground mb-2">
            Overall Confidence
          </div>
          <div className="text-4xl font-bold">
            {evalScore.overallConfidence.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Metadata */}
      <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-2">
        <h3 className="text-lg font-semibold mb-4">Evaluation Metadata</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-muted-foreground">Evaluator:</span>
            <a
              href={`https://agentverse.ai/agents/details/${evalScore.evaluatorAgentAddress}/profile`}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 font-mono text-blue-600 hover:text-blue-700 underline"
            >
              {evalScore.evaluatorAgentAddress.substring(0, 20)}...
            </a>
          </div>
          <div>
            <span className="text-muted-foreground">Timestamp:</span>
            <span className="ml-2">
              {new Date(evalScore.timestamp * 1000).toLocaleString()}
            </span>
          </div>
          <div>
            <span className="text-muted-foreground">Details CID:</span>
            <a
              href={`https://ipfs.io/ipfs/${evalScore.detailsCID}`}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 font-mono text-blue-600 hover:text-blue-700 underline text-xs"
            >
              {evalScore.detailsCID.substring(0, 20)}...
            </a>
          </div>
          <div>
            <span className="text-muted-foreground">Attestation UID:</span>
            <span className="ml-2 font-mono text-xs break-all">
              {attestation.uid}
            </span>
          </div>
        </div>
      </div>

      {/* Human Verifications Section */}
      {humanAttestationsQuery.data && (
        <>
          <HumanConfirmationsOverview
            attestationUID={attestation.uid}
            humanAttestations={humanAttestationsQuery.data}
          />


        </>
      )}

      {/* Detailed Evaluation Metrics Card */}
      <EvaluationDetailsOverview
        detailsCID={evalScore.detailsCID}
        attestationUID={attestation.uid}
        agentName={agentName}
        onVerificationSuccess={() => {
          window.location.reload();
        }}
      />
    </div>
  );
}
