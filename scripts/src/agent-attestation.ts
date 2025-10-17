import * as path from "path";
import { configDotenv } from "dotenv";
import {
  EAS,
  SchemaEncoder,
  Transaction,
} from "@ethereum-attestation-service/eas-sdk";
import { ethers } from "ethers";
import { encodingSchema, EvaluationScore } from "./type";

// Configure dotenv to load .env file from the scripts directory
// Try multiple possible paths to find the .env file
const possiblePaths = [
  path.resolve(process.cwd(), "scripts", ".env"), // From truth-swarm root
  path.resolve(process.cwd(), ".env"), // From scripts directory
  path.resolve(__dirname, "../.env"), // Relative to compiled JS
];

let envPath = possiblePaths.find((p) => {
  try {
    require("fs").accessSync(p);
    return true;
  } catch {
    return false;
  }
});

if (!envPath) {
  envPath = possiblePaths[0]; // fallback to first option
}

console.log("Loading .env from:", envPath);
configDotenv({
  path: envPath!,
});

/**
 * Bot Attestion functionality -> port to python uAgent implementation
 * prerequisites:
 *  - access to pk. cannot use viem ("RPC wallet") -> BOT INITIAL SCORE
 * agent calculates and attest to initial score, humans can verify later with a different attestation schema
 * requirements:
 *  - attestation schema must have resolver contract assigned
 *      -> resolver contract must check signature against allowed evaluator list before attestion allowed?
 *
 */

// RANDOM EXAMPLE

export async function attestAgentEvaluation(evaluationScore?: EvaluationScore) {
  // VALIDATE PK ADDRESS WITH RESOLVER CONTRACT, ADD VALIDATION LOGIC?
  const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET
  const schemaUID =
    "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";

  const eas = new EAS(easContractAddress);

  const url = process.env.SEPOLIA_RPC!;
  const pk = process.env.DT_KEY!;

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

  const tx: Transaction<string> = await eas.attest({
    schema: schemaUID,
    data: {
      recipient: "0x0000000000000000000000000000000000000000", //WEB3 Identity?
      expirationTime: 0n,
      revocable: false,
      data: encodedData,
    },
  });
  console.log(tx);
  await tx.wait();
  console.log("Attestation validated");
}

async function getAttestation() {
  const uid =
    "0x1e903e1eaa9d7b7f064b7f816b91a08f2d4c67afb712527f80c81e9adbcb18a3";

  // use EAS sdk
  const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e";
  const eas = new EAS(easContractAddress);

  const url = process.env.SEPOLIA_RPC;
  const provider = new ethers.JsonRpcProvider(url);

  eas.connect(provider);

  const attestation = await eas.getAttestation(uid);

  console.log(attestation);

  // use graphQL
}

if (require.main === module) {
  attestAgentEvaluation().catch(console.error);
}
