"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.extractSchemaUID = extractSchemaUID;
exports.decodeLogs = decodeLogs;
exports.decodeError = decodeError;
exports.envSetup = envSetup;
exports.createEvaluationScoreFromDecoded = createEvaluationScoreFromDecoded;
exports.encodeAttestationData = encodeAttestationData;
const ethers_1 = require("ethers");
const path = require("path");
const dotenv_1 = require("dotenv");
const type_1 = require("./type");
const SCHEMA_REGISTRY_ABI = [
    "event Registered(bytes32 indexed uid, address indexed registerer, tuple(bytes32 uid, address resolver, bool revocable, string schema) schema)",
];
const SCHEMA_REGISTRY_INTERFACE = new ethers_1.ethers.Interface(SCHEMA_REGISTRY_ABI);
/**
 * Extracts the schema UID from a transaction receipt after schema registration
 * @param receipt - The transaction receipt from schemaRegistry.register()
 * @returns The schema UID if found, null otherwise
 */
function extractSchemaUID(receipt) {
    try {
        const decodedLogs = decodeLogs(receipt.logs);
        const registeredEvent = decodedLogs.find((log) => log.type === "Schema Registered");
        if (registeredEvent) {
            return registeredEvent.uid;
        }
        return null;
    }
    catch (error) {
        console.error("Error extracting schema UID:", error);
        return null;
    }
}
function decodeLogs(logs) {
    const decodedLogs = [];
    for (const log of logs) {
        try {
            // Check if this is a Schema Registry Registered event
            if (log.topics[0] ===
                SCHEMA_REGISTRY_INTERFACE.getEvent("Registered").topicHash) {
                const decoded = SCHEMA_REGISTRY_INTERFACE.parseLog({
                    topics: log.topics,
                    data: log.data,
                });
                if (!decoded)
                    throw new Error("Failed to decode Schema Registry Registered event");
                decodedLogs.push({
                    type: "Schema Registered",
                    contract: log.address,
                    uid: decoded.args.uid,
                    registerer: decoded.args.registerer,
                    schema: decoded.args.schema,
                });
            }
            else {
                decodedLogs.push({
                    type: "Unknown",
                    address: log.address,
                    topics: log.topics,
                    data: log.data,
                });
            }
        }
        catch (error) {
            decodedLogs.push({ type: "Error decoding", log, error });
        }
    }
    return decodedLogs;
}
function decodeError(errorOrData) {
    const errorData = typeof errorOrData === "string"
        ? errorOrData
        : errorOrData?.data ?? errorOrData?.error?.data;
    if (!errorData || errorData === "0x" || typeof errorData !== "string") {
        return { type: "No error data", selector: null, decoded: null };
    }
    const selector = errorData.slice(0, 10);
    // Try to decode with Schema Registry interface
    try {
        const decoded = SCHEMA_REGISTRY_INTERFACE.parseError(errorData);
        if (decoded) {
            return {
                type: "Decoded",
                contract: "SchemaRegistry",
                selector,
                errorName: decoded.name,
                signature: decoded.signature,
                args: decoded.args,
                decoded,
            };
        }
    }
    catch {
        // continue trying
    }
    try {
        const iError = new ethers_1.ethers.Interface(["error Error(string)"]);
        const parsed = iError.parseError(errorData);
        if (parsed)
            return { type: "Error(string)", selector, message: parsed.args[0] };
    }
    catch { }
    try {
        const iPanic = new ethers_1.ethers.Interface(["error Panic(uint256)"]);
        const parsed = iPanic.parseError(errorData);
        if (parsed)
            return {
                type: "Panic(uint256)",
                selector,
                code: parsed.args[0].toString(),
            };
    }
    catch { }
    return {
        type: "Unknown",
        selector,
        rawData: errorData,
        possibleParams: analyzeErrorParams(errorData),
    };
}
function analyzeErrorParams(errorData) {
    if (errorData.length <= 10) {
        return { analysis: "No parameters" };
    }
    const paramData = errorData.slice(10);
    const paramCount = paramData.length / 64;
    if (paramCount !== Math.floor(paramCount)) {
        return { analysis: "Invalid parameter length" };
    }
    const params = [];
    for (let i = 0; i < paramCount; i++) {
        const paramHex = paramData.slice(i * 64, (i + 1) * 64);
        const paramValue = BigInt("0x" + paramHex);
        if (paramHex.startsWith("000000000000000000000000") &&
            paramHex.length === 64) {
            const address = "0x" + paramHex.slice(24);
            params.push({
                index: i,
                hex: "0x" + paramHex,
                uint256: paramValue.toString(),
                possibleAddress: address,
                type: "address-like",
            });
        }
        else {
            params.push({
                index: i,
                hex: "0x" + paramHex,
                uint256: paramValue.toString(),
                type: "uint256",
            });
        }
    }
    return { analysis: `${paramCount} parameters detected`, parameters: params };
}
function envSetup() {
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
    const url = process.env.SEPOLIA_RPC;
    const pk = process.env.DT_KEY;
    return { url, pk };
}
function createEvaluationScoreFromDecoded(decodedData) {
    // Create a map for easy field access
    const fieldMap = new Map();
    decodedData.forEach((field) => {
        fieldMap.set(field.name, field.value.value);
    });
    // Helper to get and validate required field
    const getField = (name, expectedType) => {
        if (!fieldMap.has(name)) {
            throw new Error(`Missing required field: ${name}`);
        }
        const value = fieldMap.get(name);
        // Type validation
        const actualType = typeof value === "bigint" ? "bigint" : typeof value;
        if (expectedType === "numeric" &&
            actualType !== "bigint" &&
            actualType !== "number") {
            throw new Error(`Field ${name} expected bigint or number, got ${actualType}`);
        }
        if (expectedType === "string" && actualType !== "string") {
            throw new Error(`Field ${name} expected string, got ${actualType}`);
        }
        return value;
    };
    // Helper to convert BigInt or number to number with validation
    const toNumber = (value, fieldName, max) => {
        const num = typeof value === "bigint" ? Number(value) : value;
        if (max !== undefined && num > max) {
            throw new Error(`Field ${fieldName} value ${num} exceeds maximum ${max}`);
        }
        if (num < 0) {
            throw new Error(`Field ${fieldName} value ${num} cannot be negative`);
        }
        return num;
    };
    // Extract and validate all fields
    const evaluatedAgentAddress = getField("evaluatedAgentAddress", "string");
    const evaluatorAgentAddress = getField("evaluatorAgentAddress", "string");
    const timestamp = toNumber(getField("timestamp", "numeric"), "timestamp");
    const finalScore = toNumber(getField("finalScore", "numeric"), "finalScore", 100);
    const overallConfidence = toNumber(getField("overallConfidence", "numeric"), "overallConfidence", 10);
    const grade = getField("grade", "string");
    const correctnessScore = toNumber(getField("correctnessScore", "numeric"), "correctnessScore", 100);
    const correctnessConfidence = toNumber(getField("correctnessConfidence", "numeric"), "correctnessConfidence", 10);
    const correctnessEffectiveScore = toNumber(getField("correctnessEffectiveScore", "numeric"), "correctnessEffectiveScore", 100);
    const correctnessWeight = toNumber(getField("correctnessWeight", "numeric"), "correctnessWeight", 100);
    const capabilitiesScore = toNumber(getField("capabilitiesScore", "numeric"), "capabilitiesScore", 100);
    const capabilitiesConfidence = toNumber(getField("capabilitiesConfidence", "numeric"), "capabilitiesConfidence", 10);
    const capabilitiesEffectiveScore = toNumber(getField("capabilitiesEffectiveScore", "numeric"), "capabilitiesEffectiveScore", 100);
    const capabilitiesWeight = toNumber(getField("capabilitiesWeight", "numeric"), "capabilitiesWeight", 100);
    const domainScore = toNumber(getField("domainScore", "numeric"), "domainScore", 100);
    const domainConfidence = toNumber(getField("domainConfidence", "numeric"), "domainConfidence", 10);
    const domainEffectiveScore = toNumber(getField("domainEffectiveScore", "numeric"), "domainEffectiveScore", 100);
    const domainWeight = toNumber(getField("domainWeight", "numeric"), "domainWeight", 100);
    const detailsCID = getField("detailsCID", "string");
    // Additional validation
    if (evaluatedAgentAddress.length === 0) {
        throw new Error("evaluatedAgentAddress cannot be empty");
    }
    if (evaluatorAgentAddress.length === 0) {
        throw new Error("evaluatorAgentAddress cannot be empty");
    }
    if (detailsCID.length === 0) {
        throw new Error("detailsCID cannot be empty");
    }
    // Validate weights sum to 100 (optional but good practice)
    const totalWeight = correctnessWeight + capabilitiesWeight + domainWeight;
    if (totalWeight !== 100) {
        console.warn(`Warning: Total weights (${totalWeight}) do not sum to 100`);
    }
    return {
        evaluatedAgentAddress,
        evaluatorAgentAddress,
        timestamp,
        finalScore,
        overallConfidence,
        grade,
        correctnessScore,
        correctnessConfidence,
        correctnessEffectiveScore,
        correctnessWeight,
        capabilitiesScore,
        capabilitiesConfidence,
        capabilitiesEffectiveScore,
        capabilitiesWeight,
        domainScore,
        domainConfidence,
        domainEffectiveScore,
        domainWeight,
        detailsCID,
    };
}
function encodeAttestationData(evaluationScore) {
    const types = type_1.encodingSchema.split(", ").map((field) => {
        const parts = field.trim().split(" ");
        if (!parts[0]) {
            throw new Error(`Invalid schema field: ${field}`);
        }
        return parts[0]; // Get just the type (e.g., "string", "uint256", "uint8")
    });
    const values = [
        evaluationScore.evaluatedAgentAddress,
        evaluationScore.evaluatorAgentAddress,
        evaluationScore.timestamp,
        evaluationScore.finalScore,
        evaluationScore.overallConfidence,
        evaluationScore.grade,
        evaluationScore.correctnessScore,
        evaluationScore.correctnessConfidence,
        evaluationScore.correctnessEffectiveScore,
        evaluationScore.correctnessWeight,
        evaluationScore.capabilitiesScore,
        evaluationScore.capabilitiesConfidence,
        evaluationScore.capabilitiesEffectiveScore,
        evaluationScore.capabilitiesWeight,
        evaluationScore.domainScore,
        evaluationScore.domainConfidence,
        evaluationScore.domainEffectiveScore,
        evaluationScore.domainWeight,
        evaluationScore.detailsCID,
    ];
    const abiCoder = ethers_1.ethers.AbiCoder.defaultAbiCoder();
    return abiCoder.encode(types, values);
}
