#!/usr/bin/env python3
"""
Test script for Agentverse integration with meTTa_eval_agent
"""

import asyncio
import httpx
import json
import os
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Test configuration
BASE_URL = "http://localhost:8000"
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")

async def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data['status']}")
                print(f"   Agent: {data['agent_name']}")
                print(f"   meTTa available: {data['metta_available']}")
                print(f"   Agentverse available: {data['agentverse_available']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

async def test_list_agents():
    """Test agent listing endpoint"""
    print("\n🔍 Testing agent listing...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/list-agents",
                json={"limit": 5, "offset": 0}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent listing successful")
                print(f"   Total agents: {data['total_count']}")
                print(f"   Agentverse available: {data['agentverse_available']}")
                print(f"   Agents returned: {len(data['agents'])}")
                
                if data['agents']:
                    print("   Sample agents:")
                    for i, agent in enumerate(data['agents'][:3]):
                        print(f"     {i+1}. {agent.get('name', 'Unknown')} ({agent.get('agent_id', 'No ID')})")
                        print(f"        Description: {agent.get('description', 'No description')[:100]}...")
                        print(f"        Capabilities: {agent.get('capabilities', [])}")
                return True
            else:
                print(f"❌ Agent listing failed: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Agent listing error: {e}")
        return False

async def test_discover_agents():
    """Test agent discovery endpoint"""
    print("\n🔍 Testing agent discovery...")
    try:
        # Test with crypto search
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/discover-agents",
                json={
                    "search_term": "crypto",
                    "capabilities": ["trading", "blockchain"],
                    "limit": 3
                }
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent discovery successful")
                print(f"   Search term: '{data['search_term']}'")
                print(f"   Capabilities searched: {data['capabilities_searched']}")
                print(f"   Total found: {data['total_found']}")
                print(f"   Agentverse available: {data['agentverse_available']}")
                
                if data['matching_agents']:
                    print("   Matching agents:")
                    for i, agent in enumerate(data['matching_agents']):
                        print(f"     {i+1}. {agent.get('name', 'Unknown')} (Score: {agent.get('match_score', 0):.2f})")
                        print(f"        Description: {agent.get('description', 'No description')[:100]}...")
                        print(f"        Capabilities: {agent.get('capabilities', [])}")
                return True
            else:
                print(f"❌ Agent discovery failed: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Agent discovery error: {e}")
        return False

async def test_crypto_detection():
    """Test crypto detection endpoint"""
    print("\n🔍 Testing crypto detection...")
    try:
        # Test with a mock agent ID
        test_agent_id = "test-crypto-agent-123"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/detect-crypto",
                json={"agent_id": test_agent_id}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Crypto detection successful")
                print(f"   Agent ID: {data['agent_id']}")
                print(f"   Is crypto agent: {data['is_crypto_agent']}")
                print(f"   Crypto score: {data['crypto_score']:.2f}")
                print(f"   Confidence: {data['confidence']:.2f}")
                print(f"   Total matches: {data['total_matches']}")
                print(f"   Evaluation method: {data['evaluation_method']}")
                print(f"   Processing time: {data['processing_time']:.2f}s")
                
                if data['readme_matches']:
                    print(f"   README matches: {data['readme_matches'][:5]}...")
                if data['capability_matches']:
                    print(f"   Capability matches: {data['capability_matches']}")
                if data['description_matches']:
                    print(f"   Description matches: {data['description_matches']}")
                return True
            else:
                print(f"❌ Crypto detection failed: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Crypto detection error: {e}")
        return False

async def test_agentverse_connection():
    """Test direct Agentverse API connection"""
    print("\n🔍 Testing direct Agentverse connection...")
    if not AGENTVERSE_API_KEY:
        print("⚠️ AGENTVERSE_API_KEY not set, skipping direct API test")
        return False
    
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            headers = {"Authorization": f"Bearer {AGENTVERSE_API_KEY}"}
            response = await client.get("https://agentverse.ai/v1/hosting/agents", headers=headers)
            
            # Handle redirects
            if response.status_code in [301, 302, 307, 308]:
                redirect_location = response.headers.get("location")
                print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                return False
            
            if response.status_code == 200:
                agents = response.json()
                print(f"✅ Direct Agentverse connection successful")
                print(f"   Found {len(agents)} agents")
                if agents:
                    print("   Sample agent:")
                    agent = agents[0]
                    print(f"     Name: {agent.get('name', 'Unknown')}")
                    print(f"     Address: {agent.get('address', 'No address')}")
                    print(f"     Status: {agent.get('status', 'Unknown')}")
                return True
            else:
                print(f"❌ Direct Agentverse connection failed: {response.status_code} - {response.text[:200]}")
                return False
    except Exception as e:
        print(f"❌ Direct Agentverse connection error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Starting Agentverse integration tests...")
    print(f"📅 Test started at: {datetime.now().isoformat()}")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"🔑 Agentverse API Key: {'Set' if AGENTVERSE_API_KEY else 'Not Set'}")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health),
        ("Agent Listing", test_list_agents),
        ("Agent Discovery", test_discover_agents),
        ("Crypto Detection", test_crypto_detection),
        ("Direct Agentverse Connection", test_agentverse_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Agentverse integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        print("\n💡 Troubleshooting tips:")
        print("   1. Make sure the agent is running: python meTTa_eval_agent.py")
        print("   2. Set AGENTVERSE_API_KEY environment variable")
        print("   3. Check network connectivity to api.agentverse.ai")
        print("   4. Verify the agent is accessible at http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(main())
