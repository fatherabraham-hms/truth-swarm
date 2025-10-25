#!/usr/bin/env python3
"""
Working test agent to communicate with the deployed meTTa evaluation agent
"""

import asyncio
import os
from uagents import Agent, Context, Model
from models.data_models import CryptoDetectionRequest, AgentCategorizationResponse

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create test agent
test_agent = Agent(
    name="test_agent",
    seed="test-agent-seed-for-metta-testing",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Target agent (your deployed agent)
TARGET_AGENT = "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5"

@test_agent.on_message(AgentCategorizationResponse)
async def handle_categorization_response(ctx: Context, sender: str, msg: AgentCategorizationResponse):
    """Handle the categorization response from the deployed agent"""
    print(f"\n🎉 Received categorization response from {sender}")
    print("=" * 60)
    print(f"Agent ID: {msg.agent_id}")
    print(f"Primary Category: {msg.primary_category.category_type}")
    print(f"Confidence: {msg.primary_category.confidence:.2f}")
    print(f"Keywords Matched: {len(msg.primary_category.keywords_matched)}")
    print(f"Evaluation Method: {msg.evaluation_method}")
    print(f"Processing Time: {msg.processing_time:.2f}s")
    
    if msg.secondary_categories:
        print(f"\nSecondary Categories ({len(msg.secondary_categories)}):")
        for i, cat in enumerate(msg.secondary_categories[:5], 1):  # Show top 5
            print(f"  {i}. {cat.category_type} ({cat.subcategory or 'general'}) - {cat.confidence:.2f}")
    
    if msg.extracted_features:
        print(f"\nExtracted Features:")
        print(f"  Tech Stack: {msg.extracted_features.tech_stack}")
        print(f"  Supported Chains: {msg.extracted_features.supported_chains}")
        print(f"  Protocols: {msg.extracted_features.protocols}")
        print(f"  Target Audience: {msg.extracted_features.target_audience}")
    
    if msg.crypto_details:
        print(f"\nCrypto Details:")
        print(f"  Subcategory: {msg.crypto_details.subcategory}")
        print(f"  Protocols: {msg.crypto_details.protocols_mentioned}")
        print(f"  Chains: {msg.crypto_details.chains_supported}")
        print(f"  Use Cases: {msg.crypto_details.use_cases}")
    
    print("=" * 60)
    print("✅ Agent-to-agent communication successful!")

async def send_test_request():
    """Send a test request to the deployed agent"""
    print("🧪 Working Test Agent")
    print("=" * 50)
    print(f"Test Agent Address: {test_agent.address}")
    print(f"Target Agent: {TARGET_AGENT}")
    
    # Create test request
    test_request = CryptoDetectionRequest(
        agent_id="agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
        include_features=True,
        include_crypto_details=True,
        multi_category_threshold=0.4
    )
    
    print(f"\n📤 Sending crypto detection request...")
    print(f"   Requesting analysis for: {test_request.agent_id}")
    print(f"   Include features: {test_request.include_features}")
    print(f"   Include crypto details: {test_request.include_crypto_details}")
    
    try:
        # Send message to the deployed agent
        await test_agent.send(TARGET_AGENT, test_request)
        print("✅ Message sent successfully!")
        print("🔄 Waiting for response...")
        
        # Keep the agent running to receive the response
        await test_agent.run()
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting working test agent...")
    asyncio.run(send_test_request())
