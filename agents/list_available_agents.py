#!/usr/bin/env python3
"""
List available agents on Agentverse
"""

import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/howardsherman/truth-swarm/.env')

async def list_available_agents():
    """List all available agents on Agentverse"""
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    
    print("🔍 Listing available agents on Agentverse")
    print("=" * 50)
    print(f"API Key: {'*' * 20 if api_key else 'Not found'}")
    print()
    
    if not api_key:
        print("❌ No API key found in environment")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            print("🔍 Getting agents list...")
            response = await client.get("https://agentverse.ai/v1/agents", headers=headers)
            
            if response.status_code == 200:
                agents = response.json()
                print(f"✅ Found {len(agents)} agents total")
                print()
                
                # Show all agents
                for i, agent in enumerate(agents):
                    if isinstance(agent, dict):
                        print(f"{i+1:2d}. {agent.get('name', 'Unknown')}")
                        print(f"     Address: {agent.get('address', 'Unknown')}")
                        print(f"     Status: {agent.get('status', 'Unknown')}")
                        print(f"     Description: {agent.get('description', 'No description')[:80]}...")
                        print()
                
                # Check if our target agent is in the list
                target_agent = "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"
                found = False
                for agent in agents:
                    if isinstance(agent, dict):
                        agent_addr = agent.get('address', '')
                        if target_agent in agent_addr or agent_addr in target_agent:
                            print(f"🎯 Found target agent: {agent.get('name', 'Unknown')}")
                            found = True
                            break
                
                if not found:
                    print(f"❌ Target agent {target_agent} not found in the list")
                
            else:
                print(f"❌ Failed to get agents list: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
        
        except Exception as e:
            print(f"❌ Error getting agents list: {e}")

if __name__ == "__main__":
    asyncio.run(list_available_agents())
