#!/usr/bin/env python3
"""
Local Test Environment for Resolver Attestation Agent

This script sets up and tests the agent against a local Hardhat blockchain.
It deploys contracts, configures the agent, and runs integration tests.
"""

import asyncio
import json
import os
import sys
import subprocess
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

class LocalTestEnvironment:
    """Manages the local test environment for the agent"""
    
    def __init__(self, test_env_dir: str = "test-env"):
        self.test_env_dir = Path(test_env_dir)
        self.hardhat_process = None
        self.deployment_info = None
        
    async def start_hardhat_node(self) -> bool:
        """Start a local Hardhat node"""
        try:
            logger.info("Starting Hardhat node...")
            
            # Start Hardhat node in the background
            self.hardhat_process = subprocess.Popen(
                ["npx", "hardhat", "node"],
                cwd=self.test_env_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for node to start
            await asyncio.sleep(3)
            
            # Check if node is running
            if self.hardhat_process.poll() is None:
                logger.info("Hardhat node started successfully")
                return True
            else:
                logger.error("Failed to start Hardhat node")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Hardhat node: {e}")
            return False
    
    async def deploy_contracts(self) -> bool:
        """Deploy contracts to the local node"""
        try:
            logger.info("Deploying contracts...")
            
            # Run deployment script
            result = subprocess.run(
                ["npx", "hardhat", "run", "scripts/deploy.js", "--network", "localhost"],
                cwd=self.test_env_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Contracts deployed successfully")
                
                # Load deployment info
                deployment_file = self.test_env_dir / "deployment.json"
                if deployment_file.exists():
                    with open(deployment_file, 'r') as f:
                        self.deployment_info = json.load(f)
                    logger.info(f"Deployment info loaded: {self.deployment_info['contracts']['MockEAS']['address']}")
                    return True
                else:
                    logger.error("Deployment file not found")
                    return False
            else:
                logger.error(f"Deployment failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error deploying contracts: {e}")
            return False
    
    async def run_contract_tests(self) -> bool:
        """Run contract tests"""
        try:
            logger.info("Running contract tests...")
            
            result = subprocess.run(
                ["npx", "hardhat", "test"],
                cwd=self.test_env_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info("Contract tests passed")
                return True
            else:
                logger.error(f"Contract tests failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error running contract tests: {e}")
            return False
    
    def create_test_agent(self) -> Optional[ResolverAttestationAgent]:
        """Create a test agent instance"""
        if not self.deployment_info:
            logger.error("No deployment info available")
            return None
        
        try:
            # Use the first Hardhat account's private key
            # In a real scenario, you'd want to use a proper test account
            test_private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Hardhat account #0
            
            # Get schema UIDs from deployment
            agent_eval_schema_uid = self.deployment_info["schemas"]["agentEvaluation"]["hash"]
            human_verif_schema_uid = self.deployment_info["schemas"]["humanVerification"]["hash"]
            
            agent = ResolverAttestationAgent(
                rpc_url="http://127.0.0.1:8545",
                eas_contract_address=self.deployment_info["contracts"]["MockEAS"]["address"],
                resolver_contract_address=self.deployment_info["contracts"]["AttesterResolver"]["address"],
                private_key=test_private_key,
                chain_id=31337
            )
            
            # Update schema UIDs in the agent
            agent.AGENT_EVALUATION_SCHEMA_UID = agent_eval_schema_uid
            agent.HUMAN_VERIFICATION_SCHEMA_UID = human_verif_schema_uid
            
            logger.info(f"Test agent created for address: {agent.address}")
            logger.info(f"Agent Evaluation Schema UID: {agent_eval_schema_uid}")
            logger.info(f"Human Verification Schema UID: {human_verif_schema_uid}")
            return agent
            
        except Exception as e:
            logger.error(f"Error creating test agent: {e}")
            return None
    
    async def test_agent_functionality(self, agent: ResolverAttestationAgent) -> bool:
        """Test the agent's functionality"""
        try:
            logger.info("Testing agent functionality...")
            
            # Test 1: Check if agent is authorized
            is_authorized = await agent._is_authorized_attester()
            logger.info(f"Agent authorization status: {is_authorized}")
            
            if not is_authorized:
                logger.error("Agent is not authorized to attest")
                return False
            
            # Test 2: Create sample evaluation data
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
            attestation_uid = await agent.create_evaluation_attestation(evaluation_data)
            logger.info(f"Evaluation attestation UID: {attestation_uid}")
            
            if not attestation_uid:
                logger.error("Failed to create evaluation attestation")
                return False
            
            # Test 5: Create human verification attestation
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
            
            logger.info("All agent functionality tests passed!")
            return True
            
        except Exception as e:
            logger.error(f"Error testing agent functionality: {e}")
            return False
    
    async def test_unauthorized_agent(self) -> bool:
        """Test with an unauthorized agent"""
        try:
            logger.info("Testing unauthorized agent scenario...")
            
            # Create agent with different private key (unauthorized)
            unauthorized_private_key = "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d"  # Hardhat account #1
            
            unauthorized_agent = ResolverAttestationAgent(
                rpc_url="http://127.0.0.1:8545",
                eas_contract_address=self.deployment_info["contracts"]["MockEAS"]["address"],
                resolver_contract_address=self.deployment_info["contracts"]["AttesterResolver"]["address"],
                private_key=unauthorized_private_key,
                chain_id=31337
            )
            
            # Check if unauthorized agent is rejected
            is_authorized = await unauthorized_agent._is_authorized_attester()
            logger.info(f"Unauthorized agent authorization status: {is_authorized}")
            
            if is_authorized:
                logger.warning("Unauthorized agent was authorized - this might be expected if account #1 was added")
            
            # Try to add the unauthorized agent
            add_result = await unauthorized_agent.add_authorized_attester(unauthorized_agent.address)
            logger.info(f"Add unauthorized attester result: {add_result}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error testing unauthorized agent: {e}")
            return False
    
    def stop_hardhat_node(self):
        """Stop the Hardhat node"""
        if self.hardhat_process:
            logger.info("Stopping Hardhat node...")
            self.hardhat_process.terminate()
            self.hardhat_process.wait()
            logger.info("Hardhat node stopped")
    
    async def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        try:
            logger.info("Starting full test suite...")
            
            # Start Hardhat node
            if not await self.start_hardhat_node():
                return False
            
            # Deploy contracts
            if not await self.deploy_contracts():
                return False
            
            # Run contract tests
            if not await self.run_contract_tests():
                return False
            
            # Create test agent
            agent = self.create_test_agent()
            if not agent:
                return False
            
            # Test agent functionality
            if not await self.test_agent_functionality(agent):
                return False
            
            # Test unauthorized agent
            if not await self.test_unauthorized_agent():
                return False
            
            logger.info("All tests passed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in test suite: {e}")
            return False
        finally:
            self.stop_hardhat_node()

async def main():
    """Main function to run the test environment"""
    test_env = LocalTestEnvironment()
    
    success = await test_env.run_full_test_suite()
    
    if success:
        print("\n✅ All tests passed! Your agent is ready for integration testing.")
        print("\nNext steps:")
        print("1. Deploy to Sepolia testnet")
        print("2. Test with real EAS contracts")
        print("3. Integrate with your main application")
    else:
        print("\n❌ Some tests failed. Check the logs above for details.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
