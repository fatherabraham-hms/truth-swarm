#!/usr/bin/env python3
"""
Check if a specific agent exists on Agentverse
"""

import asyncio
import httpx
import json

async def check_agent_exists():
    """Check if the specific agent exists on Agentverse"""
    
    agent_id = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
    
    print("🔍 Checking if agent exists on Agentverse")
    print("=" * 50)
    print(f"Agent ID: {agent_id}")
    print()
    
    # Try different endpoints
    endpoints = [
        f"https://agentverse.ai/v1/agents/{agent_id}",
        f"https://agentverse.ai/api/agents/{agent_id}",
        f"https://agentverse.ai/agents/{agent_id}",
        f"https://agentverse.ai/hosting/agents/{agent_id}"
    ]
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        for endpoint in endpoints:
            try:
                print(f"🔍 Trying: {endpoint}")
                response = await client.get(endpoint)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Found agent!")
                    print(f"   Name: {data.get('name', 'Unknown')}")
                    print(f"   Description: {data.get('description', 'No description')[:100]}...")
                    print(f"   Address: {data.get('address', 'Unknown')}")
                    print(f"   Status: {data.get('status', 'Unknown')}")
                    return True
                elif response.status_code == 404:
                    print(f"   ❌ Not found")
                elif response.status_code == 307:
                    print(f"   🔄 Redirect to: {response.headers.get('Location', 'Unknown')}")
                else:
                    print(f"   ⚠️ Unexpected status: {response.status_code}")
                    print(f"   Response: {response.text[:200]}...")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print()
    
    # Also try to search for it in the agents list
    print("🔍 Searching in agents list...")
    try:
        response = await client.get("https://agentverse.ai/v1/agents")
        if response.status_code == 200:
            agents = response.json()
            print(f"   Found {len(agents)} agents total")
            
            # Look for our agent
            found = False
            for agent in agents:
                if isinstance(agent, dict):
                    agent_addr = agent.get('address', '')
                    if agent_id in agent_addr or agent_addr in agent_id:
                        print(f"   ✅ Found in list!")
                        print(f"   Name: {agent.get('name', 'Unknown')}")
                        print(f"   Address: {agent.get('address', 'Unknown')}")
                        print(f"   Status: {agent.get('status', 'Unknown')}")
                        found = True
                        break
            
            if not found:
                print(f"   ❌ Agent not found in agents list")
                print(f"   First few agents:")
                for i, agent in enumerate(agents[:3]):
                    if isinstance(agent, dict):
                        print(f"     {i+1}. {agent.get('name', 'Unknown')} - {agent.get('address', 'Unknown')}")
        else:
            print(f"   ❌ Failed to get agents list: {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Error getting agents list: {e}")
    
    return False

if __name__ == "__main__":
    asyncio.run(check_agent_exists())
