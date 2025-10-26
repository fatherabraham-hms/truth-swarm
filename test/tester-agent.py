"""
Tester Agent for Truth Swarm Evaluator

This agent allows users to request evaluations of other agents by:
1. Accepting an agent address from the user via chat
2. Sending the address to the deployed evaluator agent
3. Receiving and displaying progress updates from the evaluator
4. Showing the final attestation result

Designed for deployment on AgentVerse (ASI)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from uagents import Agent, Context, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    TextContent,
)
from datetime import datetime
from uuid import uuid4
import re

# Load environment variables (for local testing)
# On AgentVerse, these will be set in the UI
if not os.getenv("AGENTVERSE_ENVIRONMENT"):
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)

# Get seed phrase from environment (required for AgentVerse)
SEED_PHRASE = os.getenv("TESTER_AGENT_SEED_PHRASE", "tester_agent_unique_seed_phrase_here")

# Deployed evaluator agent address
EVALUATOR_AGENT_ADDRESS = "agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4"

# Create the tester agent
tester_agent = Agent(
    name="truthswarm_tester",
    seed=SEED_PHRASE,
    port=8001,
    mailbox=True,  # Required for AgentVerse
    readme_path="README.md"
)

# ===== MESSAGE MODELS =====

class UserRequest(Model):
    """User sends an agent address to evaluate"""
    agent_address: str
    
class UserResponse(Model):
    """Response back to the user"""
    message: str

class AIResponse(Model):
    """Response from evaluator agent"""
    text: str

# ===== STATE MANAGEMENT =====

class TesterState:
    """Track evaluation requests and responses"""
    def __init__(self):
        self.current_user = None
        self.current_target_agent = None
        self.evaluation_in_progress = False
        self.updates = []
    
    def start_evaluation(self, user_address: str, target_agent: str):
        self.current_user = user_address
        self.current_target_agent = target_agent
        self.evaluation_in_progress = True
        self.updates = []
    
    def add_update(self, update: str):
        self.updates.append(update)
    
    def complete_evaluation(self):
        self.evaluation_in_progress = False
        self.current_user = None
        self.current_target_agent = None

# Global state
tester_state = TesterState()

# ===== HELPER FUNCTIONS =====

def validate_agent_address(address: str) -> bool:
    """Validate agent address format"""
    # Agent addresses should start with "agent1" and be 65 characters
    if not address:
        return False
    address = address.strip()
    return address.startswith("agent1") and len(address) == 65

def extract_agent_address(text: str) -> str:
    """Extract agent address from user text"""
    # Look for agent address pattern
    match = re.search(r'agent1[a-z0-9]{60}', text.lower())
    if match:
        return match.group(0)
    return None

# ===== EVENT HANDLERS =====

@tester_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("🧪 Truth Swarm Tester Agent Started!")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"📍 Agent Address: {tester_agent.address}")
    ctx.logger.info(f"🎯 Evaluator Address: {EVALUATOR_AGENT_ADDRESS}")
    ctx.logger.info("💬 Ready to accept evaluation requests!")
    ctx.logger.info("=" * 60)

# ===== MESSAGE HANDLERS =====

@tester_agent.on_message(model=ChatMessage)
async def handle_user_chat(ctx: Context, sender: str, msg: ChatMessage):
    """
    Handle chat messages from users requesting evaluations
    Expected format: User sends agent address they want evaluated
    """
    # Extract text from ChatMessage
    user_message = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            user_message += item.text
    
    ctx.logger.info(f"💬 Received message from {sender}: {user_message[:100]}")
    
    # Try to extract agent address from message
    agent_address = extract_agent_address(user_message)
    
    if not agent_address:
        # User message doesn't contain a valid agent address
        response_text = (
            "👋 Welcome to Truth Swarm Agent Evaluator!\n\n"
            "To evaluate an agent, please send me the agent address.\n"
            "Example: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y\n\n"
            "I'll forward it to the evaluator and keep you updated on the progress!"
        )
    else:
        # Valid agent address found
        if not validate_agent_address(agent_address):
            response_text = (
                f"❌ Invalid agent address format: {agent_address}\n\n"
                "Agent addresses should start with 'agent1' and be 65 characters long."
            )
        else:
            # Start evaluation process
            tester_state.start_evaluation(sender, agent_address)
            
            ctx.logger.info(f"🚀 Starting evaluation for: {agent_address}")
            
            # Send agent address to evaluator using ChatMessage
            # The evaluator expects the address wrapped in slashes like: /agent1.../
            evaluation_request = f"/{agent_address}/"
            
            await ctx.send(
                destination=EVALUATOR_AGENT_ADDRESS,
                message=ChatMessage(
                    timestamp=datetime.now(),
                    msg_id=uuid4(),
                    content=[TextContent(type="text", text=evaluation_request)]
                )
            )
            
            response_text = (
                f"✅ Evaluation request sent!\n\n"
                f"🎯 Target Agent: {agent_address}\n"
                f"📡 Evaluator: {EVALUATOR_AGENT_ADDRESS}\n\n"
                f"⏳ Waiting for evaluation to complete...\n"
                f"I'll send you updates as they come in!"
            )
            
            tester_state.add_update(response_text)
    
    # Send response back to user
    await ctx.send(
        destination=sender,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response_text)]
        )
    )

@tester_agent.on_message(model=AIResponse)
async def handle_evaluator_response(ctx: Context, sender: str, msg: AIResponse):
    """
    Handle responses from the evaluator agent
    Forward these updates to the user who requested the evaluation
    """
    ctx.logger.info(f"📨 Received update from evaluator: {msg.text[:100]}")
    
    # Only process if we have an active evaluation
    if not tester_state.evaluation_in_progress:
        ctx.logger.warning("⚠️  Received evaluator response but no evaluation in progress")
        return
    
    if not tester_state.current_user:
        ctx.logger.warning("⚠️  No user address stored for this evaluation")
        return
    
    # Store the update
    tester_state.add_update(msg.text)
    
    # Format update message
    update_message = f"📬 Update from Evaluator:\n\n{msg.text}"
    
    # Check if this is the final attestation message
    if "Attestation created:" in msg.text:
        # Extract attestation UID if present
        attestation_match = re.search(r'0x[a-fA-F0-9]{64}', msg.text)
        if attestation_match:
            attestation_uid = attestation_match.group(0)
            update_message += f"\n\n🎉 Evaluation Complete!\n"
            update_message += f"🔗 Attestation UID: {attestation_uid}\n"
            update_message += f"📊 View on EAS: https://sepolia.eatscan.io/attestation/{attestation_uid}"
        
        # Mark evaluation as complete
        tester_state.complete_evaluation()
    
    # Send update to user
    ctx.logger.info(f"📤 Forwarding update to user: {tester_state.current_user}")
    
    await ctx.send(
        destination=tester_state.current_user,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=update_message)]
        )
    )

# ===== MAIN =====

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           🧪 Truth Swarm Tester Agent                            ║
╚══════════════════════════════════════════════════════════════════╝

This agent helps you test other agents using the Truth Swarm evaluator:

📝 How to Use:
   1. Send me an agent address via chat
   2. I'll forward it to the evaluator agent
   3. You'll receive real-time updates on the evaluation progress
   4. Get the final attestation UID when complete

💬 Example Message:
   "Please evaluate agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

🎯 Evaluator Agent: {EVALUATOR_AGENT_ADDRESS}

🚀 Starting agent...
    """.format(EVALUATOR_AGENT_ADDRESS=EVALUATOR_AGENT_ADDRESS))
    
    tester_agent.run()

