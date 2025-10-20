"""
Integrated Evaluator + Attestation Agent

This agent combines agent evaluation with blockchain attestation:
1. Receives evaluation requests via REST POST or Chat Protocol
2. Evaluates agents using ASI:1 (or mock scores for demo/hackathon)
3. Creates attestations on Ethereum Attestation Service (EAS)
4. Returns attestation UID to the frontend

Usage:
  REST: POST http://localhost:8000/evaluate {"agent_address": "agent1q..."}
  Chat: Send agent address via chat protocol
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional
from dataclasses import dataclass
import random

# uAgents framework
from uagents import Agent, Context, Protocol, Model

# Chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Blockchain/EAS interaction
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_abi import encode

from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / ".env")


# ===== EVALUATION DATA STRUCTURES =====

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


# ===== UAGENTS MESSAGE MODELS =====

class EvaluationRequest(Model):
    """Request to evaluate an agent"""
    agent_address: str
    evaluation_type: str = "comprehensive"
    requester: str = ""


class EvaluationResponse(Model):
    """Response with evaluation and attestation"""
    success: bool
    agent_address: str
    attestation_uid: Optional[str] = None
    final_score: int
    grade: str
    message: str
    error: Optional[str] = None


# ===== ATTESTATION MANAGER =====

class AttestationManager:
    """Manages EAS attestations for agent evaluations"""
    
    AGENT_EVALUATION_SCHEMA_UID = "0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc"
    
    def __init__(self):
        # Load configuration from environment
        self.rpc_url = os.getenv('RPC_URL', 'https://sepolia.infura.io/v3/YOUR_PROJECT_ID')
        self.eas_contract_address = os.getenv('EAS_CONTRACT_ADDRESS', '0xC2679fBD37d54388Ce493F1DB75320D236e1815e')
        self.resolver_contract_address = os.getenv('RESOLVER_CONTRACT_ADDRESS', '')
        self.private_key = os.getenv('PRIVATE_KEY')
        self.chain_id = int(os.getenv('CHAIN_ID', '11155111'))  # Sepolia
        self.enabled = bool(self.private_key)
        
        if not self.enabled:
            print("⚠️  PRIVATE_KEY not set - attestation disabled (using mock mode)")
            return
        
        try:
            # Initialize Web3
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
            
            # Set up account
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address
            
            # Initialize EAS contract
            self.eas_contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(self.eas_contract_address),
                abi=self._get_eas_abi()
            )
            
            print(f"✅ Attestation manager initialized with address: {self.address}")
        except Exception as e:
            print(f"⚠️  Attestation manager initialization failed: {e}")
            self.enabled = False
    
    def _get_eas_abi(self):
        """Minimal EAS ABI for attestation"""
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
            }
        ]
    
    def _encode_evaluation_data(self, evaluation: EvaluationScore) -> bytes:
        """Encode evaluation score data for EAS schema"""
        types = [
            'string', 'string', 'uint256', 'uint256', 'uint8', 'string',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8',
            'uint256', 'uint8', 'uint256', 'uint8', 'uint256', 'uint8', 'string'
        ]
        
        values = [
            evaluation.evaluatedAgentAddress,
            evaluation.evaluatorAgentAddress,
            evaluation.timestamp,
            evaluation.finalScore,
            evaluation.overallConfidence,
            evaluation.grade,
            evaluation.correctnessScore,
            evaluation.correctnessConfidence,
            evaluation.correctnessEffectiveScore,
            evaluation.correctnessWeight,
            evaluation.capabilitiesScore,
            evaluation.capabilitiesConfidence,
            evaluation.capabilitiesEffectiveScore,
            evaluation.capabilitiesWeight,
            evaluation.domainScore,
            evaluation.domainConfidence,
            evaluation.domainEffectiveScore,
            evaluation.domainWeight,
            evaluation.detailsCID
        ]
        
        return encode(types, values)
    
    async def create_attestation(self, evaluation: EvaluationScore) -> Optional[str]:
        """Create attestation on EAS"""
        if not self.enabled:
            # Return mock UID for demo
            mock_uid = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
            print(f"🔧 Mock attestation UID generated: {mock_uid}")
            return mock_uid
        
        try:
            # Prepare attestation data
            attestation_data = self._encode_evaluation_data(evaluation)
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.address)
            
            attestation_request_tuple = (
                Web3.to_bytes(hexstr=self.AGENT_EVALUATION_SCHEMA_UID),
                attestation_data,
                0,  # No expiration
                False,  # Non-revocable
                b'\x00' * 32,  # No ref UID
                0,  # No value
                0,  # No deadline
                Web3.to_checksum_address("0x0000000000000000000000000000000000000000")
            )
            
            transaction = self.eas_contract.functions.attest(attestation_request_tuple).build_transaction({
                'from': self.address,
                'gas': 1000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
                'chainId': self.chain_id
            })
            
            # Sign and send
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            print(f"📤 Attestation transaction sent: {tx_hash.hex()}")
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status == 1:
                # Extract UID from event logs
                logs = self.eas_contract.events.Attested().process_receipt(receipt)
                if logs:
                    attestation_uid = logs[0]['args']['uid'].hex()
                    print(f"✅ Attestation created: {attestation_uid}")
                    return attestation_uid
                else:
                    # Fallback to tx hash if event parsing fails
                    return f"0x{tx_hash.hex()}"
            
            return None
            
        except Exception as e:
            print(f"❌ Error creating attestation: {e}")
            return None


# ===== ASI:1 EVALUATOR =====

class ASI1Evaluator:
    """Evaluates agents using ASI:1 or mock data"""
    
    def __init__(self, agent: Agent, use_mock: bool = True):
        self.agent = agent
        self.use_mock = use_mock
    
    async def evaluate_agent(self, agent_address: str, ctx: Context) -> EvaluationScore:
        """Evaluate an agent and return structured score"""
        
        if self.use_mock:
            return self._generate_mock_evaluation(agent_address, ctx)
        else:
            # Real ASI:1 evaluation (implement when needed)
            return await self._asi1_evaluation(agent_address, ctx)
    
    def _generate_mock_evaluation(self, agent_address: str, ctx: Context) -> EvaluationScore:
        """Generate realistic mock evaluation scores for demo/hackathon"""
        
        # Generate realistic scores with some variation
        correctness_score = random.randint(75, 95)
        capabilities_score = random.randint(70, 90)
        domain_score = random.randint(80, 95)
        
        # Weights (should sum to 100)
        correctness_weight = 40
        capabilities_weight = 30
        domain_weight = 30
        
        # Calculate effective scores (weighted)
        correctness_effective = (correctness_score * correctness_weight) // 100
        capabilities_effective = (capabilities_score * capabilities_weight) // 100
        domain_effective = (domain_score * domain_weight) // 100
        
        final_score = correctness_effective + capabilities_effective + domain_effective
        
        # Assign grade
        if final_score >= 90:
            grade = "A+"
        elif final_score >= 85:
            grade = "A"
        elif final_score >= 80:
            grade = "B+"
        elif final_score >= 75:
            grade = "B"
        else:
            grade = "C+"
        
        ctx.logger.info(f"📊 Generated evaluation: Score={final_score}/100, Grade={grade}")
        
        return EvaluationScore(
            evaluatedAgentAddress=agent_address,
            evaluatorAgentAddress=str(self.agent.address),
            timestamp=int(datetime.now(timezone.utc).timestamp()),
            finalScore=final_score,
            overallConfidence=8,
            grade=grade,
            correctnessScore=correctness_score,
            correctnessConfidence=8,
            correctnessEffectiveScore=correctness_effective,
            correctnessWeight=correctness_weight,
            capabilitiesScore=capabilities_score,
            capabilitiesConfidence=7,
            capabilitiesEffectiveScore=capabilities_effective,
            capabilitiesWeight=capabilities_weight,
            domainScore=domain_score,
            domainConfidence=9,
            domainEffectiveScore=domain_effective,
            domainWeight=domain_weight,
            detailsCID=f"bafkreimock{random.randint(1000, 9999)}evaluation"
        )
    
    async def _asi1_evaluation(self, agent_address: str, ctx: Context) -> EvaluationScore:
        """Real ASI:1 evaluation (placeholder for future implementation)"""
        # TODO: Implement real ASI:1 evaluation using structured output
        # This would send evaluation prompts to ASI:1 and parse responses
        ctx.logger.info("🤖 ASI:1 evaluation not yet implemented, using mock")
        return self._generate_mock_evaluation(agent_address, ctx)


# ===== AGENT SETUP =====

agent = Agent(
    name="evaluator_attestation_agent",
    seed="evaluator_attestation_unique_seed",
    port=8000,
    endpoint=["http://localhost:8000/submit"],
    mailbox=True  # Enable for Agentverse integration
)

# Initialize managers
attestation_manager = AttestationManager()
asi1_evaluator = ASI1Evaluator(agent, use_mock=True)  # Set to False for real ASI:1

# Create protocols
chat_proto = Protocol(spec=chat_protocol_spec)
eval_proto = Protocol(name="evaluation_protocol", version="1.0")


# ===== HELPER FUNCTIONS =====

def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    """Create chat message with text content"""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)


async def process_evaluation(agent_address: str, ctx: Context) -> EvaluationResponse:
    """Core evaluation + attestation logic"""
    try:
        ctx.logger.info(f"🔍 Starting evaluation for agent: {agent_address}")
        
        # Validate agent address format
        if not agent_address.startswith("agent1") or len(agent_address) != 65:
            return EvaluationResponse(
                success=False,
                agent_address=agent_address,
                attestation_uid=None,
                final_score=0,
                grade="F",
                message="Invalid agent address format",
                error="Agent address must start with 'agent1' and be 65 characters long"
            )
        
        # Step 1: Evaluate agent using ASI:1 (or mock)
        evaluation_score = await asi1_evaluator.evaluate_agent(agent_address, ctx)
        
        # Step 2: Create attestation on EAS
        ctx.logger.info("🔗 Creating attestation on EAS...")
        attestation_uid = await attestation_manager.create_attestation(evaluation_score)
        
        if attestation_uid:
            ctx.logger.info(f"✅ Evaluation complete! Attestation: {attestation_uid}")
            return EvaluationResponse(
                success=True,
                agent_address=agent_address,
                attestation_uid=attestation_uid,
                final_score=evaluation_score.finalScore,
                grade=evaluation_score.grade,
                message=f"Agent evaluated successfully! Score: {evaluation_score.finalScore}/100 ({evaluation_score.grade}). Attestation created on EAS."
            )
        else:
            ctx.logger.error("❌ Failed to create attestation")
            return EvaluationResponse(
                success=False,
                agent_address=agent_address,
                attestation_uid=None,
                final_score=evaluation_score.finalScore,
                grade=evaluation_score.grade,
                message="Evaluation completed but attestation failed",
                error="EAS attestation transaction failed"
            )
    
    except Exception as e:
        ctx.logger.error(f"❌ Evaluation failed: {e}")
        return EvaluationResponse(
            success=False,
            agent_address=agent_address,
            attestation_uid=None,
            final_score=0,
            grade="F",
            message="Evaluation failed",
            error=str(e)
        )


# ===== EVENT HANDLERS =====

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("🚀 Evaluator Attestation Agent Started!")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"📍 Agent Address: {agent.address}")
    ctx.logger.info(f"🌐 REST Endpoint: http://localhost:8000/evaluate")
    ctx.logger.info(f"💬 Chat Protocol: Enabled")
    ctx.logger.info(f"🔗 EAS Integration: {'Enabled' if attestation_manager.enabled else 'Mock Mode'}")
    ctx.logger.info(f"🤖 Evaluation Mode: {'Mock Scores' if asi1_evaluator.use_mock else 'ASI:1'}")
    ctx.logger.info("=" * 60)


@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    ctx.logger.info("🛑 Evaluator Attestation Agent shutting down...")


# ===== REST HANDLER =====

@agent.on_rest_post("/evaluate", EvaluationRequest, EvaluationResponse)
async def rest_evaluate(ctx: Context, request: EvaluationRequest) -> EvaluationResponse:
    """
    REST endpoint for frontend to request agent evaluation + attestation
    
    Example:
    curl -X POST http://localhost:8000/evaluate \
      -H "Content-Type: application/json" \
      -d '{"agent_address": "agent1q..."}'
    """
    ctx.logger.info(f"📨 REST evaluation request for: {request.agent_address}")
    return await process_evaluation(request.agent_address, ctx)


# ===== CHAT PROTOCOL HANDLERS =====

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat-based evaluation requests"""
    
    # Send acknowledgement
    await ctx.send(sender, ChatAcknowledgement(
        timestamp=datetime.now(timezone.utc),
        acknowledged_msg_id=msg.msg_id
    ))
    
    # Greet on session start
    if any(isinstance(item, StartSessionContent) for item in msg.content):
        await ctx.send(sender, create_text_chat(
            "👋 Hi! I'm the Agent Evaluator with EAS attestation.\n\n"
            "Send me an agent address (starting with 'agent1') and I'll:\n"
            "1. Evaluate the agent's capabilities\n"
            "2. Generate an evaluation score\n"
            "3. Create an attestation on Ethereum Attestation Service\n"
            "4. Return the attestation UID\n\n"
            "Try it now! 🚀",
            end_session=False
        ))
        return
    
    # Process text content
    text = msg.text()
    if not text:
        return

    ctx.logger.info(f"📨 Chat evaluation request from {sender}: {text}")
    
    # Check if text contains an agent address
    if text.startswith("agent1") and len(text) == 65:
        # Evaluate the agent
        result = await process_evaluation(text, ctx)
        
        # Format response
        if result.success:
            response_text = (
                f"✅ {result.message}\n\n"
                f"📊 Final Score: {result.final_score}/100\n"
                f"🎓 Grade: {result.grade}\n"
                f"🔗 Attestation UID: {result.attestation_uid}"
            )
        else:
            response_text = f"❌ {result.message}\n\nError: {result.error}"
        
        await ctx.send(sender, create_text_chat(response_text, end_session=True))
    else:
        await ctx.send(sender, create_text_chat(
            "❌ Invalid agent address.\n\n"
            "Please provide a valid agent address that:\n"
            "• Starts with 'agent1'\n"
            "• Is exactly 65 characters long\n\n"
            "Example: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y",
            end_session=True
        ))


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle chat acknowledgements"""
    pass


# ===== PROTOCOL MESSAGE HANDLER =====

@eval_proto.on_message(model=EvaluationRequest, replies=EvaluationResponse)
async def handle_eval_request(ctx: Context, sender: str, msg: EvaluationRequest):
    """Handle direct protocol-based evaluation requests from other agents"""
    ctx.logger.info(f"📨 Protocol evaluation request from {sender} for: {msg.agent_address}")
    
    result = await process_evaluation(msg.agent_address, ctx)
    await ctx.send(sender, result)


# ===== ATTACH PROTOCOLS =====

agent.include(chat_proto, publish_manifest=True)
agent.include(eval_proto, publish_manifest=True)


# ===== MAIN =====

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║         🤖 Evaluator Attestation Agent for Truth Swarm           ║
╚══════════════════════════════════════════════════════════════════╝

This agent combines AI-powered agent evaluation with blockchain attestation:

✅ Evaluate Agents - Score agents on correctness, capabilities, and domain knowledge
✅ EAS Attestation - Create immutable attestations on Ethereum Attestation Service
✅ REST API - Accept evaluation requests from frontend applications
✅ Chat Protocol - Interactive evaluation via uAgents chat protocol

📋 REST Endpoint:
   POST http://localhost:8000/evaluate
   Body: {"agent_address": "agent1q..."}
   
   Example:
   curl -X POST http://localhost:8000/evaluate \\
     -H "Content-Type: application/json" \\
     -d '{"agent_address": "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"}'

💬 Chat Protocol:
   Send an agent address via chat to trigger evaluation

🔧 Configuration:
   • Create .env file in project root with EAS credentials
   • Mock mode enabled if PRIVATE_KEY not set (perfect for testing!)
   • See README for full configuration options

🛑 Stop with Ctrl+C
    """)
    agent.run()
    