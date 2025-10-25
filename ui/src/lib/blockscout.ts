/**
 * Blockscout SDK helpers
 */

export const SEPOLIA_CHAIN_ID = "11155111";

export const BLOCKSCOUT_BASE_URL = "https://eth-sepolia.blockscout.com";

export function getBlockscoutTxUrl(txHash: string): string {
  return `${BLOCKSCOUT_BASE_URL}/tx/${txHash}`;
}

export function getBlockscoutAddressUrl(address: string): string {
  return `${BLOCKSCOUT_BASE_URL}/address/${address}`;
}


