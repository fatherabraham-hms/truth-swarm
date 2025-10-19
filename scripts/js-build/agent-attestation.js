"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.attestAgentEvaluation = attestAgentEvaluation;
exports.attestAgentEvaluationSDK = attestAgentEvaluationSDK;
const ethers_1 = require("ethers");
const utils_1 = require("./utils");
const abis_1 = require("./abis");
const eas_sdk_1 = require("@ethereum-attestation-service/eas-sdk");
const type_1 = require("./type");
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
const AGENT_ATTESTATION_SCHEMA_UID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";
const EAS_CONTRACT_ADDRESS = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET
async function attestAgentEvaluation(evaluationScore, evaluatedAgentWalletAddress) {
    const { url, pk } = (0, utils_1.envSetup)();
    if (!pk || !url)
        throw new Error(".env error");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    const encodedData = (0, utils_1.encodeAttestationData)(evaluationScore);
    let recipient;
    if (evaluatedAgentWalletAddress === ethers_1.ethers.ZeroAddress ||
        evaluatedAgentWalletAddress.trim() === "" ||
        evaluatedAgentWalletAddress === "0x") {
        recipient = ethers_1.ethers.ZeroAddress;
    }
    else {
        recipient = evaluatedAgentWalletAddress;
    }
    const attestationRequest = {
        schema: AGENT_ATTESTATION_SCHEMA_UID,
        data: {
            recipient: recipient,
            expirationTime: 0, // uint63
            revocable: false,
            refUID: ethers_1.ethers.ZeroHash, // bytes31 - using ZeroHash for empty reference
            data: encodedData,
            value: 0, // uint255 - no ETH value being sent with attestation
        },
    };
    const attestFunction = abis_1.EAS_INTERFACE.getFunction("attest");
    if (!attestFunction) {
        throw new Error("attest function not found in ABI");
    }
    const functionSelector = attestFunction.selector;
    console.log(functionSelector);
    const abiCoder = ethers_1.ethers.AbiCoder.defaultAbiCoder();
    const encodedParams = abiCoder.encode([
        "tuple(bytes32 schema, tuple(address recipient, uint64 expirationTime, bool revocable, bytes32 refUID, bytes data, uint256 value) data)",
    ], [attestationRequest]);
    //functionSelector + encodedParams.slice(2); // Remove '0x' from encoded params
    const callData = ethers_1.ethers.concat([functionSelector, encodedParams]);
    console.log("Submitting attestation to EAS contract...");
    console.log("Schema:", AGENT_ATTESTATION_SCHEMA_UID);
    console.log("Recipient:", recipient);
    console.log("Attester:", signer.address);
    const txRequest = {
        to: EAS_CONTRACT_ADDRESS,
        data: callData,
        from: signer.address,
    };
    try {
        await signer.call(txRequest);
        console.log("call passed");
    }
    catch (error) {
        console.log("call failed");
        console.log(error);
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
                return abis_1.EAS_INTERFACE.parseLog({
                    topics: [...log.topics],
                    data: log.data,
                });
            }
            catch {
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
async function attestAgentEvaluationSDK(evaluatedAgentWalletAddress, evaluationScore) {
    const { url, pk } = (0, utils_1.envSetup)();
    const eas = new eas_sdk_1.EAS(EAS_CONTRACT_ADDRESS);
    const easContract = new ethers_1.ethers.Contract(EAS_CONTRACT_ADDRESS, abis_1.EAS_INTERFACE);
    if (!pk || !url)
        throw new Error(".env error");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    await eas.connect(signer);
    const schemaEncoder = new eas_sdk_1.SchemaEncoder(type_1.encodingSchema);
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
    }
    else {
        encodedData = schemaEncoder.encodeData([
            {
                name: "evaluatedAgentAddress",
                value: "agent1qdpyzp043kf7h6yhygnfz79tljchzjcsvz626uty4s9xyhcrhas2zsr0hrs",
                type: "string",
            },
            {
                name: "evaluatorAgentAddress",
                value: "agent1qw254tc8q3mcmrseem0pmhu2jd0j7urn2e9cd5tgcg88kmy9wkqhysksdwf",
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
    if (evaluatedAgentWalletAddress === ethers_1.ethers.ZeroAddress ||
        evaluatedAgentWalletAddress.trim() == "") {
        recipient = ethers_1.ethers.ZeroAddress;
    }
    else {
        //validation with regex eth address format
        recipient = evaluatedAgentWalletAddress;
    }
    const tx = await eas.attest({
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
    const agentWalletAddress = ethers_1.ethers.ZeroAddress;
    attestAgentEvaluationSDK(agentWalletAddress).catch(console.error);
}
