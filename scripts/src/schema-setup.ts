import { SchemaRegistry } from "@ethereum-attestation-service/eas-sdk";
import { ethers } from "ethers";
import { extractSchemaUID, decodeLogs, envSetup } from "./utils";

/**
 * Create Schema functionality -> create an attestation schema
 * prerequisites:
 *  - access to onchain aes
 *  - access to pk.
 */

// scoring schema
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

const humanSchema = `(
    bytes32 originalAttestationUID,
    address verifier,
    uint64 timestamp,
    bool approved,
    string comment,
  )`;

async function createAgentSchema() {
  const { url, pk } = envSetup();
  if (!pk || !url) throw new Error("ENV error");
  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);

  const schemaRegistryContractAddress =
    "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0";

  const schemaRegistry = new SchemaRegistry(schemaRegistryContractAddress);
  schemaRegistry.connect(signer);

  const resolverAddress = ethers.ZeroAddress; // Sepolia 0.26
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
    const decodedLogs = decodeLogs(receipt.logs);
    decodedLogs.forEach((log, index) => {
      console.log(`\nLog ${index + 1}:`);
      console.log("Type:", log.type);
      if (log.type === "Schema Registered") {
        console.log("Contract:", log.contract);
        console.log("Schema UID:", log.uid);
        console.log("Registerer:", log.registerer);
        console.log("Schema Record:", log.schema);
      } else if (log.type === "Unknown") {
        console.log("Address:", log.address);
        console.log("Topics:", log.topics);
        console.log("Data:", log.data);
      } else if (log.type === "Error decoding") {
        console.log("Error:", log.error);
        console.log("Raw Log:", log.log);
      }
    });

    console.log("\n=== Schema UID Extraction ===");
    const schemaUID = extractSchemaUID(receipt);

    if (schemaUID) {
      console.log("✅ Schema UID extracted successfully:", schemaUID);
      return schemaUID;
    } else {
      console.log("❌ Failed to extract schema UID from transaction receipt");
      return null;
    }
  } catch (error) {
    console.error("❌ Error registering schema:", error);
    throw error;
  }
}

async function createHumanSchema() {
  const { url, pk } = envSetup();

  if (!pk || !url) {
    console.error("❌ Missing environment variables: SEPOLIA_RPC or DT_KEY");
    return;
  }

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);

  const schemaRegistryContractAddress =
    "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0";

  const schemaRegistry = new SchemaRegistry(schemaRegistryContractAddress);
  schemaRegistry.connect(signer);

  const resolverAddress = ethers.ZeroAddress; // Sepolia 0.26
  const revocable = false;

  try {
    console.log("Registering schema...");
    const transaction = await schemaRegistry.register({
      schema: humanSchema,
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
    const decodedLogs = decodeLogs(receipt.logs);
    decodedLogs.forEach((log, index) => {
      console.log(`\nLog ${index + 1}:`);
      console.log("Type:", log.type);
      if (log.type === "Schema Registered") {
        console.log("Contract:", log.contract);
        console.log("Schema UID:", log.uid);
        console.log("Registerer:", log.registerer);
        console.log("Schema Record:", log.schema);
      } else if (log.type === "Unknown") {
        console.log("Address:", log.address);
        console.log("Topics:", log.topics);
        console.log("Data:", log.data);
      } else if (log.type === "Error decoding") {
        console.log("Error:", log.error);
        console.log("Raw Log:", log.log);
      }
    });

    console.log("\n=== Schema UID Extraction ===");
    const schemaUID = extractSchemaUID(receipt);

    if (schemaUID) {
      console.log("✅ Schema UID extracted successfully:", schemaUID);
      return schemaUID;
    } else {
      console.log("❌ Failed to extract schema UID from transaction receipt");
      return null;
    }
  } catch (error) {
    console.error("❌ Error registering schema:", error);
    throw error;
  }
}

async function getSchemaInfo() {
  const { url, pk } = envSetup();

  if (!pk || !url) {
    console.error("❌ Missing environment variables: SEPOLIA_RPC or DT_KEY");
    return;
  }

  console.log(" Getting Schema Info...");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);
  const schemaRegistryContractAddress =
    "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0"; // Sepolia 0.26
  const schemaRegistry = new SchemaRegistry(schemaRegistryContractAddress);

  schemaRegistry.connect(provider);

  const schemaUID =
    "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc";
  const humanSchemaUID =
    "0x35bf5bfce7eaa219f46c086d4d60bfe96affaa42a0d2ae1abf17057e6607007d";

  console.log("Schema UID:", humanSchemaUID);

  const schemaRecord = await schemaRegistry.getSchema({ uid: humanSchemaUID });

  console.log(schemaRecord);
}

if (require.main === module) {
  getSchemaInfo().catch(console.error);
}
