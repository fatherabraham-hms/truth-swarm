"use client";

import { NotificationProvider, TransactionPopupProvider } from "@blockscout/app-sdk";

/**
 * BlockscoutContext provides Blockscout SDK providers for the entire application.
 * 
 * Features:
 * - NotificationProvider: Enables transaction toast notifications
 * - TransactionPopupProvider: Enables transaction history popup
 * 
 * Note: Event listening and query invalidation are handled in Dashboard.tsx
 * to better integrate with Blockscout SDK features.
 */
export function BlockscoutContext({ children }: { children: React.ReactNode }) {
  return (
    <NotificationProvider>
      <TransactionPopupProvider>
        {children}
      </TransactionPopupProvider>
    </NotificationProvider>
  );
}

