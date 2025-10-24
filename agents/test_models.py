#!/usr/bin/env python3
"""
Test script to verify Pydantic models work correctly
"""

import sys
import os

# Add the agents directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.data_models import CryptoDetectionRequest, CryptoDetectionResponse
from pydantic import BaseModel

print("Testing Pydantic models...")

# Test CryptoDetectionRequest
try:
    request = CryptoDetectionRequest(agent_id="test-agent-123")
    print(f"✅ CryptoDetectionRequest created: {request}")
    print(f"   Type: {type(request)}")
    print(f"   Is BaseModel: {isinstance(request, BaseModel)}")
except Exception as e:
    print(f"❌ CryptoDetectionRequest failed: {e}")

# Test CryptoDetectionResponse
try:
    response = CryptoDetectionResponse(
        agent_id="test-agent-123",
        is_crypto_agent=True,
        crypto_score=0.8,
        confidence=0.9,
        total_matches=5,
        evaluation_method="test",
        processing_time=1.5
    )
    print(f"✅ CryptoDetectionResponse created: {response}")
    print(f"   Type: {type(response)}")
    print(f"   Is BaseModel: {isinstance(response, BaseModel)}")
except Exception as e:
    print(f"❌ CryptoDetectionResponse failed: {e}")

print("\nTesting uAgents compatibility...")
try:
    from uagents import Agent
    agent = Agent(name="test", seed="test")
    print("✅ uAgents Agent created successfully")
except Exception as e:
    print(f"❌ uAgents Agent failed: {e}")
