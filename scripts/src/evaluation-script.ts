import * as path from "path";
import { configDotenv } from "dotenv";

import { EvaluationScore } from "./type";
import { attestAgentEvaluation } from "./agent-attestation";

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

const url = process.env.SEPOLIA_RPC;
const pk = process.env.DT_KEY;

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

async function runEvaluation() {
  if (!pk || !url) throw new Error("ENV error");

  const agentToEvaluate =
    "agent1qdpyzp043kf7h6yhygnfz79tljchzjcsvz626uty4s9xyhcrhas2zsr0hrs";

  const { evaluationScore, details } = await evaluateAgent(agentToEvaluate);

  const ipfsCID = await storeEvaluationIPFS(details);

  evaluationScore.detailsCID = ipfsCID;

  await attestAgentEvaluation(evaluationScore);
}

async function evaluateAgent(address: string) {
  console.log(`Evaluating Agent ${address}... `);
  const agentWalletAddress = "0x";

  const evaluatorAddress =
    "agent1qw254tc8q3mcmrseem0pmhu2jd0j7urn2e9cd5tgcg88kmy9wkqhysksdwf";

  const evaluationScore: EvaluationScore = {
    evaluatedAgentAddress: address,
    evaluatorAgentAddress: evaluatorAddress,
    timestamp: Math.floor(Date.now() / 1000),
    finalScore: 85,
    overallConfidence: 8,
    grade: "B+",
    correctnessScore: 90,
    correctnessConfidence: 9,
    correctnessEffectiveScore: 81,
    correctnessWeight: 30,
    capabilitiesScore: 80,
    capabilitiesConfidence: 7,
    capabilitiesEffectiveScore: 56,
    capabilitiesWeight: 35,
    domainScore: 85,
    domainConfidence: 8,
    domainEffectiveScore: 68,
    domainWeight: 35,
    detailsCID: "QmExampleCID123456789",
  };

  const details = { ...evaluationScore, agentWalletAddress };

  return { evaluationScore, details };
}

async function storeEvaluationIPFS(details: any) {
  console.log(`Storing evaluation... `);
  return "ipsfCID786451351";
}

if (require.main === module) {
  runEvaluation().catch(console.error);
}
