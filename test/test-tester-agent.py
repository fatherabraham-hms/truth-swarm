"""
Local Test Script for Tester Agent

This script simulates a user interacting with the tester agent locally.
Use this to verify the tester agent works before deploying to AgentVerse.

Usage:
    python test-tester-agent.py
"""

from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
from datetime import datetime
from uuid import uuid4
import asyncio

# Test user agent
test_user = Agent(
    name="test_user",
    seed="test_user_seed_phrase_12345",
    port=8002
)

# Your tester agent address (will be displayed when tester-agent.py starts)
# Update this after starting tester-agent.py
TESTER_AGENT_ADDRESS = "UPDATE_WITH_TESTER_AGENT_ADDRESS"

# Test agent addresses to evaluate
TEST_AGENT_ADDRESSES = [
    "agent1q2c8sxs5kg902j96ffruh0he2erhjf63eahrypzvj20gjraevxlggy4fq33",  # DeFi agent
    "agent1qtzkq9stasjkl54js9ej604pvtcnp9l2m8s3u4mnvjcz3q4qerc5zmahxcq",  # Halloween agent
]

@test_user.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("🧪 Test User Started!")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Test User Address: {test_user.address}")
    ctx.logger.info(f"Tester Agent Address: {TESTER_AGENT_ADDRESS}")
    
    if TESTER_AGENT_ADDRESS == "UPDATE_WITH_TESTER_AGENT_ADDRESS":
        ctx.logger.error("❌ Please update TESTER_AGENT_ADDRESS in this script!")
        ctx.logger.error("   1. Start tester-agent.py in another terminal")
        ctx.logger.error("   2. Copy the agent address from the output")
        ctx.logger.error("   3. Update TESTER_AGENT_ADDRESS in this script")
        return
    
    ctx.logger.info("=" * 60)
    ctx.logger.info("Waiting 3 seconds before sending test message...")
    await asyncio.sleep(3)
    
    # Test 1: Send greeting (should get welcome message)
    ctx.logger.info("\n📤 TEST 1: Sending greeting...")
    await ctx.send(
        destination=TESTER_AGENT_ADDRESS,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text="Hello! Can you help me?")]
        )
    )
    
    # Wait for response
    await asyncio.sleep(5)
    
    # Test 2: Send valid agent address
    test_address = TEST_AGENT_ADDRESSES[0]
    ctx.logger.info(f"\n📤 TEST 2: Sending agent address: {test_address}")
    await ctx.send(
        destination=TESTER_AGENT_ADDRESS,
        message=ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[TextContent(type="text", text=f"Please evaluate {test_address}")]
        )
    )
    
    ctx.logger.info("\n⏳ Waiting for evaluation updates...")
    ctx.logger.info("   (This may take 30-60 seconds)")

@test_user.on_message(model=ChatMessage)
async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
    # Extract text from response
    text = ""
    for item in msg.content:
        if isinstance(item, TextContent):
            text += item.text
    
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"📬 RECEIVED RESPONSE from {sender}:")
    ctx.logger.info("=" * 60)
    ctx.logger.info(text)
    ctx.logger.info("=" * 60)

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════╗
║           🧪 Tester Agent - Local Test Script                    ║
╚══════════════════════════════════════════════════════════════════╝

This script will test your tester agent locally.

📋 Prerequisites:
   1. Start evaluator-agent.py (if testing full flow)
   2. Start tester-agent.py in another terminal
   3. Update TESTER_AGENT_ADDRESS in this script

🔍 What this script does:
   1. Sends a greeting message (should get welcome response)
   2. Sends a valid agent address for evaluation
   3. Displays all responses from the tester agent

⚠️  IMPORTANT: Update TESTER_AGENT_ADDRESS before running!
   Look for the address in tester-agent.py output.

Press Ctrl+C to stop.
    """)
    
    test_user.run()

