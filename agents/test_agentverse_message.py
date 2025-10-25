#!/usr/bin/env python3
"""
Test sending a proper message to your Agentverse agent
"""

import asyncio
from uagents import Agent, Context, Protocol
from pydantic import BaseModel

# Import the same models your agent uses
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

# Create test agent
test_agent = Agent(
    name="agentverse_test_agent",
    seed="test_seed_2024",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
    mailbox=True
)

# Create protocol for handling responses
test_protocol = Protocol(name="test_protocol", version="1.0")

@test_protocol.on_message(model=CryptoDetectionResponse)
async def handle_crypto_response(ctx: Context, sender: str, msg: CryptoDetectionResponse):
    """Handle crypto detection response"""
    print(f"📨 Received response from {sender}:")
    print(f"   Agent ID: {msg.agent_id}")
    print(f"   Is Crypto Agent: {msg.is_crypto_agent}")
    print(f"   Crypto Score: {msg.crypto_score}")
    print(f"   Confidence: {msg.confidence}")
    print(f"   Total Matches: {msg.total_matches}")
    print(f"   Processing Time: {msg.processing_time}s")
    if msg.error:
        print(f"   Error: {msg.error}")

@test_protocol.on_message(model=ErrorResponse)
async def handle_error_response(ctx: Context, sender: str, msg: ErrorResponse):
    """Handle error response"""
    print(f"❌ Received error from {sender}: {msg.error}")

# Include protocol
test_agent.include(test_protocol)

async def test_agentverse_message():
    """Test sending a message to your Agentverse agent"""
    
    target_agent = "agent1qtelh3evq6hcd3ksqkl6y7v5v87knddv2vz2reyqudknm4ztce9l5d75v8n"
    test_agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    
    print("🧪 Agentverse Message Test")
    print("=" * 40)
    print(f"Test Agent: {test_agent.address}")
    print(f"Target Agent: {target_agent}")
    print(f"Test Agent ID: {test_agent_id}")
    print()
    
    try:
        # Start the test agent
        print("🚀 Starting test agent...")
        agent_task = asyncio.create_task(test_agent.run())
        await asyncio.sleep(2)
        
        print("✅ Test agent started")
        print()
        
        # Create the request message
        request = CryptoDetectionRequest(agent_id=test_agent_id)
        
        print("📤 Sending crypto detection request...")
        print(f"   Requesting analysis for: {test_agent_id}")
        
        # Send the message using the protocol
        await test_agent.send(target_agent, request)
        
        print("✅ Message sent successfully!")
        print("   Waiting for response...")
        print()
        
        # Wait for response
        await asyncio.sleep(10)
        
        print("✅ Test completed!")
        print("   Check the output above for the response from your agent")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        try:
            agent_task.cancel()
            print("🛑 Test agent stopped")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_agentverse_message())
