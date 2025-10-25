#!/usr/bin/env python3
"""
Direct handler test - directly calls your agent's message handler
"""

import asyncio
import sys
import os

# Add the agents directory to the path so we can import the agent
sys.path.append('/Users/howardsherman/truth-swarm/agents')

from meTTa_eval_agent_refactored import (
    crypto_detection_protocol, 
    CryptoDetectionRequest, 
    CryptoDetectionResponse,
    handle_crypto_detection_request
)
from uagents import Context

async def test_direct_handler():
    """Test your agent's message handler directly"""
    
    test_agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    sender_address = "agent1qtest123456789"  # Fake sender address for testing
    
    print("🧪 Direct Handler Test")
    print("=" * 50)
    print(f"Test Agent ID: {test_agent_id}")
    print(f"Sender Address: {sender_address}")
    print()
    
    try:
        # Create a mock context
        class MockContext:
            def __init__(self):
                self.logger = MockLogger()
            
            async def send(self, recipient, message):
                print(f"📤 Mock send to {recipient}: {type(message).__name__}")
                return True
        
        class MockLogger:
            def info(self, msg):
                print(f"ℹ️  {msg}")
            
            def warning(self, msg):
                print(f"⚠️  {msg}")
            
            def error(self, msg):
                print(f"❌ {msg}")
        
        # Create the request message
        request = CryptoDetectionRequest(agent_id=test_agent_id)
        
        print("📤 Calling your agent's message handler directly...")
        print(f"   Request: {request}")
        print()
        
        # Create mock context
        ctx = MockContext()
        
        # Call your agent's handler directly
        await handle_crypto_detection_request(ctx, sender_address, request)
        
        print("✅ Handler test completed!")
        print("   This simulates what would happen when an agent sends a message to yours")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_direct_handler())
