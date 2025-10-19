import { attestAgentEvaluation } from "./agent-attestation";
import { envSetup } from "./utils";
import { evaluateAgent } from "./agent-evaluation";
import { storeEvaluationIPFS } from "./ipfs-storage";

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

async function runEvaluation(agentAddress: string) {
  const { url, pk } = envSetup();
  if (!pk || !url) throw new Error("ENV error");

  console.log(`Evaluating Agent ${agentAddress}... `);
  const { evaluationScore, details } = await evaluateAgent(agentAddress);

  const ipfsCID = await storeEvaluationIPFS(details);

  evaluationScore.detailsCID = ipfsCID;

  console.log("eval score:");
  console.log(evaluationScore);

  console.log("Attesting Evaluation...");
  await attestAgentEvaluation(evaluationScore, details.agentWalletAddress);
}

if (require.main === module) {
  const SEO_ANALYIST_AGENT =
    "agent1qv4kfack2hq3ppn7l2hglae29wvfzesacjq35ethl8yj08gshr7tkwlwlgp";
  const agentToEvaluate =
    "agent1qdpyzp043kf7h6yhygnfz79tljchzjcsvz626uty4s9xyhcrhas2zsr0hrs";
  runEvaluation(SEO_ANALYIST_AGENT).catch(console.error);
}
