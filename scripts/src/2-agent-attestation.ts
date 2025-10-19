import { ethers } from "ethers";
import { EvaluationScore } from "./type";
import { encodeAttestationData, envSetup } from "./utils";
import { EAS_INTERFACE } from "./abis";

import {
  EAS,
  SchemaEncoder,
  Transaction,
} from "@ethereum-attestation-service/eas-sdk";
import { encodingSchema } from "./type";

/**
 * Bot Attestion functionality
 * prerequisites:
 *  - access to pk. cannot use viem ("RPC wallet") -> AGENT INITIAL ATTESTATION OF SCORE
 * agent calculates and attest to initial score, humans can verify later with a different attestation schema
 * requirements:
 *  - attestation schema must have resolver contract assigned
 *      -> resolver contract must check signature against allowed evaluator list before attestion allowed?
 *  - implemented resolver contract with basic whitelisting
 *
 */
const AGENT_ATTESTATION_SCHEMA_UID =
  "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";
const EAS_CONTRACT_ADDRESS = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET

export async function attestAgentEvaluation(
  evaluationScore: EvaluationScore,
  evaluatedAgentWalletAddress: string
) {
  const { url, pk } = envSetup();

  if (!pk || !url) throw new Error(".env error");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);

  let recipient;
  if (
    evaluatedAgentWalletAddress === ethers.ZeroAddress ||
    evaluatedAgentWalletAddress.trim() === "" ||
    evaluatedAgentWalletAddress === "0x"
  ) {
    recipient = ethers.ZeroAddress;
  } else {
    recipient = evaluatedAgentWalletAddress;
  }

  // ENCODE THE EVALUATION SCORE IN THE ATTESTATION TUPLE
  const encodedData = encodeAttestationData(evaluationScore);

  // ABI TUPLE
  const attestationTuple = {
    schema: AGENT_ATTESTATION_SCHEMA_UID,
    data: {
      recipient: recipient, //Change for a schema field?
      expirationTime: 0,
      revocable: false,
      refUID: ethers.ZeroHash,
      data: encodedData,
      value: 0,
    },
  };

  // ENCODE THE TRANSACTION CALLDATA WITH FUNCTION SELECTOR
  const callData = encodeAttestTxCallData(attestationTuple);

  console.log("Submitting attestation to EAS contract...");
  console.log("Schema:", AGENT_ATTESTATION_SCHEMA_UID);
  console.log("Recipient:", recipient);
  console.log("Attester:", signer.address);

  // CREATE TRANSACTION
  const txRequest: ethers.TransactionRequest = {
    to: EAS_CONTRACT_ADDRESS,
    data: callData,
    from: signer.address,
  };

  try {
    await signer.call(txRequest);
    console.log("call passed");
  } catch (error) {
    console.log("call failed");
    console.log(error);
  }

  const tx = await signer.sendTransaction(txRequest);

  console.log("Transaction sent:", tx.hash);

  const receipt = await tx.wait();

  console.log("Attestation confirmed in block:", receipt?.blockNumber);

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
      console.log("Attestation UID:", attestedEvent.args.uid);
      console.log("Attester:", attestedEvent.args.attester);
      console.log("Recipient:", attestedEvent.args.recipient);
    }
  }

  return receipt;
}

function encodeAttestTxCallData(attestationRequest: any) {
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

  //functionSelector + encodedParams.slice(2); // Remove '0x' from encoded params
  const callData = ethers.concat([functionSelector, encodedParams]);

  return callData;
}

export async function attestAgentEvaluationSDK(
  evaluatedAgentWalletAddress: string,
  evaluationScore?: EvaluationScore
) {
  const { url, pk } = envSetup();

  const eas = new EAS(EAS_CONTRACT_ADDRESS);
  const easContract = new ethers.Contract(EAS_CONTRACT_ADDRESS, EAS_INTERFACE);

  if (!pk || !url) throw new Error(".env error");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);
  await eas.connect(signer);
  const schemaEncoder = new SchemaEncoder(encodingSchema);
  // Use the evaluationScore object to encode data for the attestation
  let encodedData;

  if (evaluationScore) {
    encodedData = schemaEncoder.encodeData([
      {
        name: "evaluatedAgentAddress",
        value: evaluationScore.evaluatedAgentAddress,
        type: "string",
      },
      {
        name: "evaluatorAgentAddress",
        value: evaluationScore.evaluatorAgentAddress,
        type: "string",
      },
      {
        name: "timestamp",
        value: evaluationScore.timestamp.toString(),
        type: "uint256",
      },
      {
        name: "finalScore",
        value: evaluationScore.finalScore.toString(),
        type: "uint256",
      },
      {
        name: "overallConfidence",
        value: evaluationScore.overallConfidence,
        type: "uint8",
      },
      { name: "grade", value: evaluationScore.grade, type: "string" },
      {
        name: "correctnessScore",
        value: evaluationScore.correctnessScore.toString(),
        type: "uint256",
      },
      {
        name: "correctnessConfidence",
        value: evaluationScore.correctnessConfidence,
        type: "uint8",
      },
      {
        name: "correctnessEffectiveScore",
        value: evaluationScore.correctnessEffectiveScore.toString(),
        type: "uint256",
      },
      {
        name: "correctnessWeight",
        value: evaluationScore.correctnessWeight,
        type: "uint8",
      },
      {
        name: "capabilitiesScore",
        value: evaluationScore.capabilitiesScore.toString(),
        type: "uint256",
      },
      {
        name: "capabilitiesConfidence",
        value: evaluationScore.capabilitiesConfidence,
        type: "uint8",
      },
      {
        name: "capabilitiesEffectiveScore",
        value: evaluationScore.capabilitiesEffectiveScore.toString(),
        type: "uint256",
      },
      {
        name: "capabilitiesWeight",
        value: evaluationScore.capabilitiesWeight,
        type: "uint8",
      },
      {
        name: "domainScore",
        value: evaluationScore.domainScore.toString(),
        type: "uint256",
      },
      {
        name: "domainConfidence",
        value: evaluationScore.domainConfidence,
        type: "uint8",
      },
      {
        name: "domainEffectiveScore",
        value: evaluationScore.domainEffectiveScore.toString(),
        type: "uint256",
      },
      {
        name: "domainWeight",
        value: evaluationScore.domainWeight,
        type: "uint8",
      },
      { name: "detailsCID", value: evaluationScore.detailsCID, type: "string" },
    ]);
  } else {
    encodedData = schemaEncoder.encodeData([
      {
        name: "evaluatedAgentAddress",
        value:
          "agent1qdpyzp043kf7h6yhygnfz79tljchzjcsvz626uty4s9xyhcrhas2zsr0hrs",
        type: "string",
      },
      {
        name: "evaluatorAgentAddress",
        value:
          "agent1qw254tc8q3mcmrseem0pmhu2jd0j7urn2e9cd5tgcg88kmy9wkqhysksdwf",
        type: "string",
      },
      {
        name: "timestamp",
        value: Math.floor(Date.now() / 1000).toString(),
        type: "uint256",
      },
      { name: "finalScore", value: "85", type: "uint256" },
      { name: "overallConfidence", value: 8, type: "uint8" },
      { name: "grade", value: "B+", type: "string" },
      { name: "correctnessScore", value: "90", type: "uint256" },
      { name: "correctnessConfidence", value: 9, type: "uint8" },
      { name: "correctnessEffectiveScore", value: "81", type: "uint256" },
      { name: "correctnessWeight", value: 30, type: "uint8" },
      { name: "capabilitiesScore", value: "80", type: "uint256" },
      { name: "capabilitiesConfidence", value: 7, type: "uint8" },
      { name: "capabilitiesEffectiveScore", value: "56", type: "uint256" },
      { name: "capabilitiesWeight", value: 35, type: "uint8" },
      { name: "domainScore", value: "85", type: "uint256" },
      { name: "domainConfidence", value: 8, type: "uint8" },
      { name: "domainEffectiveScore", value: "68", type: "uint256" },
      { name: "domainWeight", value: 35, type: "uint8" },
      { name: "detailsCID", value: "QmExampleCID123456789", type: "string" },
    ]);
  }

  let recipient;
  if (
    evaluatedAgentWalletAddress === ethers.ZeroAddress ||
    evaluatedAgentWalletAddress.trim() == ""
  ) {
    recipient = ethers.ZeroAddress;
  } else {
    //validation with regex eth address format
    recipient = evaluatedAgentWalletAddress;
  }

  const tx: Transaction<string> = await eas.attest({
    schema: AGENT_ATTESTATION_SCHEMA_UID,
    data: {
      recipient: recipient, //WEB3 Identity?
      expirationTime: 0n,
      revocable: false,
      data: encodedData,
    },
  });
  console.log(tx);
  await tx.wait();
  console.log("Attestation validated");
}

if (require.main === module) {
  const agentWalletAddress = ethers.ZeroAddress;
  attestAgentEvaluationSDK(agentWalletAddress).catch(console.error);
}
