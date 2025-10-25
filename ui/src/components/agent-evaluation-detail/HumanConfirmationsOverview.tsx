"use client";

import { HumanConfirmationAttestation } from "@/types/attestation";
import Link from "next/link";
import {
  CheckCircle2,
  XCircle,
  MessageSquare,
  Eye,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { useState } from "react";
import { useTransactionPopup } from "@blockscout/app-sdk";
import { useAccount } from "wagmi";
import { SEPOLIA_CHAIN_ID } from "@/lib/blockscout";
import { Button } from "../ui/button";

interface HumanConfirmationsOverviewProps {
  attestationUID: string;
  humanAttestations: HumanConfirmationAttestation[];
}

const ITEMS_PER_PAGE = 3;

export function HumanConfirmationsOverview({
  attestationUID,
  humanAttestations,
}: HumanConfirmationsOverviewProps) {
  const [currentPage, setCurrentPage] = useState(1);
  const [isExpanded, setIsExpanded] = useState(false);


  const relevantAttestations = humanAttestations.filter(
    (att) => att.humanConfirmation.originalAttestationUID === attestationUID
  );

  const approvedCount = relevantAttestations.filter(
    (att) => att.humanConfirmation.approved
  ).length;
  const rejectedCount = relevantAttestations.length - approvedCount;

  // Calculate pagination
  const totalPages = Math.ceil(relevantAttestations.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const endIndex = startIndex + ITEMS_PER_PAGE;
  const paginatedAttestations = relevantAttestations.slice(
    startIndex,
    endIndex
  );

  if (relevantAttestations.length === 0) {
    return (
      <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-4">
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
          <h3 className="text-lg font-semibold">Human Verifications</h3>
        </div>
        {isExpanded && (
          <div className="text-center py-8">
            <p className="text-muted-foreground">
              No human verifications yet. Be the first to verify this
              evaluation!
            </p>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="p-6 border border-border rounded-lg bg-muted/30 space-y-4">
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
          <h3 className="text-lg font-semibold">Human Verifications</h3>
        </div>
        {isExpanded && (
          <div className="flex gap-3 text-sm">
            <span className="flex items-center gap-1 text-green-600">
              <CheckCircle2 className="h-4 w-4" />
              {approvedCount} Approved
            </span>
            <span className="flex items-center gap-1 text-red-600">
              <XCircle className="h-4 w-4" />
              {rejectedCount} Rejected
            </span>
          </div>
        )}
      </div>

      {isExpanded && (
        <>
          <div className="space-y-3">
            {paginatedAttestations.map((attestation) => {
              const { humanConfirmation } = attestation;
              const hasComment =
                humanConfirmation.comment &&
                humanConfirmation.comment.trim() !== "";

              return (
                <Link
                  key={attestation.uid}
                  href={`/human-confirmation-detail/${attestation.uid}`}
                  className="block"
                >
                  <div className="p-4 border border-border rounded-lg bg-card hover:bg-muted/50 transition-colors cursor-pointer">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 space-y-2">
                        <div className="flex items-center gap-2">
                          {humanConfirmation.approved ? (
                            <CheckCircle2 className="h-5 w-5 text-green-600" />
                          ) : (
                            <XCircle className="h-5 w-5 text-red-600" />
                          )}
                          <span className="font-medium">
                            {humanConfirmation.approved
                              ? "Approved"
                              : "Rejected"}
                          </span>
                          <span className="text-sm text-muted-foreground">
                            by {humanConfirmation.verifier.substring(0, 6)}...
                            {humanConfirmation.verifier.substring(
                              humanConfirmation.verifier.length - 4
                            )}
                          </span>
                        </div>

                        <div className="text-xs text-muted-foreground">
                          {new Date(
                            humanConfirmation.timestamp * 1000
                          ).toLocaleString()}
                        </div>

                        {hasComment && (
                          <div className="flex items-start gap-2 mt-2">
                            <MessageSquare className="h-4 w-4 text-muted-foreground flex-shrink-0 mt-0.5" />
                            <p className="text-sm text-muted-foreground line-clamp-2">
                              {humanConfirmation.comment}
                            </p>
                          </div>
                        )}
                      </div>

                      <Button
                        variant="ghost"
                        size="sm"
                        className="flex-shrink-0 gap-1"
                      >
                        <Eye className="h-4 w-4" />
                        View
                      </Button>
                    </div>

                  </div>
                </Link>
              );
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between pt-2 border-t border-border">
              <div className="text-xs text-muted-foreground">
                Showing {startIndex + 1}-
                {Math.min(endIndex, relevantAttestations.length)} of{" "}
                {relevantAttestations.length} verification
                {relevantAttestations.length !== 1 ? "s" : ""}
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                  className="h-8 w-8 p-0"
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <div className="text-xs text-muted-foreground">
                  Page {currentPage} of {totalPages}
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() =>
                    setCurrentPage((p) => Math.min(totalPages, p + 1))
                  }
                  disabled={currentPage === totalPages}
                  className="h-8 w-8 p-0"
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          )}

          {!totalPages && relevantAttestations.length > 0 && (
            <div className="pt-2 text-xs text-muted-foreground text-center">
              Showing {relevantAttestations.length} verification
              {relevantAttestations.length !== 1 ? "s" : ""}
            </div>
          )}
        </>
      )}
    </div>
  );
}
