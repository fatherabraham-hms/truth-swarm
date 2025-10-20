#!/usr/bin/env python3
"""
Simple Agent Test Script

This script tests the agent against the already deployed local contracts.
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Add the parent directory to the path to import the agent
sys.path.append(str(Path(__file__).parent.parent))

from agents.resolver_atestation_agent import ResolverAttestationAgent, EvaluationScore, HumanVerificationData

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_agent_with_deployed_contracts():
    """Test the agent against deployed contracts"""
    
    # Load deployment info
    deployment_file = Path("deployment.json")
    if not deployment_file.exists():
        logger.error("deployment.json not found. Please deploy contracts first.")
        return False
    
    with open(deployment_file, 'r') as f:
        deployment_info = json.load(f)
    
    logger.info("Loaded deployment info:")
    logger.info(f"MockEAS: {deployment_info['contracts']['MockEAS']['address']}")
    logger.info(f"AttesterResolver: {deployment_info['contracts']['AttesterResolver']['address']}")
    
    # Create test agent
    test_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Hardhat account #0
    
    # Get schema UIDs from deployment
    agent_eval_schema_uid = deployment_info["schemas"]["agentEvaluation"]["hash"]
    human_verif_schema_uid = deployment_info["schemas"]["humanVerification"]["hash"]
    
    agent = ResolverAttestationAgent(
        rpc_url="http://127.0.0.1:8545",
        eas_contract_address=deployment_info["contracts"]["MockEAS"]["address"],
        resolver_contract_address=deployment_info["contracts"]["AttesterResolver"]["address"],
        private_key=test_private_key,
        chain_id=31337
    )
    
    # Update schema UIDs in the agent
    agent.AGENT_EVALUATION_SCHEMA_UID = agent_eval_schema_uid
    agent.HUMAN_VERIFICATION_SCHEMA_UID = human_verif_schema_uid
    
    logger.info(f"Test agent created for address: {agent.address}")
    logger.info(f"Agent Evaluation Schema UID: {agent_eval_schema_uid}")
    logger.info(f"Human Verification Schema UID: {human_verif_schema_uid}")
    
    # Test 1: Check if agent is authorized
    logger.info("\n=== Test 1: Authorization Check ===")
    is_authorized = await agent._is_authorized_attester()
    logger.info(f"Agent authorization status: {is_authorized}")
    
    if not is_authorized:
        logger.error("Agent is not authorized to attest")
        return False
    
    # Test 2: Create sample evaluation data
    logger.info("\n=== Test 2: Evaluation Data Processing ===")
    evaluation_data = EvaluationScore(
        evaluatedAgentAddress="0x1234567890123456789012345678901234567890",
        evaluatorAgentAddress=agent.address,
        timestamp=int(time.time()),
        finalScore=85,
        overallConfidence=8,
        grade="B+",
        correctnessScore=90,
        correctnessConfidence=9,
        correctnessEffectiveScore=81,
        correctnessWeight=40,
        capabilitiesScore=80,
        capabilitiesConfidence=7,
        capabilitiesEffectiveScore=56,
        capabilitiesWeight=30,
        domainScore=85,
        domainConfidence=8,
        domainEffectiveScore=68,
        domainWeight=30,
        detailsCID="bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
    )
    
    # Test 3: Process evaluation data
    process_result = await agent.process_evaluation_data(evaluation_data)
    logger.info(f"Evaluation data processing result: {process_result}")
    
    if not process_result:
        logger.error("Failed to process evaluation data")
        return False
    
    # Test 4: Create evaluation attestation
    logger.info("\n=== Test 3: Creating Evaluation Attestation ===")
    attestation_uid = await agent.create_evaluation_attestation(evaluation_data)
    logger.info(f"Evaluation attestation UID: {attestation_uid}")
    
    if not attestation_uid:
        logger.error("Failed to create evaluation attestation")
        return False
    
    # Test 5: Create human verification attestation
    logger.info("\n=== Test 4: Creating Human Verification Attestation ===")
    verification_data = HumanVerificationData(
        originalAttestationUID=attestation_uid,
        verifier=agent.address,
        timestamp=int(time.time()),
        approved=True,
        comment="Verified manually - agent performed well in tests"
    )
    
    human_attestation_uid = await agent.create_human_verification_attestation(verification_data)
    logger.info(f"Human verification attestation UID: {human_attestation_uid}")
    
    if not human_attestation_uid:
        logger.error("Failed to create human verification attestation")
        return False
    
    # Test 6: Verify attestations exist
    logger.info("\n=== Test 5: Verifying Attestations ===")
    try:
        # Check if attestations are valid
        eas_contract = agent.w3.eth.contract(
            address=agent.eas_contract_address,
            abi=agent.eas_abi
        )
        
        eval_valid = eas_contract.functions.isAttestationValid(
            agent.w3.to_bytes(hexstr=attestation_uid)
        ).call()
        
        human_valid = eas_contract.functions.isAttestationValid(
            agent.w3.to_bytes(hexstr=human_attestation_uid)
        ).call()
        
        logger.info(f"Evaluation attestation valid: {eval_valid}")
        logger.info(f"Human verification attestation valid: {human_valid}")
        
        if not eval_valid or not human_valid:
            logger.error("Some attestations are not valid")
            return False
            
    except Exception as e:
        logger.error(f"Error verifying attestations: {e}")
        return False
    
    logger.info("\n🎉 All tests passed successfully!")
    logger.info("Your agent is working correctly with the local contracts!")
    
    return True

async def main():
    """Main function to run the agent test"""
    logger.info("🤖 Testing Resolver Attestation Agent against Local Contracts")
    logger.info("=" * 60)
    
    success = await test_agent_with_deployed_contracts()
    
    if success:
        print("\n✅ Agent test completed successfully!")
        print("\nYour agent can:")
        print("  ✓ Connect to local blockchain")
        print("  ✓ Check authorization status")
        print("  ✓ Process evaluation data")
        print("  ✓ Create evaluation attestations")
        print("  ✓ Create human verification attestations")
        print("  ✓ Verify attestation validity")
        print("\n🚀 Ready for testnet deployment!")
    else:
        print("\n❌ Agent test failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
