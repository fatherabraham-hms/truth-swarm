// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Script.sol";

interface ISchemaRegistry {
    struct SchemaRecord {
        bytes32 uid;
        address resolver;
        bool revocable;
        string schema;
    }

    function register(string calldata schema, address resolver, bool revocable) external returns (bytes32);

    function getSchema(bytes32 uid) external view returns (SchemaRecord memory);
}

contract CreateTruthSwarmSchemasSepolia is Script {
    address constant SCHEMA_REGISTRY = 0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0;

    string constant AGENT_SCHEMA =
        "string evaluatedAgentAddress,string evaluatorAgentAddress,uint256 timestamp,uint256 finalScore,uint8 overallConfidence,string grade,uint256 correctnessScore,uint8 correctnessConfidence,uint256 correctnessEffectiveScore,uint8 correctnessWeight,uint256 capabilitiesScore,uint8 capabilitiesConfidence,uint256 capabilitiesEffectiveScore,uint8 capabilitiesWeight,uint256 domainScore,uint8 domainConfidence,uint256 domainEffectiveScore,uint8 domainWeight,string detailsCID";

    string constant HUMAN_SCHEMA =
        "bytes32 originalAttestationUID,address verifier,uint64 timestamp,bool approved,string comment";

    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        ISchemaRegistry registry = ISchemaRegistry(SCHEMA_REGISTRY);

        console.log("Registering agent scoring schema...");
        bytes32 agentSchemaUID = registry.register(
            AGENT_SCHEMA,
            address(0), // No resolver
            false // Not revocable
        );
        console.log("Agent Schema UID:");
        console.logBytes32(agentSchemaUID);

        // Register human verification schema
        console.log("\nRegistering human verification schema...");
        bytes32 humanSchemaUID = registry.register(
            HUMAN_SCHEMA,
            address(0), // No resolver
            false // Not revocable
        );
        console.log("Human Schema UID:");
        console.logBytes32(humanSchemaUID);

        vm.stopBroadcast();

        console.log("\n=== Summary ===");
        console.log("Agent Schema UID:");
        console.logBytes32(agentSchemaUID);
        console.log("Human Schema UID:");
        console.logBytes32(humanSchemaUID);
    }

    // Optional: Function to verify schemas after deployment
    function verify(bytes32 agentUID, bytes32 humanUID) external view {
        ISchemaRegistry registry = ISchemaRegistry(SCHEMA_REGISTRY);

        ISchemaRegistry.SchemaRecord memory agentSchema = registry.getSchema(agentUID);
        ISchemaRegistry.SchemaRecord memory humanSchema = registry.getSchema(humanUID);

        console.log("Agent Schema:");
        console.log("  Schema:", agentSchema.schema);
        console.log("  Revocable:", agentSchema.revocable);

        console.log("\nHuman Schema:");
        console.log("  Schema:", humanSchema.schema);
        console.log("  Revocable:", humanSchema.revocable);
    }
}

