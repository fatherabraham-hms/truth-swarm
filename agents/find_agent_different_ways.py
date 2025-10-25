#!/usr/bin/env python3
"""
Try different methods to find the specific agent on Agentverse
"""

import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/howardsherman/truth-swarm/.env')

async def find_agent_different_ways():
    """Try different methods to find the agent"""
    
    agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    api_key = os.getenv("AGENTVERSE_API_KEY")
    
    print("🔍 Trying different methods to find your agent")
    print("=" * 60)
    print(f"Agent ID: {agent_id}")
    print()
    
    if not api_key:
        print("❌ No API key found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        
        # Method 1: Try different base URLs
        print("1️⃣ Trying different base URLs...")
        base_urls = [
            "https://agentverse.ai",
            "https://api.agentverse.ai", 
            "https://hosting.agentverse.ai"
        ]
        
        for base_url in base_urls:
            try:
                url = f"{base_url}/v1/agents/{agent_id}"
                print(f"   Trying: {url}")
                response = await client.get(url, headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Found! Name: {data.get('name', 'Unknown')}")
                    return True
                elif response.status_code != 404:
                    print(f"   Response: {response.text[:100]}...")
            except Exception as e:
                print(f"   Error: {e}")
            print()
        
        # Method 2: Try different endpoint patterns
        print("2️⃣ Trying different endpoint patterns...")
        endpoints = [
            f"https://agentverse.ai/v1/agents/{agent_id}",
            f"https://agentverse.ai/api/v1/agents/{agent_id}",
            f"https://agentverse.ai/hosting/v1/agents/{agent_id}",
            f"https://agentverse.ai/agents/{agent_id}",
            f"https://agentverse.ai/hosting/agents/{agent_id}",
            f"https://agentverse.ai/v1/hosting/agents/{agent_id}"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"   Trying: {endpoint}")
                response = await client.get(endpoint, headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Found! Name: {data.get('name', 'Unknown')}")
                    return True
                elif response.status_code not in [404, 307]:
                    print(f"   Response: {response.text[:100]}...")
            except Exception as e:
                print(f"   Error: {e}")
            print()
        
        # Method 3: Search in agents list with different parameters
        print("3️⃣ Searching in agents list with different parameters...")
        
        # Try different query parameters
        search_params = [
            {},
            {"limit": 100},
            {"offset": 0, "limit": 100},
            {"status": "active"},
            {"status": "all"},
            {"include_inactive": "true"}
        ]
        
        for params in search_params:
            try:
                url = "https://agentverse.ai/v1/agents"
                print(f"   Trying: {url} with params: {params}")
                response = await client.get(url, headers=headers, params=params)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    agents = response.json()
                    print(f"   Found {len(agents)} agents")
                    
                    # Look for our agent
                    for agent in agents:
                        if isinstance(agent, dict):
                            agent_addr = agent.get('address', '')
                            if agent_id == agent_addr:
                                print(f"   ✅ Found in list! Name: {agent.get('name', 'Unknown')}")
                                print(f"   Status: {agent.get('status', 'Unknown')}")
                                return True
                    
                    print(f"   ❌ Agent not found in this list")
                else:
                    print(f"   Response: {response.text[:100]}...")
            except Exception as e:
                print(f"   Error: {e}")
            print()
        
        print("❌ Could not find the agent using any method")
        return False

if __name__ == "__main__":
    asyncio.run(find_agent_different_ways())
