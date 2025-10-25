#!/usr/bin/env python3
"""
Show available agents on Agentverse with details
"""

import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/howardsherman/truth-swarm/.env')

async def show_available_agents():
    """Show all available agents on Agentverse with details"""
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    
    print("🔍 Available Agents on Agentverse")
    print("=" * 50)
    
    if not api_key:
        print("❌ No API key found in environment")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.get("https://agentverse.ai/v1/agents", headers=headers)
            
            if response.status_code == 200:
                agents = response.json()
                print(f"✅ Found {len(agents)} agents total")
                print()
                
                # Show all agents with details
                for i, agent in enumerate(agents):
                    if isinstance(agent, dict):
                        print(f"🤖 Agent {i+1}:")
                        print(f"   Name: {agent.get('name', 'Unknown')}")
                        print(f"   Address: {agent.get('address', 'Unknown')}")
                        print(f"   Status: {agent.get('status', 'Unknown')}")
                        print(f"   Description: {agent.get('description', 'No description')}")
                        print(f"   Capabilities: {agent.get('capabilities', [])}")
                        print(f"   Endpoint: {agent.get('endpoint', 'No endpoint')}")
                        print()
                
                print("🎯 To test your agent, use one of these addresses:")
                for i, agent in enumerate(agents):
                    if isinstance(agent, dict):
                        print(f"   {i+1}. {agent.get('address', 'Unknown')} - {agent.get('name', 'Unknown')}")
                
            else:
                print(f"❌ Failed to get agents list: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
        
        except Exception as e:
            print(f"❌ Error getting agents list: {e}")

if __name__ == "__main__":
    asyncio.run(show_available_agents())
