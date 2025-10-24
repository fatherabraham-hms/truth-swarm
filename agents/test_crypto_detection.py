#!/usr/bin/env python3
"""
Test script for crypto agent detection functionality.
This script demonstrates how to test the crypto detection feature.
"""

import asyncio
import httpx
import json
from typing import Dict, Any

# Test configuration
AGENT_URL = "http://localhost:8000"

async def test_crypto_detection():
    """Test the crypto agent detection functionality"""
    print("🔍 Testing meTTa Crypto Detector...")
    print("=" * 50)
    
    # Test cases with different agent IDs
    test_cases = [
        {
            "name": "Specified Agent ID",
            "agent_id": "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
            "expected_crypto": True
        },
        {
            "name": "Crypto Trading Agent",
            "agent_id": "crypto-trading-agent-123",
            "expected_crypto": True
        },
        {
            "name": "General Purpose Agent", 
            "agent_id": "general-agent-456",
            "expected_crypto": False
        },
        {
            "name": "DeFi Protocol Agent",
            "agent_id": "defi-protocol-agent-789",
            "expected_crypto": True
        }
    ]
    
    try:
        async with httpx.AsyncClient() as client:
            # Test health endpoint first
            print("1. Checking agent health...")
            health_response = await client.get(f"{AGENT_URL}/health")
            if health_response.status_code != 200:
                print(f"❌ Agent not running. Status: {health_response.status_code}")
                return
            print("✅ Agent is running")
            
            # Test each case
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n{i+1}. Testing {test_case['name']} (ID: {test_case['agent_id']})")
                
                # Test crypto detection
                crypto_request = {
                    "agent_id": test_case["agent_id"]
                }
                
                try:
                    response = await client.post(
                        f"{AGENT_URL}/detect-crypto",
                        json=crypto_request,
                        headers={"Content-Type": "application/json"},
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   ✅ Crypto detection successful")
                        print(f"   📊 Results:")
                        print(f"      • Is Crypto Agent: {result.get('is_crypto_agent', 'Unknown')}")
                        print(f"      • Crypto Score: {result.get('crypto_score', 0):.2f}")
                        print(f"      • Confidence: {result.get('confidence', 0):.2f}")
                        print(f"      • Total Matches: {result.get('total_matches', 0)}")
                        print(f"      • Evaluation Method: {result.get('evaluation_method', 'Unknown')}")
                        
                        # Show matched keywords
                        if 'readme_matches' in result and result['readme_matches']:
                            print(f"      • README Matches: {result['readme_matches'][:5]}{'...' if len(result['readme_matches']) > 5 else ''}")
                        
                        if 'capability_matches' in result and result['capability_matches']:
                            print(f"      • Capability Matches: {result['capability_matches']}")
                        
                        if 'description_matches' in result and result['description_matches']:
                            print(f"      • Description Matches: {result['description_matches']}")
                        
                        # Check if result matches expectation
                        is_crypto = result.get('is_crypto_agent', False)
                        expected = test_case['expected_crypto']
                        if is_crypto == expected:
                            print(f"   ✅ Result matches expectation ({expected})")
                        else:
                            print(f"   ⚠️  Result doesn't match expectation (got {is_crypto}, expected {expected})")
                            
                    else:
                        print(f"   ❌ Crypto detection failed: {response.status_code}")
                        print(f"      Error: {response.text}")
                        
                except httpx.TimeoutException:
                    print(f"   ⏰ Request timed out for {test_case['agent_id']}")
                except Exception as e:
                    print(f"   ❌ Error testing {test_case['agent_id']}: {e}")
            
                    
    except httpx.ConnectError:
        print("❌ Could not connect to agent. Make sure it's running on localhost:8000")
        print("   Start the agent with: python meTTa_eval_agent.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

async def main():
    """Run crypto detection tests"""
    print("🚀 Starting meTTa Crypto Detector Tests...")
    print("This test requires the meTTa_crypto_detector to be running.")
    print("Make sure to set AGENTVERSE_API_KEY for full functionality.")
    print()
    
    await test_crypto_detection()
    
    print("\n" + "=" * 50)
    print("✅ Crypto detection tests completed!")
    print("\n💡 Note: Results may vary based on:")
    print("   • AgentVerse API availability")
    print("   • meTTa framework availability")
    print("   • Agent profile content")

if __name__ == "__main__":
    asyncio.run(main())
