import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { toast } from "sonner";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function splitAddress(tokenAddress: string) {
  const firstFive = tokenAddress.substring(0, 5);
  const lastSix = tokenAddress.substring(tokenAddress.length - 6);

  return `${firstFive}...${lastSix}`;
}

export const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
    toast.success("Address copied to clipboard!");
  } catch (err) {
    toast.error("Failed to copy address", {
      description: err instanceof Error ? err.message : "An unknown error occurred"
    });
  }
};

export const parseNum = (v: string | number | null | undefined): number => {
  if (v === null || v === undefined || v === "") return 0;
  const n = Number(v);
  return isNaN(n) ? 0 : n;
};

export const formatLargeNumber = (value: number): string => {
  if (value >= 1_000_000_000) {
    const billions = value / 1_000_000_000;
    return billions % 1 === 0 ? `${billions}B` : `${billions.toFixed(1)}B`;
  } else if (value >= 1_000_000) {
    const millions = value / 1_000_000;
    return millions % 1 === 0 ? `${millions}M` : `${millions.toFixed(1)}M`;
  } else if (value >= 1_000) {
    const thousands = value / 1_000;
    return thousands % 1 === 0 ? `${thousands}K` : `${thousands.toFixed(1)}K`;
  } else {
    return value.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }
};
