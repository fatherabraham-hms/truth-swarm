#!/usr/bin/env python3
"""
Quick test to send a message to your Agentverse agent
"""

import asyncio
from uagents import Agent, Context
from uagents.protocol import Protocol
from pydantic import BaseModel

# Simple message model
class SimpleMessage(BaseModel):
    content: str

# Create a simple test agent
test_agent = Agent(
    name="quick_test_agent",
    seed="quick_test_seed_2024",
    port=8003,
    endpoint=["http://localhost:8003/submit"],
    mailbox=True
)

async def quick_test():
    """Quick test of agent communication"""
    
    target_agent = "agent1qtelh3evq6hcd3ksqkl6y7v5v87knddv2vz2reyqudknm4ztce9l5d75v8n"
    test_content = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    
    print("🧪 Quick Agent Communication Test")
    print("=" * 40)
    print(f"Test Agent: {test_agent.address}")
    print(f"Target Agent: {target_agent}")
    print(f"Message: {test_content}")
    print()
    
    try:
        # Create a simple message
        message = SimpleMessage(content=test_content)
        
        # Send message directly from agent
        print("📤 Sending message...")
        await test_agent.send(target_agent, message)
        
        print("✅ Message sent successfully!")
        print("   Check your agent's logs to see if it received the message")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   This might be because:")
        print("   - The target agent is not running")
        print("   - Network connectivity issues")
        print("   - Agent addresses are incorrect")

if __name__ == "__main__":
    asyncio.run(quick_test())
