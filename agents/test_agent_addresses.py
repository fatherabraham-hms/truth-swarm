#!/usr/bin/env python3
"""
Test agent addresses to see if they're working
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

async def test_agent_address(agent_address: str):
    """Test if an agent address is working"""
    
    print(f"🔍 Testing agent: {agent_address}")
    print("=" * 60)
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Check if agent exists in Hosting API
    print("1. Checking agent in Hosting API...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"https://agentverse.ai/v1/hosting/agents/{agent_address}", headers=headers)
            
            if response.status_code == 200:
                agent_data = response.json()
                print("✅ Agent found in Hosting API!")
                print(f"   Name: {agent_data.get('name', 'No name')}")
                print(f"   Status: {agent_data.get('running', 'Unknown')}")
                print(f"   Endpoint: {agent_data.get('endpoint', 'No endpoint')}")
                print(f"   Created: {agent_data.get('creation_timestamp', 'Unknown')}")
                return True
            elif response.status_code == 404:
                print("❌ Agent not found in Hosting API")
            else:
                print(f"⚠️ Unexpected response: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error checking Hosting API: {e}")
    
    # Test 2: Check if agent exists in regular API
    print("\n2. Checking agent in regular API...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"https://agentverse.ai/v1/agents/{agent_address}", headers=headers)
            
            if response.status_code == 200:
                agent_data = response.json()
                print("✅ Agent found in regular API!")
                print(f"   Data: {agent_data}")
                return True
            elif response.status_code == 404:
                print("❌ Agent not found in regular API")
            else:
                print(f"⚠️ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking regular API: {e}")
    
    # Test 3: Check if agent is in the agents list
    print("\n3. Checking agent in agents list...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://agentverse.ai/v1/hosting/agents", headers=headers)
            
            if response.status_code == 200:
                agents = response.json()
                print(f"📊 Found {len(agents)} agents in Hosting API")
                
                # Look for our agent
                for agent_data in agents:
                    if agent_data.get('address') == agent_address:
                        print("✅ Agent found in agents list!")
                        print(f"   Name: {agent_data.get('name', 'No name')}")
                        print(f"   Running: {agent_data.get('running', 'Unknown')}")
                        return True
                
                print("❌ Agent not found in agents list")
                print("   Available agents:")
                for i, agent in enumerate(agents[:3]):
                    print(f"     {i+1}. {agent.get('name', 'No name')} - {agent.get('address', 'No address')}")
            else:
                print(f"❌ Cannot get agents list: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking agents list: {e}")
    
    # Test 4: Try to ping the agent's endpoint
    print("\n4. Testing agent endpoint...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try to get agent details to find the endpoint
            response = await client.get(f"https://agentverse.ai/v1/hosting/agents/{agent_address}", headers=headers)
            
            if response.status_code == 200:
                agent_data = response.json()
                endpoint = agent_data.get('endpoint')
                
                if endpoint:
                    print(f"   Testing endpoint: {endpoint}")
                    
                    # Try to reach the endpoint
                    if endpoint.startswith('https://'):
                        health_url = endpoint.replace('/submit', '/health')
                    else:
                        health_url = endpoint.replace('/submit', '/health')
                    
                    try:
                        health_response = await client.get(health_url, timeout=5.0)
                        if health_response.status_code == 200:
                            print("✅ Agent endpoint is responding!")
                            print(f"   Health response: {health_response.text[:200]}")
                            return True
                        else:
                            print(f"⚠️ Endpoint responded with: {health_response.status_code}")
                    except Exception as e:
                        print(f"❌ Cannot reach endpoint: {e}")
                else:
                    print("❌ No endpoint found for agent")
            else:
                print("❌ Cannot get agent details for endpoint test")
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")
    
    print("\n❌ Agent appears to be not working or not found")
    return False

async def main():
    """Test multiple agent addresses"""
    
    # Test both addresses
    addresses_to_test = [
        "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5",  # Original
        "agent1qtelh3evq6hcd3ksqkl6y7v5v87knddv2vz2reyqudknm4ztce9l5d75v8n",  # Registered
        "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac"   # Target agent
    ]
    
    print("🧪 Testing Agent Addresses")
    print("=" * 60)
    
    for i, address in enumerate(addresses_to_test, 1):
        print(f"\n{'='*20} TEST {i} {'='*20}")
        await test_agent_address(address)
        print()
    
    print("🎯 Summary:")
    print("- If an agent shows as 'found' and 'running', it's working")
    print("- If an agent shows as 'found' but not 'running', it's registered but not active")
    print("- If an agent is 'not found', it's not registered with Agentverse")

if __name__ == "__main__":
    asyncio.run(main())
