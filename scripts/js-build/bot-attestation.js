"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const path = require("path");
const dotenv_1 = require("dotenv");
const eas_sdk_1 = require("@ethereum-attestation-service/eas-sdk");
const ethers_1 = require("ethers");
const utils_1 = require("./utils");
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
    }
    catch {
        return false;
    }
});
if (!envPath) {
    envPath = possiblePaths[0]; // fallback to first option
}
console.log("Loading .env from:", envPath);
(0, dotenv_1.configDotenv)({
    path: envPath,
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
const url = process.env.SEPOLIA_RPC;
const pk = process.env.DT_KEY;
const schema = `(
    string evaluatedAgentAddress,
    string evaluatorAgentAddress,
    uint256 timestamp,
    uint256 finalScore,
    uint8 overallConfidence,
    string grade,
    uint256 correctnessScore,
    uint8 correctnessConfidence,
    uint256 correctnessEffectiveScore,
    uint8 correctnessWeight,
    uint256 capabilitiesScore,
    uint8 capabilitiesConfidence,
    uint256 capabilitiesEffectiveScore,
    uint8 capabilitiesWeight,
    uint256 domainScore,
    uint8 domainConfidence,
    uint256 domainEffectiveScore,
    uint8 domainWeight,
    string detailsCID
  )`;
const encodingSchema = `string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID`;
async function createSchema() {
    if (!pk || !url)
        throw new Error("ENV error");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    const schemaRegistryContractAddress = "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0";
    const schemaRegistry = new eas_sdk_1.SchemaRegistry(schemaRegistryContractAddress);
    schemaRegistry.connect(signer);
    const resolverAddress = ethers_1.ethers.ZeroAddress; // Sepolia 0.26
    const revocable = false;
    try {
        console.log("Registering schema...");
        const transaction = await schemaRegistry.register({
            schema,
            resolverAddress,
            revocable,
        });
        console.log("Waiting for transaction confirmation...");
        const txHash = await transaction.wait();
        // Get the full transaction receipt
        const receipt = await provider.getTransactionReceipt(txHash);
        if (!receipt) {
            throw new Error("Failed to get transaction receipt");
        }
        console.log("\n=== Transaction Receipt ===");
        console.log("Transaction Hash:", receipt.hash);
        console.log("Block Number:", receipt.blockNumber);
        console.log("Gas Used:", receipt.gasUsed.toString());
        console.log("Status:", receipt.status === 1 ? "Success" : "Failed");
        console.log("\n=== Decoded Logs ===");
        const decodedLogs = (0, utils_1.decodeLogs)(receipt.logs);
        decodedLogs.forEach((log, index) => {
            console.log(`\nLog ${index + 1}:`);
            console.log("Type:", log.type);
            if (log.type === "Schema Registered") {
                console.log("Contract:", log.contract);
                console.log("Schema UID:", log.uid);
                console.log("Registerer:", log.registerer);
                console.log("Schema Record:", log.schema);
            }
            else if (log.type === "Unknown") {
                console.log("Address:", log.address);
                console.log("Topics:", log.topics);
                console.log("Data:", log.data);
            }
            else if (log.type === "Error decoding") {
                console.log("Error:", log.error);
                console.log("Raw Log:", log.log);
            }
        });
        console.log("\n=== Schema UID Extraction ===");
        const schemaUID = (0, utils_1.extractSchemaUID)(receipt);
        if (schemaUID) {
            console.log("✅ Schema UID extracted successfully:", schemaUID);
            return schemaUID;
        }
        else {
            console.log("❌ Failed to extract schema UID from transaction receipt");
            return null;
        }
    }
    catch (error) {
        console.error("❌ Error registering schema:", error);
        throw error;
    }
}
async function getSchemaInfo() {
    const url = process.env.SEPOLIA_RPC;
    const pk = process.env.DT_KEY;
    if (!pk || !url) {
        console.error("❌ Missing environment variables: SEPOLIA_RPC or DT_KEY");
        return;
    }
    console.log(" Getting Schema Info...");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    const schemaRegistryContractAddress = "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0"; // Sepolia 0.26
    const schemaRegistry = new eas_sdk_1.SchemaRegistry(schemaRegistryContractAddress);
    schemaRegistry.connect(provider);
    const schemaUID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";
    console.log("Schema UID:", schemaUID);
    const schemaRecord = await schemaRegistry.getSchema({ uid: schemaUID });
    console.log(schemaRecord);
}
async function attestAgentEvaluation() {
    // VALIDATE PK ADDRESS WITH RESOLVER CONTRACT, ADD VALIDATION LOGIC?
    const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET
    const schemaUID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";
    const eas = new eas_sdk_1.EAS(easContractAddress);
    const url = process.env.SEPOLIA_RPC;
    const pk = process.env.DT_KEY;
    if (!pk || !url)
        throw new Error(".env error");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    await eas.connect(signer);
    const schemaEncoder = new eas_sdk_1.SchemaEncoder(encodingSchema);
    const encodedData = schemaEncoder.encodeData([
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
    const tx = await eas.attest({
        schema: schemaUID,
        data: {
            recipient: "0x0000000000000000000000000000000000000000",
            expirationTime: 0n,
            revocable: false,
            data: encodedData,
        },
    });
    const newAttestationUID = await tx.wait();
    console.log("New attestation UID:", newAttestationUID);
}
async function getAttestation() {
    // use EAS sdk
    const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e";
    const eas = new eas_sdk_1.EAS(easContractAddress);
    const url = process.env.SEPOLIA_RPC;
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    eas.connect(provider);
    const uid = "0xff08bbf3d3e6e0992fc70ab9b9370416be59e87897c3d42b20549901d2cccc3e";
    const attestation = await eas.getAttestation(uid);
    console.log(attestation);
    // use graphQL
}
if (require.main === module) {
    attestAgentEvaluation().catch(console.error);
}
