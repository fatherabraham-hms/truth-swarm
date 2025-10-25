#!/usr/bin/env python3
"""
HTTP-based test to communicate with the deployed meTTa evaluation agent
"""

import asyncio
import aiohttp
import json
from datetime import datetime

async def test_agent_via_http():
    """Test the deployed agent via HTTP API"""
    print("🌐 HTTP Test Agent")
    print("=" * 50)
    
    # Your deployed agent's Railway URL
    RAILWAY_URL = "https://truth-swarm-production.up.railway.app"
    
    # Test request data
    test_request = {
        "agent_id": "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
        "include_features": True,
        "include_crypto_details": True,
        "multi_category_threshold": 0.4
    }
    
    print(f"Target Agent: {test_request['agent_id']}")
    print(f"Railway URL: {RAILWAY_URL}")
    print(f"Request: {json.dumps(test_request, indent=2)}")
    
    try:
        async with aiohttp.ClientSession() as session:
            print(f"\n📤 Sending HTTP request to categorize-agent endpoint...")
            
            async with session.post(
                f"{RAILWAY_URL}/categorize-agent",
                json=test_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    print(f"\n🎉 Received successful response!")
                    print("=" * 60)
                    print(f"Agent ID: {result['agent_id']}")
                    print(f"Primary Category: {result['primary_category']['category_type']}")
                    print(f"Confidence: {result['primary_category']['confidence']:.2f}")
                    print(f"Keywords Matched: {len(result['primary_category']['keywords_matched'])}")
                    print(f"Evaluation Method: {result['evaluation_method']}")
                    print(f"Processing Time: {result['processing_time']:.2f}s")
                    
                    if result['secondary_categories']:
                        print(f"\nSecondary Categories ({len(result['secondary_categories'])}):")
                        for i, cat in enumerate(result['secondary_categories'][:5], 1):  # Show top 5
                            subcat = cat.get('subcategory', 'general')
                            print(f"  {i}. {cat['category_type']} ({subcat}) - {cat['confidence']:.2f}")
                    
                    if result['extracted_features']:
                        print(f"\nExtracted Features:")
                        print(f"  Tech Stack: {result['extracted_features']['tech_stack']}")
                        print(f"  Supported Chains: {result['extracted_features']['supported_chains']}")
                        print(f"  Protocols: {result['extracted_features']['protocols']}")
                        print(f"  Target Audience: {result['extracted_features']['target_audience']}")
                    
                    if result['crypto_details']:
                        print(f"\nCrypto Details:")
                        print(f"  Subcategory: {result['crypto_details']['subcategory']}")
                        print(f"  Protocols: {result['crypto_details']['protocols_mentioned']}")
                        print(f"  Chains: {result['crypto_details']['chains_supported']}")
                        print(f"  Use Cases: {result['crypto_details']['use_cases']}")
                    
                    print("=" * 60)
                    print("✅ HTTP-based agent communication successful!")
                    
                else:
                    print(f"❌ HTTP request failed with status {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    
    except Exception as e:
        print(f"❌ Error during HTTP request: {e}")
        import traceback
        traceback.print_exc()

async def test_health_endpoint():
    """Test the health endpoint first"""
    print("🏥 Testing health endpoint...")
    
    RAILWAY_URL = "https://truth-swarm-production.up.railway.app"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{RAILWAY_URL}/health") as response:
                if response.status == 200:
                    health = await response.json()
                    print(f"✅ Agent is healthy: {health['status']}")
                    print(f"   Agent Name: {health['agent_name']}")
                    print(f"   Agent Address: {health['agent_address']}")
                    print(f"   meTTa Available: {health['metta_available']}")
                    print(f"   Agentverse Available: {health['agentverse_available']}")
                    return True
                else:
                    print(f"❌ Health check failed with status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting HTTP-based agent test...")
    
    # Test health first
    health_ok = await test_health_endpoint()
    if not health_ok:
        print("❌ Agent is not healthy, aborting test")
        return
    
    print()
    
    # Test categorization
    await test_agent_via_http()

if __name__ == "__main__":
    asyncio.run(main())
