"use strict";
// Functionality to be implemented in the frontend.
Object.defineProperty(exports, "__esModule", { value: true });
const eas_sdk_1 = require("@ethereum-attestation-service/eas-sdk");
const utils_1 = require("./utils");
const ethers_1 = require("ethers");
const type_1 = require("./type");
const { url, pk } = (0, utils_1.envSetup)();
async function getAttestationInfo(attestionUid) {
    const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET
    const eas = new eas_sdk_1.EAS(easContractAddress);
    if (!pk || !url)
        throw new Error(".env error");
    const provider = new ethers_1.ethers.JsonRpcProvider(url);
    const signer = new ethers_1.ethers.Wallet(pk, provider);
    await eas.connect(signer);
    const attestation = await eas.getAttestation(attestionUid);
    console.log(attestation);
    console.log();
    console.log("DECODED SCHEMA DATA...");
    const dataDecoder = new eas_sdk_1.SchemaEncoder(type_1.encodingSchema);
    const result = await dataDecoder.decodeData(attestation.data);
    console.log(result);
    console.log();
    console.log("EVALUATION SCORE OBJECT...");
    // Convert decoded data to typed EvaluationScore object
    const evaluationScore = (0, utils_1.createEvaluationScoreFromDecoded)(result);
    console.log(evaluationScore);
}
async function getAllEvaluationScoreAttestions() { }
async function getAttestionScoreDetails() { }
if (require.main === module) {
    const attestionUid = "0x1e903e1eaa9d7b7f064b7f816b91a08f2d4c67afb712527f80c81e9adbcb18a3";
    getAttestationInfo(attestionUid).catch(console.error);
}
