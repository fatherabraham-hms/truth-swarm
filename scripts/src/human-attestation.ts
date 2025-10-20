import { ethers } from "ethers";
import { envSetup } from "./utils";
import { EAS_INTERFACE } from "./abis";

/**
 * Human Attestation functionality -> EOA attestation to verify agent evaluation
 * prerequisites:
 *  - access to pk (EOA wallet)
 *  - original attestation UID from agent evaluation
 *
 * Human verifiers attest to the accuracy of agent evaluations
 */

const HUMAN_ATTESTATION_SCHEMA_UID =
  "0x35bf5bfce7eaa219f46c086d4d60bfe96affaa42a0d2ae1abf17057e6607007d";
const EAS_CONTRACT_ADDRESS = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET

export interface HumanVerificationData {
  originalAttestationUID: string; // bytes32
  verifier: string; // address
  timestamp: number; // uint64
  approved: boolean; // bool
  comment: string; // string
}

/**
 * Encode human verification data according to the human attestation schema
 * Schema: (bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment)
 */
function encodeHumanVerificationData(data: HumanVerificationData): string {
  const abiCoder = ethers.AbiCoder.defaultAbiCoder();

  return abiCoder.encode(
    ["bytes32", "address", "uint64", "bool", "string"],
    [
      data.originalAttestationUID,
      data.verifier,
      data.timestamp,
      data.approved,
      data.comment,
    ]
  );
}

/**
 * Attest to a human verification of an agent evaluation
 * @param originalAttestationUID - The UID of the original agent evaluation attestation
 * @param approved - Whether the human verifier approves the evaluation
 * @param comment - Optional comment explaining the verification decision
 */
export async function attestHumanVerification(
  originalAttestationUID: string,
  approved: boolean,
  comment: string = ""
) {
  const { url, pk } = envSetup();

  if (!pk || !url) throw new Error(".env error");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);

  // Create verification data
  const verificationData: HumanVerificationData = {
    originalAttestationUID,
    verifier: signer.address,
    timestamp: Math.floor(Date.now() / 1000),
    approved,
    comment,
  };

  const encodedData = encodeHumanVerificationData(verificationData);

  const attestationRequest = {
    schema: HUMAN_ATTESTATION_SCHEMA_UID,
    data: {
      recipient: ethers.ZeroAddress, // Human attestations don't need a recipient
      expirationTime: 0,
      revocable: false,
      refUID: ethers.ZeroHash,
      data: encodedData,
      value: 0,
    },
  };

  const attestFunction = EAS_INTERFACE.getFunction("attest");
  if (!attestFunction) {
    throw new Error("attest function not found in ABI");
  }
  const functionSelector = attestFunction.selector;

  const abiCoder = ethers.AbiCoder.defaultAbiCoder();
  const encodedParams = abiCoder.encode(
    [
      "tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value) data)",
    ],
    [attestationRequest]
  );

  const callData = ethers.concat([functionSelector, encodedParams]);

  console.log("Submitting human verification attestation to EAS contract...");
  console.log("Schema:", HUMAN_ATTESTATION_SCHEMA_UID);
  console.log("Original Attestation UID:", originalAttestationUID);
  console.log("Verifier:", signer.address);
  console.log("Approved:", approved);
  console.log("Comment:", comment || "(none)");

  const txRequest: ethers.TransactionRequest = {
    to: EAS_CONTRACT_ADDRESS,
    data: callData,
    from: signer.address,
  };

  try {
    await signer.call(txRequest);
    console.log("✓ Dry run passed");
  } catch (error) {
    console.log("✗ Dry run failed");
    console.log(error);
    throw error;
  }

  // Send the transaction
  const tx = await signer.sendTransaction(txRequest);

  console.log("Transaction sent:", tx.hash);

  // Wait for confirmation
  const receipt = await tx.wait();

  console.log("Attestation confirmed in block:", receipt?.blockNumber);

  // Parse the Attested event from the receipt to get the UID
  if (receipt) {
    const attestedEvent = receipt.logs
      .map((log) => {
        try {
          return EAS_INTERFACE.parseLog({
            topics: [...log.topics],
            data: log.data,
          });
        } catch {
          return null;
        }
      })
      .find((event) => event && event.name === "Attested");

    if (attestedEvent) {
      console.log("\n=== Human Verification Attestation Created ===");
      console.log("Attestation UID:", attestedEvent.args.uid);
      console.log("Attester:", attestedEvent.args.attester);
      console.log("Schema:", attestedEvent.args.schema);
      console.log(
        `View on Etherscan: https://sepolia.etherscan.io/tx/${tx.hash}`
      );
      return attestedEvent.args.uid;
    }
  }

  return receipt;
}

// Example usage
if (require.main === module) {
  // Replace with an actual agent evaluation attestation UID
  const originalAttestationUID =
    "0x0000000000000000000000000000000000000000000000000000000000000000";
  const approved = true;
  const comment =
    "Verified the evaluation manually. Agent performed well in tests.";

  attestHumanVerification(originalAttestationUID, approved, comment)
    .then(() => {
      console.log("\n✓ Human verification attestation completed successfully");
    })
    .catch((error) => {
      console.error(
        "\n✗ Error creating human verification attestation:",
        error
      );
    });
}
