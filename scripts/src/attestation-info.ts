// Functionality to be implemented in the frontend.

import {
  Attestation,
  EAS,
  SchemaEncoder,
} from "@ethereum-attestation-service/eas-sdk";
import { envSetup, createEvaluationScoreFromDecoded } from "./utils";
import { ethers } from "ethers";
import { encodingSchema } from "./type";

const { url, pk } = envSetup();

async function getAttestationInfo(attestionUid: string) {
  const easContractAddress = "0xC2679fBD37d54388Ce493F1DB75320D236e1815e"; //SEPOLIA TESTNET
  const eas = new EAS(easContractAddress);

  if (!pk || !url) throw new Error(".env error");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);
  await eas.connect(signer);

  const attestation: Attestation = await eas.getAttestation(attestionUid);
  console.log(attestation);

  console.log();
  console.log("DECODED SCHEMA DATA...");

  const dataDecoder = new SchemaEncoder(encodingSchema);
  const result = await dataDecoder.decodeData(attestation.data);

  console.log(result);

  console.log();
  console.log("EVALUATION SCORE OBJECT...");

  // Convert decoded data to typed EvaluationScore object
  const evaluationScore = createEvaluationScoreFromDecoded(result);
  console.log(evaluationScore);
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

async function getAllEvaluationScoreAttestions() {}

async function getAttestionScoreDetails() {}

if (require.main === module) {
  const attestionUid =
    "0x1e903e1eaa9d7b7f064b7f816b91a08f2d4c67afb712527f80c81e9adbcb18a3";
  getAttestationInfo(attestionUid).catch(console.error);
}
