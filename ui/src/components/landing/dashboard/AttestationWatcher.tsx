"use client";

import { useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useWatchContractEvent } from "wagmi";
import { useNotification } from "@blockscout/app-sdk";
import { EAS_CONTRACT_ADDRESS, EAS_ABI } from "@/lib/constants";
import { SEPOLIA_CHAIN_ID } from "@/lib/blockscout";

interface EventLog {
  transactionHash: string;
  logIndex: number;
}

/**
 * AttestationWatcher integrates Blockscout SDK with EAS contract event monitoring.
 * 
 * Features:
 * - Listens to EAS "Attested" events in real-time
 * - Shows Blockscout transaction toast notifications for new attestations
 * - Auto-refreshes attestation queries when new events are detected
 * - Prevents duplicate event processing
 * 
 * This showcases Blockscout SDK's transaction notification feature with
 * real-time blockchain event monitoring for a seamless UX.
 */
export function AttestationWatcher() {
  const queryClient = useQueryClient();
  const { openTxToast } = useNotification();
  const lastEventRef = useRef<string | null>(null);
  const processingRef = useRef<Set<string>>(new Set());

  // Listen for Attested events on EAS contract
  useWatchContractEvent({
    address: EAS_CONTRACT_ADDRESS,
    abi: EAS_ABI,
    eventName: "Attested",
    onLogs(logs) {
      if (!logs || logs.length === 0) return;
      
      logs.forEach((log: EventLog) => {
        const eventId = `${log.transactionHash}-${log.logIndex}`;
        
        // Avoid processing the same event twice
        if (lastEventRef.current === eventId || processingRef.current.has(eventId)) {
          return;
        }
        
        lastEventRef.current = eventId;
        processingRef.current.add(eventId);

        console.log("🔔 New attestation detected:", {
          txHash: log.transactionHash,
          eventId,
        });
        
        // Show Blockscout transaction toast notification
        // This provides real-time feedback with transaction status tracking
        openTxToast(SEPOLIA_CHAIN_ID, log.transactionHash)
          .then(() => {
            console.log("✅ Blockscout toast shown for attestation");
            
            // Invalidate queries after toast is shown and blockchain has synced
            // This ensures the UI updates with the new attestation data
            setTimeout(() => {
              console.log("🔄 Refreshing attestation data...");
              queryClient.invalidateQueries({ queryKey: ["agent-attestations"] });
              queryClient.invalidateQueries({ queryKey: ["human-attestations"] });
              
              // Clean up processed event after refresh
              setTimeout(() => {
                processingRef.current.delete(eventId);
              }, 5000);
            }, 2000);
          })
          .catch((error) => {
            console.error("Failed to show Blockscout toast:", error);
            // Still refresh data even if toast fails
            setTimeout(() => {
              queryClient.invalidateQueries({ queryKey: ["agent-attestations"] });
              queryClient.invalidateQueries({ queryKey: ["human-attestations"] });
              processingRef.current.delete(eventId);
            }, 2000);
          });
      });
    },
  });

  return null;
}



