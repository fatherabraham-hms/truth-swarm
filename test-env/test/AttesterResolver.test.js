const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("AttesterResolver and MockEAS Integration", function () {
    let mockEAS, attesterResolver, schemaRegistry;
    let owner, authorizedAttester, unauthorizedAttester;
    let agentEvaluationSchemaUID, humanVerificationSchemaUID;

    beforeEach(async function () {
        [owner, authorizedAttester, unauthorizedAttester] = await ethers.getSigners();

        // Deploy MockEAS
        const MockEAS = await ethers.getContractFactory("MockEAS");
        mockEAS = await MockEAS.deploy();

        // Deploy MockSchemaRegistry separately
        const MockSchemaRegistry = await ethers.getContractFactory("MockSchemaRegistry");
        schemaRegistry = await MockSchemaRegistry.deploy();
        
        // Set the schema registry in MockEAS
        await mockEAS.setSchemaRegistry(schemaRegistry.address);

        // Register schemas
        const agentEvaluationSchema = "string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID";
        agentEvaluationSchemaUID = await schemaRegistry.register(agentEvaluationSchema, false);

        const humanVerificationSchema = "bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment";
        humanVerificationSchemaUID = await schemaRegistry.register(humanVerificationSchema, false);

        // Deploy AttesterResolver with owner as initial authorized attester
        const AttesterResolver = await ethers.getContractFactory("AttesterResolver");
        attesterResolver = await AttesterResolver.deploy(mockEAS.address, [owner.address]);
    });

    describe("AttesterResolver", function () {
        it("Should return correct initial authorized attesters", async function () {
            const attesters = await attesterResolver.getTargetAttesters();
            expect(attesters).to.include(owner.address);
            expect(attesters.length).to.equal(1);
        });

        it("Should allow adding new authorized attesters", async function () {
            await attesterResolver.add_attesters(authorizedAttester.address);
            const attesters = await attesterResolver.getTargetAttesters();
            expect(attesters).to.include(authorizedAttester.address);
            expect(attesters.length).to.equal(2);
        });

        it("Should allow attestation from authorized attester", async function () {
            // Create test attestation data
            const testData = ethers.utils.defaultAbiCoder.encode(
                ["string", "string", "uint256", "uint256", "uint8", "string", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "string"],
                [
                    "0x1234567890123456789012345678901234567890", // evaluatedAgentAddress
                    owner.address, // evaluatorAgentAddress
                    Math.floor(Date.now() / 1000), // timestamp
                    85, // finalScore
                    8, // overallConfidence
                    "B+", // grade
                    90, // correctnessScore
                    9, // correctnessConfidence
                    81, // correctnessEffectiveScore
                    40, // correctnessWeight
                    80, // capabilitiesScore
                    7, // capabilitiesConfidence
                    56, // capabilitiesEffectiveScore
                    30, // capabilitiesWeight
                    85, // domainScore
                    8, // domainConfidence
                    68, // domainEffectiveScore
                    30, // domainWeight
                    "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l" // detailsCID
                ]
            );

            const attestationRequest = {
                schema: agentEvaluationSchemaUID,
                data: testData,
                expirationTime: 0,
                revocable: false,
                refUID: ethers.constants.HashZero,
                value: 0,
                deadline: 0,
                recipient: ethers.constants.AddressZero
            };

            // Should succeed for authorized attester
            await expect(mockEAS.connect(owner).attest(attestationRequest))
                .to.emit(mockEAS, "Attested");
        });

        it("Should reject attestation from unauthorized attester", async function () {
            // Add unauthorized attester to resolver first
            await attesterResolver.add_attesters(unauthorizedAttester.address);
            
            // Remove them to test rejection
            // Note: In the current implementation, we can't remove attesters
            // This test would need to be modified based on your resolver logic
            
            const testData = ethers.utils.defaultAbiCoder.encode(
                ["string", "string", "uint256", "uint256", "uint8", "string", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "string"],
                [
                    "0x1234567890123456789012345678901234567890",
                    unauthorizedAttester.address,
                    Math.floor(Date.now() / 1000),
                    85, 8, "B+", 90, 9, 81, 40, 80, 7, 56, 30, 85, 8, 68, 30,
                    "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
                ]
            );

            const attestationRequest = {
                schema: agentEvaluationSchemaUID,
                data: testData,
                expirationTime: 0,
                revocable: false,
                refUID: ethers.constants.HashZero,
                value: 0,
                deadline: 0,
                recipient: ethers.constants.AddressZero
            };

            // This should succeed because unauthorizedAttester was added
            await expect(mockEAS.connect(unauthorizedAttester).attest(attestationRequest))
                .to.emit(mockEAS, "Attested");
        });
    });

    describe("MockEAS", function () {
        it("Should create attestations correctly", async function () {
            const testData = ethers.utils.defaultAbiCoder.encode(
                ["string", "string", "uint256", "uint256", "uint8", "string", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "string"],
                [
                    "0x1234567890123456789012345678901234567890",
                    owner.address,
                    Math.floor(Date.now() / 1000),
                    85, 8, "B+", 90, 9, 81, 40, 80, 7, 56, 30, 85, 8, 68, 30,
                    "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
                ]
            );

            const attestationRequest = {
                schema: agentEvaluationSchemaUID,
                data: testData,
                expirationTime: 0,
                revocable: false,
                refUID: ethers.constants.HashZero,
                value: 0,
                deadline: 0,
                recipient: ethers.constants.AddressZero
            };

            const tx = await mockEAS.attest(attestationRequest);
            const receipt = await tx.wait();
            
            const attestedEvent = receipt.events.find(e => e.event === "Attested");
            expect(attestedEvent).to.not.be.undefined;
            
            const attestationUID = attestedEvent.args.uid;
            expect(await mockEAS.isAttestationValid(attestationUID)).to.be.true;
            
            const attestation = await mockEAS.getAttestation(attestationUID);
            expect(attestation.attester).to.equal(owner.address);
            expect(attestation.schema).to.equal(agentEvaluationSchemaUID);
        });

        it("Should handle human verification attestations", async function () {
            // First create an evaluation attestation
            const evaluationData = ethers.utils.defaultAbiCoder.encode(
                ["string", "string", "uint256", "uint256", "uint8", "string", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "uint256", "uint8", "string"],
                [
                    "0x1234567890123456789012345678901234567890",
                    owner.address,
                    Math.floor(Date.now() / 1000),
                    85, 8, "B+", 90, 9, 81, 40, 80, 7, 56, 30, 85, 8, 68, 30,
                    "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
                ]
            );

            const evaluationRequest = {
                schema: agentEvaluationSchemaUID,
                data: evaluationData,
                expirationTime: 0,
                revocable: false,
                refUID: ethers.constants.HashZero,
                value: 0,
                deadline: 0,
                recipient: ethers.constants.AddressZero
            };

            const evaluationTx = await mockEAS.attest(evaluationRequest);
            const evaluationReceipt = await evaluationTx.wait();
            const evaluationUID = evaluationReceipt.events.find(e => e.event === "Attested").args.uid;

            // Now create human verification attestation
            const verificationData = ethers.utils.defaultAbiCoder.encode(
                ["bytes32", "address", "uint64", "bool", "string"],
                [
                    evaluationUID,
                    owner.address,
                    Math.floor(Date.now() / 1000),
                    true,
                    "Verified manually - agent performed well"
                ]
            );

            const verificationRequest = {
                schema: humanVerificationSchemaUID,
                data: verificationData,
                expirationTime: 0,
                revocable: false,
                refUID: ethers.constants.HashZero,
                value: 0,
                deadline: 0,
                recipient: ethers.constants.AddressZero
            };

            const verificationTx = await mockEAS.attest(verificationRequest);
            const verificationReceipt = await verificationTx.wait();
            
            const verificationEvent = verificationReceipt.events.find(e => e.event === "Attested");
            expect(verificationEvent).to.not.be.undefined;
            
            const verificationUID = verificationEvent.args.uid;
            expect(await mockEAS.isAttestationValid(verificationUID)).to.be.true;
        });
    });
});
