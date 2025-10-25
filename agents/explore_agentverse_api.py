#!/usr/bin/env python3
"""
Explore Agentverse API to understand the correct registration format
"""

import os
import asyncio
import httpx
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
except ImportError:
    pass

async def explore_agentverse_api():
    """Explore Agentverse API to understand registration requirements"""
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Exploring Agentverse API...")
    print("=" * 50)
    
    # Test different endpoints and methods
    endpoints_to_test = [
        ("GET", "https://agentverse.ai/v1/agents", "List agents"),
        ("GET", "https://agentverse.ai/v1/agents/", "List agents with trailing slash"),
        ("GET", "https://agentverse.ai/api/agents", "API agents endpoint"),
        ("GET", "https://agentverse.ai/agents", "Root agents endpoint"),
        ("GET", "https://agentverse.ai/v1/", "API root"),
        ("GET", "https://agentverse.ai/api/", "API root v2"),
    ]
    
    for method, url, description in endpoints_to_test:
        print(f"\n📡 Testing {method} {url}")
        print(f"   Description: {description}")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                else:
                    response = await client.post(url, headers=headers)
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   Response type: {type(data)}")
                        if isinstance(data, dict):
                            print(f"   Keys: {list(data.keys())}")
                            if 'items' in data:
                                print(f"   Items count: {len(data.get('items', []))}")
                        elif isinstance(data, list):
                            print(f"   List length: {len(data)}")
                    except:
                        print(f"   Response (first 200 chars): {response.text[:200]}")
                else:
                    print(f"   Error: {response.text[:200]}")
                    
        except Exception as e:
            print(f"   Exception: {e}")
    
    # Try to understand the challenge requirement
    print(f"\n🔍 Investigating challenge field requirement...")
    
    # Test with different challenge formats
    challenge_tests = [
        {"challenge": "test"},
        {"challenge": ""},
        {"challenge": None},
        {"challenge": "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5"},
        {"challenge": "proof_of_work"},
        {"challenge": "verification"},
    ]
    
    for i, challenge_data in enumerate(challenge_tests):
        print(f"\n   Test {i+1}: {challenge_data}")
        
        registration_data = {
            "address": "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5",
            "name": "Test Agent",
            "description": "Test agent for API exploration",
            **challenge_data
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post("https://agentverse.ai/v1/agents", 
                                           headers=headers, 
                                           json=registration_data)
                print(f"     Status: {response.status_code}")
                if response.status_code != 422:
                    print(f"     Success! Response: {response.text[:200]}")
                    break
                else:
                    error_data = response.json()
                    print(f"     Error: {error_data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"     Exception: {e}")
    
    # Check if there are any other required fields
    print(f"\n🔍 Checking for other required fields...")
    
    # Try with minimal data to see what's required
    minimal_tests = [
        {"address": "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5"},
        {"address": "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5", "challenge": "test"},
        {"name": "Test Agent", "challenge": "test"},
        {"endpoint": "https://test.com/submit", "challenge": "test"},
    ]
    
    for i, test_data in enumerate(minimal_tests):
        print(f"\n   Minimal test {i+1}: {test_data}")
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post("https://agentverse.ai/v1/agents", 
                                           headers=headers, 
                                           json=test_data)
                print(f"     Status: {response.status_code}")
                if response.status_code != 422:
                    print(f"     Success! Response: {response.text[:200]}")
                else:
                    error_data = response.json()
                    print(f"     Error: {error_data.get('detail', 'Unknown error')}")
        except Exception as e:
            print(f"     Exception: {e}")

if __name__ == "__main__":
    asyncio.run(explore_agentverse_api())
