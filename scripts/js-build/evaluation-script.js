"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const agent_attestation_1 = require("./agent-attestation");
const utils_1 = require("./utils");
const agent_evaluation_1 = require("./agent-evaluation");
const ipfs_storage_1 = require("./ipfs-storage");
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
async function runEvaluation(agentAddress) {
    const { url, pk } = (0, utils_1.envSetup)();
    if (!pk || !url)
        throw new Error("ENV error");
    console.log(`Evaluating Agent ${agentAddress}... `);
    const { evaluationScore, details } = await (0, agent_evaluation_1.evaluateAgent)(agentAddress);
    const ipfsCID = await (0, ipfs_storage_1.storeEvaluationIPFS)(details);
    evaluationScore.detailsCID = ipfsCID;
    console.log("eval score:");
    console.log(evaluationScore);
    console.log("Attesting Evaluation...");
    await (0, agent_attestation_1.attestAgentEvaluation)(evaluationScore, details.agentWalletAddress);
}
if (require.main === module) {
    const SEO_ANALYIST_AGENT = "agent1qv4kfack2hq3ppn7l2hglae29wvfzesacjq35ethl8yj08gshr7tkwlwlgp";
    const agentToEvaluate = "agent1qdpyzp043kf7h6yhygnfz79tljchzjcsvz626uty4s9xyhcrhas2zsr0hrs";
    runEvaluation(SEO_ANALYIST_AGENT).catch(console.error);
}
