#!/usr/bin/env python3
"""
Agent Registration Script for Agentverse

This script registers the crypto detection agent with Agentverse so it can be discovered
and communicate with other agents in the ecosystem.
"""

import os
import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from api.agentverse_client import AgentverseAPIClient
from uagents import Agent

def get_agent_info() -> Dict[str, Any]:
    """Get agent information for registration"""
    
    # Create a temporary agent instance to get the address
    temp_agent = Agent(
        name="crypto_detection_agent",
        seed="crypto_detection_seed_2024_truth_swarm",
        port=8000,
        endpoint=["http://localhost:8000/submit"],
        mailbox=False
    )
    
    # Read the README file
    readme_path = Path("README.md")
    readme_content = ""
    if readme_path.exists():
        with open(readme_path, "r") as f:
            readme_content = f.read()
    else:
        readme_content = """# Crypto Detection Agent

A specialized agent that detects cryptocurrency-related agents using advanced symbolic reasoning with the meTTa framework and AgentVerse integration.

## Capabilities

- **Crypto Agent Detection**: Identifies agents involved in cryptocurrency, blockchain, DeFi, and trading
- **Agent Profile Analysis**: Analyzes agent descriptions, capabilities, and README content
- **Symbolic Reasoning**: Uses meTTa framework for advanced pattern matching and evaluation
- **AgentVerse Integration**: Seamlessly integrates with the AgentVerse ecosystem
- **REST API**: Provides HTTP endpoints for easy integration

## Usage

The agent provides several REST API endpoints:

- `GET /health` - Health check and status
- `POST /detect-crypto` - Detect if an agent is crypto-related
- `POST /list-agents` - List agents from AgentVerse
- `POST /discover-agents` - Search for agents by capabilities

## Example

```bash
# Detect if an agent is crypto-related
curl -X POST http://localhost:8000/detect-crypto \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "example-agent-123"}'
```

## Technical Details

- Built with uAgent framework
- Integrates with meTTa for symbolic reasoning
- Uses AgentVerse API for agent discovery
- Supports both local and cloud deployment
"""
    
    return {
        "name": "Crypto Detection Agent",
        "description": "Detects cryptocurrency-related agents using meTTa framework and AgentVerse integration",
        "agent_address": str(temp_agent.address),
        "endpoint": "http://localhost:8000/submit",
        "capabilities": [
            "crypto_agent_detection",
            "agent_profile_analysis", 
            "symbolic_reasoning",
            "agentverse_integration",
            "rest_api"
        ],
        "readme": readme_content,
        "version": "1.0.0",
        "status": "active",
        "tags": ["crypto", "detection", "analysis", "metta", "agentverse"]
    }

async def register_with_agentverse():
    """Register the agent with Agentverse"""
    print("🚀 Agent Registration for Agentverse")
    print("=" * 50)
    
    # Check for API key
    api_key = os.getenv("AGENTVERSE_API_KEY", "eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3NjM3NTkwOTAsImlhdCI6MTc2MTE2NzA5MCwiaXNzIjoiZmV0Y2guYWkiLCJqdGkiOiI4ZTNjN2UwOTNmNjBkNDdmNzMwZWRjYWUiLCJzY29wZSI6ImF2Iiwic3ViIjoiMGFhYmM1MWJmMzBhM2VkMDdlMTZiNDg4OTliZDBjMTUyOGRmY2UwNzE2MmFiMWIzIn0.HC-RF4rvuVcIYW07khIIh0ip_IBsYelI1q4qb6stPEUTeU0PgB-mv88sABJKoJP0qMH5w0aR9RYxe0maNla9YQZVfU2cxG7ArFfKKXjoq5cKKwZUd874gTH9_Vr7InMKK9EGeXp8Rwa4jcbL2ejz_lZZYWq5H6AOSp5ON1KkNh44Jfh5DnNhzaQ2rolx00UyMmysZC60JJUTyCclBpMxpecb_ZWsvAitDKFzNjiZZxIYAgLygVuMvw47Iat1oBJx-n8yoepWJdjVZYC4ktiPa9QNBZASe1f1Ku7UkfdyoWLPdmkMBS7hXXvbTxsWtuR9Rn4OmgstrkZ9neE_tUCbYQ")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found in environment variables")
        print("   Please run: python setup_agentverse.py")
        return False
    
    # Initialize API client with correct base URL
    client = AgentverseAPIClient(api_key, "https://agentverse.ai/v1")
    
    # Test connection first
    print("1. Testing Agentverse connection...")
    if not await client.test_connection():
        print("❌ Cannot connect to Agentverse. Please check your API key.")
        return False
    print("✅ Connection successful")
    
    # Get agent information
    print("\n2. Preparing agent information...")
    agent_info = get_agent_info()
    print(f"   Agent Name: {agent_info['name']}")
    print(f"   Agent Address: {agent_info['agent_address']}")
    print(f"   Endpoint: {agent_info['endpoint']}")
    print(f"   Capabilities: {', '.join(agent_info['capabilities'])}")
    
    # Register the agent
    print("\n3. Registering agent with Agentverse...")
    success = await client.register_agent(agent_info)
    
    if success:
        print("✅ Agent registered successfully!")
        print(f"   Agent Address: {agent_info['agent_address']}")
        print(f"   You can now discover this agent from other agents")
        print(f"   Test with: python test_agentverse_integration.py")
        return True
    else:
        print("❌ Agent registration failed")
        return False

async def check_existing_agents():
    """Check if agent is already registered"""
    print("🔍 Checking existing agents...")
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ No API key found")
        return False
    
    client = AgentverseAPIClient(api_key, "https://agentverse.ai/v1")
    agents = await client.get_agents()
    
    if agents and isinstance(agents, list):
        print(f"   Found {len(agents)} registered agents")
        for agent in agents[:5]:  # Show first 5
            print(f"   • {agent.get('name', 'Unknown')} - {agent.get('agent_address', 'No address')}")
        if len(agents) > 5:
            print(f"   ... and {len(agents) - 5} more")
    else:
        print("   No agents found or API connection failed")
    
    return len(agents) > 0

async def main():
    """Main registration function"""
    print("🎯 Crypto Detection Agent Registration")
    print("This will register your agent with Agentverse for discovery and communication")
    print()
    
    # Check existing agents first
    await check_existing_agents()
    print()
    
    # Confirm registration
    confirm = input("Do you want to register the crypto detection agent? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Registration cancelled")
        return
    
    # Register the agent
    success = await register_with_agentverse()
    
    if success:
        print("\n🎉 Registration completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Start your agent: python run_agent.py")
        print("   2. Test the registration: python test_agentverse_integration.py")
        print("   3. Other agents can now discover and communicate with your agent")
    else:
        print("\n❌ Registration failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())
