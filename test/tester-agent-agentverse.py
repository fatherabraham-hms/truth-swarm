"""
Truth Swarm Tester Agent - AgentVerse Version

Copy this entire file into AgentVerse code editor.
Set TESTER_AGENT_SEED_PHRASE in AgentVerse environment variables.

This agent allows users to request evaluations of other agents via chat.
"""

from uagents import Agent, Context, Model
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    TextContent,
)
from datetime import datetime
from uuid import uuid4
import re
import os

# Configuration
EVALUATOR_AGENT_ADDRESS = "agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4"
SEED_PHRASE = os.getenv("TESTER_AGENT_SEED_PHRASE", "")

# Create agent
agent = Agent(
    name="truthswarm_tester",
    seed=SEED_PHRASE,
    mailbox=True
)

# Message Models
class AIResponse(Model):
    text: str

# State Management
class State:
    def __init__(self):
        self.user = None
        self.target = None
        self.active = False
    
    def start(self, user: str, target: str):
        self.user = user
        self.target = target
        self.active = True
    
    def complete(self):
        self.active = False
        self.user = None
        self.target = None

state = State()

# Helper Functions
def validate_address(addr: str) -> bool:
    if not addr:
        return False
    addr = addr.strip()
    return addr.startswith("agent1") and len(addr) == 65

def extract_address(text: str) -> str:
    match = re.search(r'agent1[a-z0-9]{60}', text.lower())
    return match.group(0) if match else None

# Event Handlers
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("🧪 Truth Swarm Tester Agent Ready!")
    ctx.logger.info(f"Agent: {agent.address}")

@agent.on_message(model=ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    # Extract message text
    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    
    ctx.logger.info(f"Message from {sender}: {text[:50]}")
    
    # Extract agent address
    addr = extract_address(text)
    
    if not addr:
        response = (
            "👋 Welcome to Truth Swarm Agent Evaluator!\n\n"
            "Send me an agent address to evaluate.\n"
            "Example: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
        )
    elif not validate_address(addr):
        response = f"❌ Invalid agent address: {addr}\nMust start with 'agent1' and be 65 characters."
    else:
        # Start evaluation
        state.start(sender, addr)
        ctx.logger.info(f"Starting eval for: {addr}")
        
        # Send to evaluator with /address/ format
        await ctx.send(
            destination=EVALUATOR_AGENT_ADDRESS,
            message=ChatMessage(
                timestamp=datetime.now(),
                msg_id=uuid4(),
                content=[TextContent(type="text", text=f"/{addr}/")]
            )
        )
        
        response = (
            f"✅ Evaluation Started!\n\n"
            f"🎯 Target: {addr}\n"
            f"⏳ Please wait for updates..."
        )
    
    # Reply to user
    await ctx.send(
        destination=sender,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=response)]
        )
    )

@agent.on_message(model=AIResponse)
async def handle_update(ctx: Context, sender: str, msg: AIResponse):
    ctx.logger.info(f"Update from evaluator: {msg.text[:50]}")
    
    if not state.active or not state.user:
        ctx.logger.warning("No active evaluation")
        return
    
    # Format update
    update = f"📬 Update:\n\n{msg.text}"
    
    # Check for completion
    if "Attestation created:" in msg.text:
        match = re.search(r'0x[a-fA-F0-9]{64}', msg.text)
        if match:
            uid = match.group(0)
            update += f"\n\n🎉 Complete!\n🔗 UID: {uid}\n📊 https://sepolia.eatscan.io/attestation/{uid}"
        state.complete()
    
    # Send to user
    await ctx.send(
        destination=state.user,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=update)]
        )
    )

if __name__ == "__main__":
    agent.run()

