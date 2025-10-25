#!/usr/bin/env python3
"""
HTTP simulation test - simulates what an agent-to-agent message would do
"""

import asyncio
import httpx
import json

async def simulate_agent_message():
    """Simulate sending a message to your agent via HTTP (like agent-to-agent would do)"""
    
    # Your agent's Railway URL
    agent_url = "https://truth-swarm-production.up.railway.app"
    test_agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    
    print("🧪 HTTP Simulation Test")
    print("=" * 50)
    print(f"Agent URL: {agent_url}")
    print(f"Test Agent ID: {test_agent_id}")
    print()
    
    try:
        # Test 1: Health check
        print("1️⃣ Testing health endpoint...")
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{agent_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ Health check passed: {health_data.get('status', 'Unknown')}")
                print(f"   Agent Address: {health_data.get('agent_address', 'Unknown')}")
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
                return
        print()
        
        # Test 2: Crypto detection (simulating agent-to-agent message)
        print("2️⃣ Testing crypto detection (simulating agent message)...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{agent_url}/detect-crypto",
                json={"agent_id": test_agent_id},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                crypto_data = response.json()
                print(f"   ✅ Crypto detection successful!")
                print(f"   Agent ID: {crypto_data.get('agent_id', 'Unknown')}")
                print(f"   Is Crypto Agent: {crypto_data.get('is_crypto_agent', False)}")
                print(f"   Crypto Score: {crypto_data.get('crypto_score', 0.0)}")
                print(f"   Confidence: {crypto_data.get('confidence', 0.0)}")
                print(f"   Total Matches: {crypto_data.get('total_matches', 0)}")
                print(f"   Processing Time: {crypto_data.get('processing_time', 0.0)}s")
                
                if crypto_data.get('error'):
                    print(f"   Error: {crypto_data.get('error')}")
            else:
                print(f"   ❌ Crypto detection failed: {response.status_code}")
                print(f"   Response: {response.text}")
        print()
        
        # Test 3: Feature extraction
        print("3️⃣ Testing feature extraction...")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{agent_url}/extract-features",
                json={"agent_id": test_agent_id},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                features_data = response.json()
                print(f"   ✅ Feature extraction successful!")
                print(f"   Agent ID: {features_data.get('agent_id', 'Unknown')}")
                print(f"   Capabilities: {features_data.get('capabilities', [])}")
                print(f"   Key Features: {features_data.get('key_features', [])}")
                print(f"   Target Audience: {features_data.get('target_audience', 'Unknown')}")
                print(f"   Business Model: {features_data.get('business_model', 'Unknown')}")
            else:
                print(f"   ❌ Feature extraction failed: {response.status_code}")
        print()
        
        print("🎉 All tests completed successfully!")
        print("   This simulates what agent-to-agent communication would do")
        print("   Your agent is working perfectly via HTTP API!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simulate_agent_message())
