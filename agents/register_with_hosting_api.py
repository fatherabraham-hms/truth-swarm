#!/usr/bin/env python3
"""
Register agent using the correct Agentverse Hosting API
Based on: https://docs.agentverse.ai/docs/api/hosting
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

async def register_with_hosting_api():
    """Register agent using the correct Hosting API endpoint"""
    
    print("🚀 Registering Agent with Agentverse Hosting API")
    print("=" * 60)
    print("Based on: https://docs.agentverse.ai/docs/api/hosting")
    print()
    
    # Get environment variables
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    agent_port = int(os.getenv("PORT", 8000))
    agent_name = os.getenv("AGENT_NAME", "truth_swarm_categorizer_agent")
    api_key = os.getenv("AGENTVERSE_API_KEY")
    
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found")
        print("   Get your API key from: https://docs.agentverse.ai/docs/api/hosting")
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
    
    # Register using Hosting API
    print("\n2. Registering with Hosting API...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Agent registration data for Hosting API
    agent_data = {
        "name": "Truth Swarm Categorizer Agent",
        "description": "Advanced agent categorization and analysis using meTTa framework with comprehensive crypto detection capabilities",
        "address": str(agent.address),
        "endpoint": endpoint_url,
        "capabilities": [
            "crypto_agent_detection",
            "agent_categorization", 
            "feature_extraction",
            "symbolic_reasoning",
            "agentverse_integration",
            "rest_api",
            "metta_analytics"
        ],
        "readme": """# Truth Swarm Categorizer Agent

A sophisticated agent that provides comprehensive categorization and analysis of other agents using advanced meTTa framework symbolic reasoning.

## 🧠 Capabilities

- **Multi-Category Detection**: Identifies agents across multiple categories (crypto, AI, trading, etc.)
- **Feature Extraction**: Extracts detailed technical features and capabilities
- **Crypto Subcategory Analysis**: Deep analysis of crypto-related agents
- **Symbolic Reasoning**: Uses meTTa framework for advanced pattern matching
- **AgentVerse Integration**: Seamlessly integrates with the AgentVerse ecosystem

## 🚀 REST API Endpoints

- `GET /health` - Health check and status
- `POST /categorize-agent` - Comprehensive agent categorization
- `POST /extract-features` - Detailed feature extraction
- `POST /detect-crypto` - Crypto agent detection
- `GET /get-taxonomy` - Category taxonomy information
- `POST /list-agents` - List agents from AgentVerse
- `POST /discover-agents` - Search for agents by capabilities

## 📊 Example Usage

```bash
# Comprehensive agent categorization
curl -X POST https://your-app.railway.app/categorize-agent \\
     -H "Content-Type: application/json" \\
     -d '{"agent_id": "agent123", "include_features": true, "include_crypto_details": true}'

# Feature extraction
curl -X POST https://your-app.railway.app/extract-features \\
     -H "Content-Type: application/json" \\
     -d '{"agent_id": "agent123"}'

# Get category taxonomy
curl https://your-app.railway.app/get-taxonomy
```

## 🔧 Technical Details

- Built with uAgent framework
- Integrates with meTTa (Hyperon) for symbolic reasoning
- Uses AgentVerse API for agent discovery
- Supports both local and cloud deployment
- Enhanced error handling and fallback mechanisms

## 🎯 Use Cases

- Agent discovery and categorization
- Crypto agent identification
- Technical feature analysis
- Agent ecosystem mapping
- Research and analytics
""",
        "version": "2.0.0",
        "status": "active",
        "tags": ["crypto", "detection", "analysis", "metta", "agentverse", "categorization", "features"]
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Use the correct Hosting API endpoint
            response = await client.post("https://agentverse.ai/v1/hosting/agents", 
                                       headers=headers, 
                                       json=agent_data)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
            if response.status_code in [200, 201]:
                print("✅ Agent registered successfully with Hosting API!")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code}")
                print(f"Error details: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False
    
    # Verify registration
    print("\n3. Verifying registration...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get("https://agentverse.ai/v1/hosting/agents", headers=headers)
            
            if response.status_code == 200:
                agents = response.json()
                print(f"✅ Found {len(agents)} agents in Hosting API")
                
                # Look for our agent
                for agent_data in agents:
                    if (agent_data.get('address') == str(agent.address) or 
                        agent_data.get('agent_address') == str(agent.address)):
                        print(f"✅ Our agent found: {agent_data.get('name', 'No name')}")
                        print(f"   Status: {agent_data.get('status', 'Unknown')}")
                        print(f"   Endpoint: {agent_data.get('endpoint', 'No endpoint')}")
                        return True
                
                print("❌ Our agent not found in the list")
                return False
            else:
                print(f"❌ Cannot verify registration: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(register_with_hosting_api())
