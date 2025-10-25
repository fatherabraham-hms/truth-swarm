#!/usr/bin/env python3
"""
Check agent status and help with Agentverse registration
"""

import os
import asyncio
from uagents import Agent

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from: {env_path}")
except ImportError:
    print("⚠️ python-dotenv not available, using system environment variables only")

from api.agentverse_client import AgentverseAPIClient

async def check_agent_status():
    """Check the current agent status and configuration"""
    
    print("🔍 Agent Status Check")
    print("=" * 50)
    
    # Get environment variables
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    agent_port = int(os.getenv("PORT", 8000))
    agent_name = os.getenv("AGENT_NAME", "truth_swarm_categorizer_agent")
    
    # Create agent instance to get address
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
    
    print(f"Agent Name: {agent_name}")
    print(f"Agent Address: {agent.address}")
    print(f"Endpoint URL: {endpoint_url}")
    print(f"Railway URL: {railway_url or 'Not set'}")
    print(f"Port: {agent_port}")
    print(f"Mailbox: Enabled")
    print()
    
    # Check if agent is running
    print("🔍 Checking if agent is running...")
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            if railway_url:
                health_url = f"https://{railway_url}/health"
            else:
                health_url = "http://localhost:8000/health"
            
            response = await client.get(health_url)
            if response.status_code == 200:
                print("✅ Agent is running and responding")
                data = response.json()
                print(f"   Agent Address from health: {data.get('agent_address', 'Not found')}")
            else:
                print(f"❌ Agent not responding: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach agent: {e}")
    
    print()
    
    # Check Agentverse connection
    print("🔍 Checking Agentverse connection...")
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        return
    
    client = AgentverseAPIClient(api_key, "https://agentverse.ai")
    
    try:
        connection_ok = await client.test_connection()
        if connection_ok:
            print("✅ Agentverse connection successful")
            
            # Try to get agents list
            agents = await client.get_agents()
            print(f"📊 Found {len(agents)} agents on Agentverse")
            
            # Look for our agent
            our_agent = None
            for agent_data in agents:
                if agent_data.get('address') == str(agent.address) or agent_data.get('agent_address') == str(agent.address):
                    our_agent = agent_data
                    break
            
            if our_agent:
                print("✅ Our agent found on Agentverse:")
                print(f"   Name: {our_agent.get('name', 'No name')}")
                print(f"   Description: {our_agent.get('description', 'No description')}")
                print(f"   Endpoint: {our_agent.get('endpoint', 'No endpoint')}")
                print(f"   Status: {our_agent.get('status', 'Unknown')}")
            else:
                print("❌ Our agent not found on Agentverse")
                print("   This explains why it shows as 'local'")
                print("   We need to register it properly")
        else:
            print("❌ Agentverse connection failed")
    except Exception as e:
        print(f"❌ Error checking Agentverse: {e}")

if __name__ == "__main__":
    asyncio.run(check_agent_status())
