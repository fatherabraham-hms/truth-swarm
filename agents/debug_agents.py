#!/usr/bin/env python3
"""
Simple debug script to see what agents are on Agentverse
"""

import os
import asyncio
import httpx

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
except ImportError:
    pass

async def debug_agents():
    """Debug what agents are on Agentverse"""
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        return
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Debugging Agentverse agents...")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get("https://agentverse.ai/v1/agents", headers=headers)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                agents = response.json()
                print(f"Found {len(agents)} agents")
                print(f"Raw response: {agents}")
                
                if agents:
                    print(f"\nFirst agent structure:")
                    print(f"Type: {type(agents[0])}")
                    if isinstance(agents[0], dict):
                        print(f"Keys: {list(agents[0].keys())}")
                        print(f"Values: {agents[0]}")
                    else:
                        print(f"Value: {agents[0]}")
            else:
                print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_agents())
