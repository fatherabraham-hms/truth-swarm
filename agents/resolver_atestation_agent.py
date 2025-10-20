"""
Resolver Attestation Agent

This agent handles test attestation using the AttesterResolver smart contract.
It processes test data, validates it, and creates attestations through the EAS system.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import aiohttp
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EvaluationScore:
    """Structure for agent evaluation score data that will be attested"""
    evaluatedAgentAddress: str
    evaluatorAgentAddress: str
    timestamp: int
    finalScore: int
    overallConfidence: int
    grade: str
    correctnessScore: int
    correctnessConfidence: int
    correctnessEffectiveScore: int
    correctnessWeight: int
    capabilitiesScore: int
    capabilitiesConfidence: int
    capabilitiesEffectiveScore: int
    capabilitiesWeight: int
    domainScore: int
    domainConfidence: int
    domainEffectiveScore: int
    domainWeight: int
    detailsCID: str

@dataclass
class HumanVerificationData:
    """Structure for human verification data"""
    originalAttestationUID: str
    verifier: str
    timestamp: int
    approved: bool
    comment: str

@dataclass
class AttestationRequest:
    """Structure for attestation requests"""
    schema_uid: str
    recipient: str
    expiration_time: Optional[int]
    revocable: bool
    ref_uid: Optional[str]
    data: bytes
    value: int

class ResolverAttestationAgent:
    """
    Agent that handles agent evaluation attestation using the AttesterResolver contract.
    
    This agent:
    1. Processes evaluation score data and validates it
    2. Interacts with the AttesterResolver contract
    3. Creates attestations through EAS using the project schema
    4. Manages attestation lifecycle
    5. Supports human verification attestations
    """
    
    # Schema UIDs from the project
    AGENT_EVALUATION_SCHEMA_UID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc"
    HUMAN_VERIFICATION_SCHEMA_UID = "0x35bf5bfce7eaa219f46c086d4d60bfe96affaa42a0d2ae1abf17057e6607007d"
    
    def __init__(self, 
                 rpc_url: str,
                 eas_contract_address: str,
                 resolver_contract_address: str,
                 private_key: str,
                 chain_id: int = 11155111):  # Default to Sepolia
        """
        Initialize the Resolver Attestation Agent
        
        Args:
            rpc_url: Ethereum RPC endpoint
            eas_contract_address: EAS contract address
            resolver_contract_address: AttesterResolver contract address
            private_key: Private key for signing transactions
            chain_id: Ethereum chain ID
        """
        self.rpc_url = rpc_url
        self.eas_contract_address = eas_contract_address
        self.resolver_contract_address = resolver_contract_address
        self.chain_id = chain_id
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        # Set up account
        self.account = self.w3.eth.account.from_key(private_key)
        self.address = self.account.address
        
        # Contract ABIs - updated to match project contracts
        self.eas_abi = self._get_eas_abi()
        self.resolver_abi = self._get_resolver_abi()
        
        # Initialize contracts
        self.eas_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(eas_contract_address),
            abi=self.eas_abi
        )
        self.resolver_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(resolver_contract_address),
            abi=self.resolver_abi
        )
        
        logger.info(f"Resolver Attestation Agent initialized for address: {self.address}")
    
    def _get_eas_abi(self) -> List[Dict]:
        """Get EAS contract ABI - includes attest function and Attested event"""
        return [
            {
                "inputs": [
                    {"name": "request", "type": "tuple", "components": [
                        {"name": "schema", "type": "bytes32"},
                        {"name": "data", "type": "bytes"},
                        {"name": "expirationTime", "type": "uint64"},
                        {"name": "revocable", "type": "bool"},
                        {"name": "refUID", "type": "bytes32"},
                        {"name": "value", "type": "uint256"},
                        {"name": "deadline", "type": "uint64"},
                        {"name": "recipient", "type": "address"}
                    ]}
                ],
                "name": "attest",
                "outputs": [{"name": "", "type": "bytes32"}],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "uid", "type": "bytes32"},
                    {"indexed": True, "name": "schema", "type": "bytes32"},
                    {"indexed": True, "name": "attester", "type": "address"},
                    {"indexed": False, "name": "recipient", "type": "address"},
                    {"indexed": False, "name": "expirationTime", "type": "uint64"},
                    {"indexed": False, "name": "revocable", "type": "bool"},
                    {"indexed": False, "name": "refUID", "type": "bytes32"},
                    {"indexed": False, "name": "data", "type": "bytes"},
                    {"indexed": False, "name": "value", "type": "uint256"}
                ],
                "name": "Attested",
                "type": "event"
            },
            {
                "inputs": [{"name": "uid", "type": "bytes32"}],
                "name": "isAttestationValid",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "uid", "type": "bytes32"}],
                "name": "getAttestation",
                "outputs": [{"name": "", "type": "tuple", "components": [
                    {"name": "uid", "type": "bytes32"},
                    {"name": "schema", "type": "bytes32"},
                    {"name": "time", "type": "uint64"},
                    {"name": "expirationTime", "type": "uint64"},
                    {"name": "revocationTime", "type": "uint64"},
                    {"name": "refUID", "type": "bytes32"},
                    {"name": "recipient", "type": "address"},
                    {"name": "attester", "type": "address"},
                    {"name": "revocable", "type": "bool"},
                    {"name": "data", "type": "bytes"}
                ]}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def _get_resolver_abi(self) -> List[Dict]:
        """Get AttesterResolver contract ABI"""
        return [
            {
                "inputs": [],
                "name": "getTargetAttesters",
                "outputs": [{"name": "", "type": "address[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "new_attester", "type": "address"}],
                "name": "add_attesters",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
    
    async def process_evaluation_data(self, evaluation_data: EvaluationScore) -> bool:
        """
        Process and validate evaluation score data before attestation
        
        Args:
            evaluation_data: Evaluation score data to process
            
        Returns:
            bool: True if evaluation data is valid for attestation
        """
        try:
            logger.info(f"Processing evaluation data for agent: {evaluation_data.evaluatedAgentAddress}")
            
            # Validate evaluation data
            if not self._validate_evaluation_data(evaluation_data):
                logger.error(f"Invalid evaluation data for agent: {evaluation_data.evaluatedAgentAddress}")
                return False
            
            # Check if attester is authorized
            if not await self._is_authorized_attester():
                logger.error(f"Address {self.address} is not authorized to attest")
                return False
            
            logger.info(f"Evaluation data validation successful for agent: {evaluation_data.evaluatedAgentAddress}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing evaluation data: {str(e)}")
            return False
    
    def _validate_evaluation_data(self, evaluation_data: EvaluationScore) -> bool:
        """Validate evaluation score data structure and content"""
        try:
            # Check required fields
            if not evaluation_data.evaluatedAgentAddress or not evaluation_data.evaluatorAgentAddress:
                return False
            
            # Validate addresses are valid Ethereum addresses
            if not self.w3.is_address(evaluation_data.evaluatedAgentAddress):
                return False
            if not self.w3.is_address(evaluation_data.evaluatorAgentAddress):
                return False
            
            # Validate scores are within valid ranges (0-100)
            scores = [
                evaluation_data.finalScore,
                evaluation_data.correctnessScore,
                evaluation_data.correctnessEffectiveScore,
                evaluation_data.capabilitiesScore,
                evaluation_data.capabilitiesEffectiveScore,
                evaluation_data.domainScore,
                evaluation_data.domainEffectiveScore
            ]
            
            for score in scores:
                if score < 0 or score > 100:
                    return False
            
            # Validate confidence levels (0-10)
            confidences = [
                evaluation_data.overallConfidence,
                evaluation_data.correctnessConfidence,
                evaluation_data.capabilitiesConfidence,
                evaluation_data.domainConfidence
            ]
            
            for confidence in confidences:
                if confidence < 0 or confidence > 10:
                    return False
            
            # Validate weights sum to 100
            total_weight = (evaluation_data.correctnessWeight + 
                          evaluation_data.capabilitiesWeight + 
                          evaluation_data.domainWeight)
            if total_weight != 100:
                logger.warning(f"Total weights ({total_weight}) do not sum to 100")
            
            # Validate grade is not empty
            if not evaluation_data.grade:
                return False
            
            # Validate detailsCID is not empty
            if not evaluation_data.detailsCID:
                return False
            
            # Validate timestamp is recent (within last 7 days)
            current_time = int(datetime.now().timestamp())
            if evaluation_data.timestamp > current_time or (current_time - evaluation_data.timestamp) > 604800:  # 7 days
                logger.warning(f"Evaluation timestamp is older than 7 days or in the future")
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating evaluation data: {str(e)}")
            return False
    
    async def _is_authorized_attester(self) -> bool:
        """Check if the current address is authorized to attest"""
        try:
            target_attesters = self.resolver_contract.functions.getTargetAttesters().call()
            return self.address.lower() in [addr.lower() for addr in target_attesters]
        except Exception as e:
            logger.error(f"Error checking authorized attesters: {str(e)}")
            return False
    
    async def create_evaluation_attestation(self, 
                                           evaluation_data: EvaluationScore, 
                                           recipient: Optional[str] = None) -> Optional[str]:
        """
        Create an attestation for the evaluation score data
        
        Args:
            evaluation_data: Evaluation score data to attest
            recipient: Optional recipient address
            
        Returns:
            Optional[str]: Attestation UID if successful, None otherwise
        """
        try:
            logger.info(f"Creating evaluation attestation for agent: {evaluation_data.evaluatedAgentAddress}")
            
            # Prepare attestation data using the project schema
            attestation_data = self._prepare_evaluation_attestation_data(evaluation_data)
            
            # Create attestation request
            attestation_request = AttestationRequest(
                schema_uid=self.AGENT_EVALUATION_SCHEMA_UID,
                recipient=recipient or "0x0000000000000000000000000000000000000000",
                expiration_time=None,  # No expiration
                revocable=False,  # Non-revocable as per project schema
                ref_uid=None,
                data=attestation_data,
                value=0
            )
            
            # Submit attestation
            attestation_uid = await self._submit_attestation(attestation_request)
            
            if attestation_uid:
                logger.info(f"Evaluation attestation created successfully: {attestation_uid}")
                return attestation_uid
            else:
                logger.error("Failed to create evaluation attestation")
                return None
                
        except Exception as e:
            logger.error(f"Error creating evaluation attestation: {str(e)}")
            return None
    
    def _prepare_evaluation_attestation_data(self, evaluation_data: EvaluationScore) -> bytes:
        """Prepare evaluation score data for attestation encoding using the project schema"""
        # Encode according to the project schema: 
        # string evaluatedAgentAddress, string evaluatorAgentAddress, uint256 timestamp, 
        # uint256 finalScore, uint8 overallConfidence, string grade, uint256 correctnessScore, 
        # uint8 correctnessConfidence, uint256 correctnessEffectiveScore, uint8 correctnessWeight, 
        # uint256 capabilitiesScore, uint8 capabilitiesConfidence, uint256 capabilitiesEffectiveScore, 
        # uint8 capabilitiesWeight, uint256 domainScore, uint8 domainConfidence, 
        # uint256 domainEffectiveScore, uint8 domainWeight, string detailsCID
        
        from eth_abi import encode
        
        # Prepare values in the exact order of the schema
        values = [
            evaluation_data.evaluatedAgentAddress,
            evaluation_data.evaluatorAgentAddress,
            evaluation_data.timestamp,
            evaluation_data.finalScore,
            evaluation_data.overallConfidence,
            evaluation_data.grade,
            evaluation_data.correctnessScore,
            evaluation_data.correctnessConfidence,
            evaluation_data.correctnessEffectiveScore,
            evaluation_data.correctnessWeight,
            evaluation_data.capabilitiesScore,
            evaluation_data.capabilitiesConfidence,
            evaluation_data.capabilitiesEffectiveScore,
            evaluation_data.capabilitiesWeight,
            evaluation_data.domainScore,
            evaluation_data.domainConfidence,
            evaluation_data.domainEffectiveScore,
            evaluation_data.domainWeight,
            evaluation_data.detailsCID
        ]
        
        # Define types in the exact order of the schema
        types = [
            'string', 'string', 'uint256', 'uint256', 'uint8', 'string',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8', 'string'
        ]
        
        # Encode the data
        encoded_data = encode(types, values)
        return encoded_data
    
    async def _submit_attestation(self, request: AttestationRequest) -> Optional[str]:
        """Submit attestation to EAS contract"""
        try:
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.address)
            
            # Prepare attestation request tuple
            attestation_request_tuple = (
                Web3.to_bytes(hexstr=request.schema_uid),
                request.data,
                request.expiration_time or 0,
                request.revocable,
                Web3.to_bytes(hexstr=request.ref_uid) if request.ref_uid else b'\x00' * 32,
                request.value,
                0,  # deadline
                Web3.to_checksum_address(request.recipient)
            )
            
            # Build transaction
            transaction = self.eas_contract.functions.attest(attestation_request_tuple).build_transaction({
                'from': self.address,
                'gas': 1000000,  # Increased gas limit
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': self.chain_id
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                # Extract attestation UID from logs
                logs = self.eas_contract.events.Attested().process_receipt(receipt)
                if logs:
                    return logs[0]['args']['uid'].hex()
            
            return None
            
        except Exception as e:
            logger.error(f"Error submitting attestation: {str(e)}")
            return None
    
    async def add_authorized_attester(self, new_attester: str) -> bool:
        """
        Add a new authorized attester to the resolver contract
        
        Args:
            new_attester: Address of the new attester
            
        Returns:
            bool: True if successful
        """
        try:
            logger.info(f"Adding authorized attester: {new_attester}")
            
            nonce = self.w3.eth.get_transaction_count(self.address)
            
            transaction = self.resolver_contract.functions.add_attesters(
                Web3.to_checksum_address(new_attester)
            ).build_transaction({
                'from': self.address,
                'gas': 200000,  # Increased gas limit
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': self.chain_id
            })
            
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                logger.info(f"Successfully added authorized attester: {new_attester}")
                return True
            else:
                logger.error(f"Failed to add authorized attester: {new_attester}")
                return False
                
        except Exception as e:
            logger.error(f"Error adding authorized attester: {str(e)}")
            return False
    
    async def get_authorized_attesters(self) -> List[str]:
        """Get list of authorized attesters from the resolver contract"""
        try:
            attesters = self.resolver_contract.functions.getTargetAttesters().call()
            return [Web3.to_checksum_address(addr) for addr in attesters]
        except Exception as e:
            logger.error(f"Error getting authorized attesters: {str(e)}")
            return []
    
    async def create_human_verification_attestation(self, 
                                                   verification_data: HumanVerificationData) -> Optional[str]:
        """
        Create a human verification attestation
        
        Args:
            verification_data: Human verification data
            
        Returns:
            Optional[str]: Attestation UID if successful, None otherwise
        """
        try:
            logger.info(f"Creating human verification attestation for original UID: {verification_data.originalAttestationUID}")
            
            # Prepare attestation data for human verification schema
            attestation_data = self._prepare_human_verification_data(verification_data)
            
            # Create attestation request
            attestation_request = AttestationRequest(
                schema_uid=self.HUMAN_VERIFICATION_SCHEMA_UID,
                recipient="0x0000000000000000000000000000000000000000",  # No recipient for human attestations
                expiration_time=None,  # No expiration
                revocable=False,  # Non-revocable as per project schema
                ref_uid=None,
                data=attestation_data,
                value=0
            )
            
            # Submit attestation
            attestation_uid = await self._submit_attestation(attestation_request)
            
            if attestation_uid:
                logger.info(f"Human verification attestation created successfully: {attestation_uid}")
                return attestation_uid
            else:
                logger.error("Failed to create human verification attestation")
                return None
                
        except Exception as e:
            logger.error(f"Error creating human verification attestation: {str(e)}")
            return None
    
    def _prepare_human_verification_data(self, verification_data: HumanVerificationData) -> bytes:
        """Prepare human verification data for attestation encoding"""
        from eth_abi import encode
        
        # Schema: (bytes32 originalAttestationUID, address verifier, uint64 timestamp, bool approved, string comment)
        values = [
            bytes.fromhex(verification_data.originalAttestationUID[2:]),  # Convert hex string to bytes32
            verification_data.verifier,
            verification_data.timestamp,
            verification_data.approved,
            verification_data.comment
        ]
        
        types = ['bytes32', 'address', 'uint64', 'bool', 'string']
        
        # Encode the data
        encoded_data = encode(types, values)
        return encoded_data
    
    async def batch_attest_evaluations(self, 
                                     evaluation_data_list: List[EvaluationScore]) -> Dict[str, str]:
        """
        Process multiple evaluation attestations in batch
        
        Args:
            evaluation_data_list: List of evaluation data to attest
            
        Returns:
            Dict[str, str]: Mapping of evaluatedAgentAddress to attestation_uid
        """
        results = {}
        
        logger.info(f"Processing batch attestation for {len(evaluation_data_list)} evaluations")
        
        for evaluation_data in evaluation_data_list:
            try:
                # Process evaluation data
                if await self.process_evaluation_data(evaluation_data):
                    # Create attestation
                    attestation_uid = await self.create_evaluation_attestation(evaluation_data)
                    if attestation_uid:
                        results[evaluation_data.evaluatedAgentAddress] = attestation_uid
                    else:
                        logger.error(f"Failed to create attestation for agent: {evaluation_data.evaluatedAgentAddress}")
                else:
                    logger.error(f"Failed to process evaluation data for agent: {evaluation_data.evaluatedAgentAddress}")
                    
            except Exception as e:
                logger.error(f"Error processing agent {evaluation_data.evaluatedAgentAddress}: {str(e)}")
        
        logger.info(f"Batch attestation completed. {len(results)}/{len(evaluation_data_list)} successful")
        return results

# Example usage and testing
async def main():
    """Example usage of the Resolver Attestation Agent"""
    
    # Configuration (replace with actual values)
    config = {
        "rpc_url": "https://sepolia.infura.io/v3/YOUR_PROJECT_ID",
        "eas_contract_address": "0xC2679fBD37d54388Ce493F1DB75320D236e1815e",  # Sepolia EAS
        "resolver_contract_address": "YOUR_RESOLVER_CONTRACT_ADDRESS",
        "private_key": "YOUR_PRIVATE_KEY",
        "chain_id": 11155111  # Sepolia
    }
    
    # Initialize agent
    agent = ResolverAttestationAgent(
        rpc_url=config["rpc_url"],
        eas_contract_address=config["eas_contract_address"],
        resolver_contract_address=config["resolver_contract_address"],
        private_key=config["private_key"],
        chain_id=config["chain_id"]
    )
    
    # Example evaluation score data
    evaluation_data = EvaluationScore(
        evaluatedAgentAddress="0x1234567890123456789012345678901234567890",
        evaluatorAgentAddress=agent.address,
        timestamp=int(datetime.now().timestamp()),
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
    
    # Process evaluation attestation
    if await agent.process_evaluation_data(evaluation_data):
        attestation_uid = await agent.create_evaluation_attestation(evaluation_data)
        if attestation_uid:
            print(f"Evaluation attestation created: {attestation_uid}")
            
            # Example human verification
            verification_data = HumanVerificationData(
                originalAttestationUID=attestation_uid,
                verifier=agent.address,
                timestamp=int(datetime.now().timestamp()),
                approved=True,
                comment="Verified the evaluation manually. Agent performed well in tests."
            )
            
            human_attestation_uid = await agent.create_human_verification_attestation(verification_data)
            if human_attestation_uid:
                print(f"Human verification attestation created: {human_attestation_uid}")
            else:
                print("Failed to create human verification attestation")
        else:
            print("Failed to create evaluation attestation")
    else:
        print("Evaluation data validation failed")

if __name__ == "__main__":
    asyncio.run(main())
