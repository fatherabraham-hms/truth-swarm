#!/usr/bin/env python3
"""
Quick agent registration script for the running agent
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

async def register_my_agent():
    """Register the currently running agent with Agentverse"""
    
    # Your agent details (from the logs you showed)
    agent_address = "agent1q2w87lcmxs0ykma6dnklhnyd8usprv3rzc3e9umpgyf9726xtumfjtvx5a5"
    
    # Get Railway URL if available
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_url:
        endpoint_url = f"https://{railway_url}/submit"
    else:
        endpoint_url = "http://localhost:8080/submit"
    
    # Agent information
    agent_info = {
        "name": "Truth Swarm Categorizer Agent",
        "description": "Advanced agent categorization and analysis using meTTa framework with comprehensive crypto detection capabilities",
        "agent_address": agent_address,
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
    
    print("🚀 Registering Truth Swarm Categorizer Agent")
    print("=" * 50)
    print(f"Agent Address: {agent_address}")
    print(f"Endpoint: {endpoint_url}")
    print(f"Name: {agent_info['name']}")
    print()
    
    # Check for API key
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("❌ AGENTVERSE_API_KEY not found in environment variables")
        print("   Please set your API key in the .env file or environment")
        return False
    
    # Initialize API client
    client = AgentverseAPIClient(api_key, "https://agentverse.ai")
    
    # Test connection first
    print("1. Testing Agentverse connection...")
    if not await client.test_connection():
        print("❌ Cannot connect to Agentverse. Please check your API key.")
        return False
    print("✅ Connection successful")
    
    # Register the agent
    print("\n2. Registering agent with Agentverse...")
    success = await client.register_agent(agent_info)
    
    if success:
        print("✅ Agent registered successfully!")
        print(f"   Agent Address: {agent_address}")
        print(f"   You can now find your agent on Agentverse with name and README")
        return True
    else:
        print("❌ Agent registration failed")
        return False

if __name__ == "__main__":
    asyncio.run(register_my_agent())
