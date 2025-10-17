#!/usr/bin/env ts-node

/**
 * Test script to demonstrate schema creation with log decoding
 * Run with: npx ts-node test-schema-creation.ts
 */
import * as path from "path";
import { configDotenv } from "dotenv";
import { ethers, sha256 } from "ethers";
import { SchemaRegistry } from "@ethereum-attestation-service/eas-sdk";
import { extractSchemaUID, decodeLogs } from "./utils";

// Setup Dotenv
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

// Load environment variables
configDotenv();

async function testSchemaCreation() {
  const url = process.env.SEPOLIA_RPC;
  const pk = process.env.DT_KEY;

  if (!pk || !url) {
    console.error("❌ Missing environment variables: SEPOLIA_RPC or DT_KEY");
    return;
  }

  console.log("🚀 Starting schema creation test...");

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);

  const schemaRegistryContractAddress =
    "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0";
  const schemaRegistry = new SchemaRegistry(schemaRegistryContractAddress);
  schemaRegistry.connect(signer);

  // Simple test schema
  const schema = `(
    string name,
    uint256 score,
    bool verified
  )`;

  const resolverAddress = ethers.ZeroAddress;
  const revocable = true;

  try {
    console.log("📝 Registering test schema...");
    const transaction = await schemaRegistry.register({
      schema,
      resolverAddress,
      revocable,
    });

    console.log("⏳ Waiting for transaction confirmation...");
    const txHash = await transaction.wait();
    console.log("tx Hash:");
    console.log(txHash);

    // Get the full transaction receipt
    const receipt = await provider.getTransactionReceipt(txHash);
    if (!receipt) {
      throw new Error("Failed to get transaction receipt");
    }

    console.log("\n" + "=".repeat(60));
    console.log("📋 TRANSACTION RECEIPT");
    console.log("=".repeat(60));
    console.log("Transaction Hash:", receipt.hash);
    console.log("Block Number:", receipt.blockNumber);
    console.log("Gas Used:", receipt.gasUsed.toString());
    console.log("Status:", receipt.status === 1 ? "✅ Success" : "❌ Failed");

    console.log("\n" + "=".repeat(60));
    console.log("🔍 DECODED LOGS");
    console.log("=".repeat(60));
    const decodedLogs = decodeLogs(receipt.logs);

    if (decodedLogs.length === 0) {
      console.log("No logs found in transaction");
    } else {
      decodedLogs.forEach((log, index) => {
        console.log(`\n📄 Log ${index + 1}:`);
        console.log("   Type:", log.type);

        if (log.type === "Schema Registered") {
          console.log("   Contract:", log.contract);
          console.log("   Schema UID:", log.uid);
          console.log("   Registerer:", log.registerer);
          console.log("   Schema Record:", JSON.stringify(log.schema, null, 2));
        } else if (log.type === "Unknown") {
          console.log("   Address:", log.address);
          console.log("   Topics:", log.topics);
          console.log("   Data:", log.data);
        } else if (log.type === "Error decoding") {
          console.log("   Error:", log.error);
          console.log("   Raw Log:", log.log);
        }
      });
    }

    console.log("\n" + "=".repeat(60));
    console.log("🎯 SCHEMA UID EXTRACTION");
    console.log("=".repeat(60));
    const schemaUID = extractSchemaUID(receipt);

    if (schemaUID) {
      console.log("✅ Schema UID extracted successfully!");
      console.log("Schema UID:", schemaUID);
      console.log("\n🎉 Test completed successfully!");
      console.log("You can now use this schema UID for creating attestations.");
    } else {
      console.log("❌ Failed to extract schema UID from transaction receipt");
    }
  } catch (error) {
    console.error("❌ Error during schema creation:", error);
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

  const provider = new ethers.JsonRpcProvider(url);
  const signer = new ethers.Wallet(pk, provider);
  const schemaRegistryContractAddress =
    "0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0"; // Sepolia 0.26
  const schemaRegistry = new SchemaRegistry(schemaRegistryContractAddress);

  schemaRegistry.connect(provider);

  const schemaUID = "0x4E86759463b66836EE96a1F10fE61be64eD1414F";
  console.log("Schema UID:", schemaUID);

  const schemaRecord = await schemaRegistry.getSchema({ uid: schemaUID });

  console.log(schemaRecord);
}

// Run the test
if (require.main === module) {
  getSchemaInfo().catch(console.error);
}
