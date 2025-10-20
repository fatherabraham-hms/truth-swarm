const { ethers } = require("hardhat");

async function main() {
    console.log("Deploying contracts...");

    // Get the ContractFactory and Signers here.
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
    console.log("Account balance:", ethers.formatEther(await deployer.provider.getBalance(deployer.address)));

    // Deploy MockEAS first
    console.log("\nDeploying MockEAS...");
    const MockEAS = await ethers.getContractFactory("MockEAS");
    const mockEAS = await MockEAS.deploy();
    console.log("MockEAS deployed to:", mockEAS.target);

    // Deploy MockSchemaRegistry
    console.log("\nDeploying MockSchemaRegistry...");
    const MockSchemaRegistry = await ethers.getContractFactory("MockSchemaRegistry");
    const schemaRegistry = await MockSchemaRegistry.deploy();
    console.log("MockSchemaRegistry deployed to:", schemaRegistry.target);
    
    // Set schema registry in MockEAS
    await mockEAS.setSchemaRegistry(schemaRegistry.target);
    console.log("Schema registry set in MockEAS");
    
    // Register test schemas
    console.log("\nRegistering test schemas...");
    
    // Agent Evaluation Schema
    const agentEvaluationSchema = "string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID";
    const agentEvaluationSchemaUID = await schemaRegistry.register(agentEvaluationSchema, false);
    console.log("Agent Evaluation Schema UID:", agentEvaluationSchemaUID);

    // Human Verification Schema
    const humanVerificationSchema = "bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment";
    const humanVerificationSchemaUID = await schemaRegistry.register(humanVerificationSchema, false);
    console.log("Human Verification Schema UID:", humanVerificationSchemaUID);

    // Deploy AttesterResolver
    console.log("\nDeploying AttesterResolver...");
    const AttesterResolver = await ethers.getContractFactory("AttesterResolver");
    
    // Initialize with deployer as authorized attester
    const initialAttesters = [deployer.address];
    const attesterResolver = await AttesterResolver.deploy(mockEAS.target, initialAttesters);
    console.log("AttesterResolver deployed to:", attesterResolver.target);

    // Verify deployment
    console.log("\nVerifying deployment...");
    const authorizedAttesters = await attesterResolver.getTargetAttesters();
    console.log("Authorized attesters:", authorizedAttesters);

    // Save deployment info
    const deploymentInfo = {
        network: "hardhat",
        chainId: 31337,
        contracts: {
            MockEAS: {
                address: mockEAS.target,
                abi: MockEAS.interface.format("json")
            },
            AttesterResolver: {
                address: attesterResolver.target,
                abi: AttesterResolver.interface.format("json")
            },
            SchemaRegistry: {
                address: schemaRegistry.target,
                abi: MockSchemaRegistry.interface.format("json")
            }
        },
        schemas: {
            agentEvaluation: agentEvaluationSchemaUID,
            humanVerification: humanVerificationSchemaUID
        },
        deployer: deployer.address,
        timestamp: new Date().toISOString()
    };

    // Write deployment info to file
    const fs = require('fs');
    fs.writeFileSync('./deployment.json', JSON.stringify(deploymentInfo, null, 2));
    console.log("\nDeployment info saved to deployment.json");

    console.log("\nDeployment completed successfully!");
    console.log("You can now start testing your agent with these contract addresses.");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
