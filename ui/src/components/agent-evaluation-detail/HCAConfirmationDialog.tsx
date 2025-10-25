"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  useAccount,
  useWriteContract,
  useWaitForTransactionReceipt,
} from "wagmi";
import { encodeAbiParameters, parseAbiParameters, pad } from "viem";
import {
  EAS_CONTRACT_ADDRESS,
  EAS_ABI,
  HUMAN_ATTESTATION_SCHEMA_UID,
} from "@/lib/constants";
import { CheckCircle2, XCircle, Loader2, Shield } from "lucide-react";
import { useNotification } from "@blockscout/app-sdk";
import { SEPOLIA_CHAIN_ID, getBlockscoutTxUrl } from "@/lib/blockscout";
import { useQueryClient } from "@tanstack/react-query";

interface HumanAttestationDialogProps {
  attestationUID: string;
  agentName: string;
  onSuccess?: () => void;
}

export function HumanAttestationDialog({
  attestationUID,
  agentName,
  onSuccess,
}: HumanAttestationDialogProps) {
  const [open, setOpen] = useState(false);
  const [approved, setApproved] = useState(true);
  const [comment, setComment] = useState("");

  const { address, isConnected } = useAccount();
  const { writeContract, data: hash, isPending, error } = useWriteContract();
  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });
  
  const { openTxToast } = useNotification();
  const queryClient = useQueryClient();

  // Blockscout SDK: Show transaction toast when hash is available
  useEffect(() => {
    if (hash) {
      console.log("📤 Human attestation transaction submitted:", hash);
      openTxToast(SEPOLIA_CHAIN_ID, hash)
        .then(() => {
          console.log("✅ Blockscout toast displayed for human attestation");
        })
        .catch((err) => {
          console.error("Failed to show Blockscout toast:", err);
        });
    }
  }, [hash, openTxToast]);

  // Invalidate queries when transaction is confirmed
  useEffect(() => {
    if (isSuccess && hash) {
      console.log("🎉 Human attestation confirmed on-chain:", hash);
      
      // Delay to allow blockchain to sync with indexers
      setTimeout(() => {
        console.log("🔄 Refreshing attestation data after confirmation...");
        queryClient.invalidateQueries({ queryKey: ["human-attestations"] });
        queryClient.invalidateQueries({ queryKey: ["agent-attestations"] });
      }, 2000);
    }
  }, [isSuccess, hash, queryClient]);

  const handleSubmit = async () => {
    if (!isConnected || !address) {
      alert("Please connect your wallet first");
      return;
    }

    try {
      // Encode the attestation data according to the human schema
      // Schema: bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment
      const timestamp = BigInt(Math.floor(Date.now() / 1000));

      const encodedData = encodeAbiParameters(
        parseAbiParameters(
          "bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment"
        ),
        [attestationUID as `0x${string}`, address, timestamp, approved, comment]
      );

      // Create the attestation request
      const attestationRequest = {
        schema: HUMAN_ATTESTATION_SCHEMA_UID,
        data: {
          recipient:
            "0x0000000000000000000000000000000000000000" as `0x${string}`, // Zero address
          expirationTime: BigInt(0),
          revocable: false,
          refUID: pad("0x0", { size: 32 }) as `0x${string}`,
          data: encodedData,
          value: BigInt(0),
        },
      };

      // Submit the attestation
      writeContract({
        address: EAS_CONTRACT_ADDRESS,
        abi: EAS_ABI,
        functionName: "attest",
        args: [attestationRequest],
      });
    } catch (err) {
      console.error("Error creating attestation:", err);
    }
  };

  // Reset and close dialog on success
  useEffect(() => {
    if (isSuccess && open) {
      const timer = setTimeout(() => {
        setOpen(false);
        setComment("");
        setApproved(true);
        onSuccess?.();
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [isSuccess, open, onSuccess]);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="gap-2" disabled={!isConnected}>
          <Shield className="h-4 w-4" />
          Verify Evaluation
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Human Verification</DialogTitle>
          <DialogDescription>
            Verify the evaluation attestation for {agentName}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Attestation UID Display */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Attestation UID</label>
            <div className="p-3 bg-muted rounded-md">
              <code className="text-xs break-all">{attestationUID}</code>
            </div>
          </div>

          {/* Verifier Address */}
          {isConnected && (
            <div className="space-y-2">
              <label className="text-sm font-medium">Your Address</label>
              <div className="p-3 bg-muted rounded-md">
                <code className="text-xs break-all">{address}</code>
              </div>
            </div>
          )}

          {/* Approval Toggle */}
          <div className="space-y-2">
            <label className="text-sm font-medium">Verification Decision</label>
            <div className="flex gap-2">
              <Button
                type="button"
                variant={approved ? "default" : "outline"}
                className={`flex-1 gap-2 ${
                  approved ? "bg-green-600 hover:bg-green-700" : ""
                }`}
                onClick={() => setApproved(true)}
              >
                <CheckCircle2 className="h-4 w-4" />
                Approve
              </Button>
              <Button
                type="button"
                variant={!approved ? "default" : "outline"}
                className={`flex-1 gap-2 ${
                  !approved ? "bg-red-600 hover:bg-red-700" : ""
                }`}
                onClick={() => setApproved(false)}
              >
                <XCircle className="h-4 w-4" />
                Reject
              </Button>
            </div>
          </div>

          {/* Comment Field */}
          <div className="space-y-2">
            <label className="text-sm font-medium ">
              Comment <span className="text-muted-foreground">(optional)</span>
            </label>
            <Textarea
              placeholder="Add your verification notes or reasoning..."
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              className="min-h-[100px]"
            />
          </div>

          {/* Error Display */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">
                Error: {error.message?.substring(0, 100)}
              </p>
            </div>
          )}

          {/* Success Display */}
          {isSuccess && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-md">
              <p className="text-sm text-green-600 font-medium">
                ✓ Attestation submitted successfully!
              </p>
              {hash && (
                <a
                  href={getBlockscoutTxUrl(hash)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-blue-600 hover:underline break-all"
                >
                  View on Blockscout
                </a>
              )}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            onClick={() => setOpen(false)}
            disabled={isPending || isConfirming}
          >
            Cancel
          </Button>
          <Button
            type="button"
            onClick={handleSubmit}
            disabled={!isConnected || isPending || isConfirming || isSuccess}
            className="gap-2"
          >
            {(isPending || isConfirming) && (
              <Loader2 className="h-4 w-4 animate-spin" />
            )}
            {isPending
              ? "Waiting for signature..."
              : isConfirming
              ? "Confirming..."
              : isSuccess
              ? "Submitted!"
              : "Submit Verification"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
