#!/usr/bin/env python3
"""
Test agent that sends messages to your Agentverse agent
"""

import asyncio
from uagents import Agent, Context, Protocol
from uagents.protocol import Protocol
from pydantic import BaseModel

# Message model for testing
class TestMessage(BaseModel):
    content: str
    test_type: str = "categorization_request"

# Create the test agent
test_agent = Agent(
    name="test_agent_communication",
    seed="test_agent_seed_2024",
    port=8002,  # Different port to avoid conflicts
    endpoint=["http://localhost:8002/submit"],
    mailbox=True
)

# Create a protocol for sending test messages
test_protocol = Protocol(name="test_protocol", version="1.0")

@test_protocol.on_message(model=TestMessage)
async def handle_test_message(ctx: Context, sender: str, msg: TestMessage):
    """Handle incoming test messages"""
    print(f"📨 Test agent received message from {sender}:")
    print(f"   Content: {msg.content}")
    print(f"   Type: {msg.test_type}")
    
    # Send a response back
    response = TestMessage(
        content=f"Test agent received: {msg.content}",
        test_type="response"
    )
    await ctx.send(sender, response)
    print(f"📤 Sent response back to {sender}")

# Include the protocol in the test agent
test_agent.include(test_protocol)

async def test_agentverse_communication():
    """Test communication with your Agentverse agent"""
    
    # Your agent's Agentverse address
    target_agent = "agent1qtelh3evq6hcd3ksqkl6y7v5v87knddv2vz2reyqudknm4ztce9l5d75v8n"
    
    print("🧪 Test Agent Communication")
    print("=" * 50)
    print(f"Test Agent Address: {test_agent.address}")
    print(f"Target Agent: {target_agent}")
    print()
    
    try:
        # Start the test agent
        print("🚀 Starting test agent...")
        
        # Run the agent in the background
        agent_task = asyncio.create_task(test_agent.run())
        
        # Wait for agent to initialize
        await asyncio.sleep(3)
        
        print("✅ Test agent started successfully")
        print(f"   Address: {test_agent.address}")
        print()
        
        # Send test messages
        test_messages = [
            TestMessage(content="agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac", test_type="categorization_request"),
            TestMessage(content="Hello from test agent!", test_type="greeting"),
            TestMessage(content="Please categorize this agent: agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac", test_type="categorization_request")
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"📤 Sending test message {i}...")
            print(f"   Content: {message.content}")
            print(f"   Type: {message.test_type}")
            
            # Create context and send message
            ctx = Context(test_agent)
            await ctx.send(target_agent, message)
            
            print(f"✅ Message {i} sent successfully")
            
            # Wait for potential response
            await asyncio.sleep(2)
            print()
        
        print("🔍 All test messages sent!")
        print("   Check your agent's logs to see if it received the messages")
        print("   Your agent should process the categorization requests")
        
        # Keep the agent running for a bit to receive responses
        print("\n⏳ Waiting for responses...")
        await asyncio.sleep(10)
        
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Stop the test agent
        try:
            agent_task.cancel()
            print("🛑 Test agent stopped")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_agentverse_communication())
