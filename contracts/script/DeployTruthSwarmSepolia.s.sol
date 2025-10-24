// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "forge-std/Script.sol";
import {TruthSwarmResolver, IEAS} from "../src/Resolver.sol";

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

contract DeployTruthSwarmSepolia is Script {
    // Sepolia addresses
    address constant EAS_ADDRESS = 0xC2679fBD37d54388Ce493F1DB75320D236e1815e;
    address constant SCHEMA_REGISTRY = 0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0;

    // Schema definition
    string constant AGENT_SCHEMA =
        "string evaluatedAgentAddress,string evaluatorAgentAddress,uint256 timestamp,uint256 finalScore,uint8 overallConfidence,string grade,uint256 correctnessScore,uint8 correctnessConfidence,uint256 correctnessEffectiveScore,uint8 correctnessWeight,uint256 capabilitiesScore,uint8 capabilitiesConfidence,uint256 capabilitiesEffectiveScore,uint8 capabilitiesWeight,uint256 domainScore,uint8 domainConfidence,uint256 domainEffectiveScore,uint8 domainWeight,string detailsCID";

    string constant HUMAN_SCHEMA =
        "bytes32 originalAttestationUID,address verifier,uint64 timestamp,bool approved,string comment";

    function run() external returns (address resolverAddress, bytes32 agentSchemaUID, bytes32 humanSchemaUID) {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);

        console.log("\n=== TruthSwarm Deployment ===");
        console.log("Deployer:", deployer);
        console.log("Network: Sepolia");

        vm.startBroadcast(deployerPrivateKey);

        // Step 1: Deploy TruthSwarmResolver with initial whitelist
        console.log("\n[1/2] Deploying TruthSwarmResolver...");
        address[] memory initialAttesters = new address[](1);
        initialAttesters[0] = deployer; // Add deployer to initial whitelist

        TruthSwarmResolver resolver = new TruthSwarmResolver(IEAS(EAS_ADDRESS), initialAttesters);
        resolverAddress = address(resolver);

        console.log("  Resolver deployed at:", resolverAddress);
        console.log("  Initial whitelisted attesters:", initialAttesters.length);
        console.log("  - Deployer:", deployer);

        ISchemaRegistry registry = ISchemaRegistry(SCHEMA_REGISTRY);

        // Step 2: Register Agent Schema with resolver
        console.log("\n[2/3] Registering Agent Schema...");
        agentSchemaUID = registry.register(
            AGENT_SCHEMA,
            resolverAddress, // Use our custom resolver
            true // Make it revocable for flexibility
        );
        console.log("  Agent schema registered successfully");

        console.log("\n[3/3] Registering Human Schema...");
        humanSchemaUID = registry.register(
            HUMAN_SCHEMA,
            resolverAddress, // Use our custom resolver
            true // Make it revocable for flexibility
        );
        console.log("  Human schema registered successfully");

        vm.stopBroadcast();

        // Summary
        console.log("\n=== Deployment Summary ===");
        console.log("Resolver Address:", resolverAddress);
        console.log("Agent Schema UID:");
        console.logBytes32(agentSchemaUID);
        console.log("Human Schema UID:");
        console.logBytes32(humanSchemaUID);
        console.log("\nNext steps:");
        console.log("1. Add agent addresses to whitelist using resolver.addAttester()");
        console.log("2. Start creating attestations with the schema UID");
        console.log("3. Only whitelisted agents can create valid attestations");

        return (resolverAddress, agentSchemaUID, humanSchemaUID);
    }

    function addAttester(address payable resolverAddress, address newAttester) external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        TruthSwarmResolver resolver = TruthSwarmResolver(resolverAddress);
        resolver.addAttester(newAttester);

        console.log("Added attester:", newAttester);

        vm.stopBroadcast();
    }
}

