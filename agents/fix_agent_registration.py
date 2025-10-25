#!/usr/bin/env python3
"""
Fix agent registration with Agentverse
"""

import os
import asyncio
import httpx
from uagents import Agent

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from: {env_path}")
except ImportError:
    print("⚠️ python-dotenv not available, using system environment variables only")

async def fix_agent_registration():
    """Fix the agent registration with Agentverse"""
    
    print("🔧 Fixing Agent Registration with Agentverse")
    print("=" * 50)
    
    # Get environment variables
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    agent_port = int(os.getenv("PORT", 8000))
    agent_name = os.getenv("AGENT_NAME", "truth_swarm_categorizer_agent")
    api_key = os.getenv("AGENTVERSE_API_KEY")
    
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        return False
    
    # Create agent instance
    if railway_url:
        endpoint_url = f"https://{railway_url}/submit"
    else:
        endpoint_url = "http://localhost:8000/submit"
    
    agent = Agent(
        name=agent_name,
        seed="crypto_detection_seed_2024_truth_swarm",
        port=agent_port,
        endpoint=[endpoint_url],
        mailbox=True
    )
    
    print(f"Agent Address: {agent.address}")
    print(f"Endpoint: {endpoint_url}")
    print(f"Railway URL: {railway_url}")
    print()
    
    # Test agent is running
    print("1. Testing agent is running...")
    try:
        if railway_url:
            health_url = f"https://{railway_url}/health"
        else:
            health_url = "http://localhost:8000/health"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(health_url)
            if response.status_code == 200:
                print("✅ Agent is running and responding")
            else:
                print(f"❌ Agent not responding: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Cannot reach agent: {e}")
        return False
    
    # Try different registration approaches
    print("\n2. Attempting registration with different methods...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Method 1: Try the new Agentverse API format
    print("\n   Method 1: New API format...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try to register with the new format
            registration_data = {
                "address": str(agent.address),
                "name": "Truth Swarm Categorizer Agent",
                "description": "Advanced agent categorization and analysis using meTTa framework",
                "endpoint": endpoint_url,
                "capabilities": ["crypto_detection", "categorization", "feature_extraction"],
                "readme": """# Truth Swarm Categorizer Agent

A sophisticated agent that provides comprehensive categorization and analysis of other agents using advanced meTTa framework symbolic reasoning.

## Capabilities
- Multi-Category Detection
- Feature Extraction  
- Crypto Subcategory Analysis
- Symbolic Reasoning
- AgentVerse Integration

## API Endpoints
- GET /health - Health check
- POST /categorize-agent - Agent categorization
- POST /extract-features - Feature extraction
- GET /get-taxonomy - Category taxonomy
"""
            }
            
            # Try different endpoints
            endpoints = [
                "https://agentverse.ai/v1/agents",
                "https://agentverse.ai/api/agents",
                "https://agentverse.ai/agents"
            ]
            
            for endpoint in endpoints:
                try:
                    response = await client.post(endpoint, headers=headers, json=registration_data)
                    print(f"     {endpoint}: {response.status_code}")
                    if response.status_code in [200, 201]:
                        print(f"     ✅ Success! Response: {response.text[:200]}")
                        return True
                    elif response.status_code == 422:
                        print(f"     ⚠️ Validation error: {response.text[:200]}")
                    else:
                        print(f"     ❌ Failed: {response.text[:200]}")
                except Exception as e:
                    print(f"     ❌ Error: {e}")
    except Exception as e:
        print(f"   ❌ Method 1 failed: {e}")
    
    # Method 2: Try to update existing agent
    print("\n   Method 2: Update existing agent...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try to get existing agent first
            response = await client.get(f"https://agentverse.ai/v1/agents/{agent.address}", headers=headers)
            if response.status_code == 200:
                print("     ✅ Agent exists, trying to update...")
                # Try to update
                update_data = {
                    "name": "Truth Swarm Categorizer Agent",
                    "description": "Advanced agent categorization and analysis using meTTa framework",
                    "endpoint": endpoint_url,
                    "readme": "Updated README content"
                }
                response = await client.put(f"https://agentverse.ai/v1/agents/{agent.address}", headers=headers, json=update_data)
                if response.status_code in [200, 201]:
                    print("     ✅ Agent updated successfully!")
                    return True
                else:
                    print(f"     ❌ Update failed: {response.status_code} - {response.text[:200]}")
            else:
                print(f"     ⚠️ Agent not found: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Method 2 failed: {e}")
    
    # Method 3: Check if agent is already registered but not showing
    print("\n   Method 3: Check agent visibility...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Try to get all agents
            response = await client.get("https://agentverse.ai/v1/agents", headers=headers)
            if response.status_code == 200:
                agents = response.json()
                print(f"     Found {len(agents)} agents on Agentverse")
                
                # Debug: print the structure
                if agents:
                    print(f"     Sample agent structure: {type(agents[0])}")
                    if isinstance(agents[0], dict):
                        print(f"     Sample agent keys: {list(agents[0].keys())}")
                
                # Look for our agent
                try:
                    for agent_data in agents:
                        if isinstance(agent_data, dict):
                            if (agent_data.get('address') == str(agent.address) or 
                                agent_data.get('agent_address') == str(agent.address)):
                                print(f"     ✅ Found our agent: {agent_data.get('name', 'No name')}")
                                print(f"        Status: {agent_data.get('status', 'Unknown')}")
                                print(f"        Endpoint: {agent_data.get('endpoint', 'No endpoint')}")
                                return True
                        else:
                            print(f"     Agent data type: {type(agent_data)}")
                    
                    print("     ❌ Our agent not found in the list")
                    print("     Available agents:")
                    for i, agent_data in enumerate(agents[:3]):  # Show first 3
                        if isinstance(agent_data, dict):
                            print(f"       {i+1}. {agent_data.get('name', 'No name')} - {agent_data.get('address', 'No address')}")
                        else:
                            print(f"       {i+1}. {agent_data}")
                except Exception as e:
                    print(f"     Error processing agents: {e}")
                    print(f"     Agents data: {agents}")
            else:
                print(f"     ❌ Cannot get agents list: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Method 3 failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n❌ All registration methods failed")
    print("\n🔧 Manual steps needed:")
    print("1. Go to https://agentverse.ai")
    print("2. Search for your agent address")
    print("3. If found, edit it to add name and README")
    print("4. If not found, contact Agentverse support")
    
    return False

if __name__ == "__main__":
    asyncio.run(fix_agent_registration())
