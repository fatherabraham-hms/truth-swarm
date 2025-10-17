"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const eas_sdk_1 = require("@ethereum-attestation-service/eas-sdk");
const schema = `string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID`;
async function debugSchema() {
    console.log("Schema:", schema);
    console.log("Schema length:", schema.length);
    try {
        const schemaEncoder = new eas_sdk_1.SchemaEncoder(schema);
        console.log("SchemaEncoder created successfully");
        console.log("Schema fields count:", schemaEncoder.schema.length);
        // Test with minimal data
        const testData = [
            { name: "evaluatedAgentAddress", value: "test", type: "string" },
            { name: "evaluatorAgentAddress", value: "test", type: "string" },
            { name: "timestamp", value: "1234567890", type: "uint256" },
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
        ];
        console.log("Test data length:", testData.length);
        console.log("Test data fields:", testData.map(d => d.name));
        const encodedData = schemaEncoder.encodeData(testData);
        console.log("Encoding successful!");
        console.log("Encoded data length:", encodedData.length);
    }
    catch (error) {
        console.error("Error:", error);
        console.error("Error details:", error instanceof Error ? error.message : String(error));
    }
}
if (require.main === module) {
    debugSchema().catch(console.error);
}
