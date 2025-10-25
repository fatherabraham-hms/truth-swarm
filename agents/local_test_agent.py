#!/usr/bin/env python3
"""
Local test agent that sends messages to your Agentverse agent
"""

import asyncio
from uagents import Agent, Context, Protocol
from pydantic import BaseModel

# Message models matching your agent's protocol
class CryptoDetectionRequest(BaseModel):
    agent_id: str

class CryptoDetectionResponse(BaseModel):
    agent_id: str
    is_crypto_agent: bool
    crypto_score: float
    confidence: float
    total_matches: int
    readme_matches: list
    capabilities_matches: list
    processing_time: float
    error: str = None

class ErrorResponse(BaseModel):
    error: str

# Create the test agent
test_agent = Agent(
    name="local_test_agent",
    seed="local_test_seed_2024",
    port=8005,
    endpoint=["http://localhost:8005/submit"],
    mailbox=True
)

# Create protocol for handling responses
test_protocol = Protocol(name="test_protocol", version="1.0")

@test_protocol.on_message(model=CryptoDetectionResponse)
async def handle_crypto_response(ctx: Context, sender: str, msg: CryptoDetectionResponse):
    """Handle crypto detection response"""
    print(f"\n📨 Received response from {sender}:")
    print(f"   Agent ID: {msg.agent_id}")
    print(f"   Is Crypto Agent: {msg.is_crypto_agent}")
    print(f"   Crypto Score: {msg.crypto_score}")
    print(f"   Confidence: {msg.confidence}")
    print(f"   Total Matches: {msg.total_matches}")
    print(f"   Processing Time: {msg.processing_time}s")
    if msg.error:
        print(f"   Error: {msg.error}")
    print()

@test_protocol.on_message(model=ErrorResponse)
async def handle_error_response(ctx: Context, sender: str, msg: ErrorResponse):
    """Handle error response"""
    print(f"\n❌ Received error from {sender}: {msg.error}\n")

# Include the protocol
test_agent.include(test_protocol)

async def send_test_message():
    """Send a test message to your Agentverse agent"""
    
    # Your agent's Agentverse address
    target_agent = "agent1qtelh3evq6hcd3ksqkl6y7v5v87knddv2vz2reyqudknm4ztce9l5d75v8n"
    test_agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    
    print("🧪 Local Test Agent")
    print("=" * 50)
    print(f"Test Agent Address: {test_agent.address}")
    print(f"Target Agent: {target_agent}")
    print(f"Test Agent ID: {test_agent_id}")
    print()
    
    try:
        # Create the request message
        request = CryptoDetectionRequest(agent_id=test_agent_id)
        
        print("📤 Sending crypto detection request...")
        print(f"   Requesting analysis for: {test_agent_id}")
        
        # Send the message
        await test_agent.send(target_agent, request)
        
        print("✅ Message sent successfully!")
        print("   Waiting for response...")
        print("   (Your agent should process this and send back a response)")
        print()
        
        # Keep the agent running to receive the response
        print("🔄 Test agent is running and waiting for response...")
        print("   Press Ctrl+C to stop")
        
        # Run the agent
        await test_agent.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Test agent stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(send_test_message())
