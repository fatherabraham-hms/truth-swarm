#!/usr/bin/env python3
"""
Setup script for Agentverse integration
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check if we're in the right directory
    if not Path("meTTa_eval_agent.py").exists():
        print("❌ meTTa_eval_agent.py not found. Please run this script from the agents directory.")
        return False
    
    # Check for required dependencies
    try:
        import uagents
        print("✅ uagents framework found")
    except ImportError:
        print("❌ uagents framework not found. Please install: pip install uagents")
        return False
    
    try:
        import httpx
        print("✅ httpx found")
    except ImportError:
        print("❌ httpx not found. Please install: pip install httpx")
        return False
    
    # Check for optional dependencies
    try:
        import metta
        print("✅ meTTa framework found (optional)")
    except ImportError:
        print("⚠️ meTTa framework not found (optional). Install with: pip install metta")
    
    return True

def setup_agentverse_key():
    """Help user set up Agentverse API key"""
    print("\n🔑 Setting up Agentverse API key...")
    
    current_key = os.getenv("AGENTVERSE_API_KEY")
    if current_key:
        print(f"✅ AGENTVERSE_API_KEY is already set: {current_key[:8]}...")
        return True
    
    print("\n📋 To get an Agentverse API key:")
    print("   1. Go to https://agentverse.ai")
    print("   2. Log in with your Gmail address")
    print("   3. Navigate to Profile > API Keys")
    print("   4. Click '+ New API Key'")
    print("   5. Give it a name and grant write permissions")
    print("   6. Set permission duration (e.g., 30 days)")
    print("   7. Click 'Generate API Key'")
    print("   8. Copy the generated key")
    
    api_key = input("\n🔑 Enter your Agentverse API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⚠️ No API key provided. Agent will use mock data for testing.")
        return False
    
    # Save to .env file
    env_file = Path(".env")
    env_content = ""
    
    if env_file.exists():
        with open(env_file, "r") as f:
            env_content = f.read()
    
    # Update or add AGENTVERSE_API_KEY
    if "AGENTVERSE_API_KEY" in env_content:
        lines = env_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("AGENTVERSE_API_KEY"):
                lines[i] = f"AGENTVERSE_API_KEY={api_key}"
                break
        env_content = "\n".join(lines)
    else:
        env_content += f"\nAGENTVERSE_API_KEY={api_key}\n"
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print(f"✅ API key saved to {env_file.absolute()}")
    print("💡 You can also set it as an environment variable:")
    print(f"   export AGENTVERSE_API_KEY={api_key}")
    
    return True

def test_agentverse_connection():
    """Test connection to Agentverse"""
    print("\n🔗 Testing Agentverse connection...")
    
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("⚠️ No API key set. Skipping connection test.")
        return False
    
    try:
        import httpx
        import asyncio
        
        async def test():
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
                headers = {"Authorization": f"Bearer {api_key}"}
                response = await client.get("https://agentverse.ai/v1/hosting/agents", headers=headers)
                
                # Handle redirects
                if response.status_code in [301, 302, 307, 308]:
                    redirect_location = response.headers.get("location")
                    print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                    return False
                
                return response.status_code == 200
        
        result = asyncio.run(test())
        if result:
            print("✅ Agentverse connection successful!")
            return True
        else:
            print("❌ Agentverse connection failed. Please check your API key.")
            return False
    except Exception as e:
        print(f"❌ Connection test error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Agentverse Integration Setup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Setup API key
    api_key_set = setup_agentverse_key()
    
    # Test connection if key is set
    if api_key_set:
        test_agentverse_connection()
    
    print("\n" + "=" * 40)
    print("🎯 Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Start the agent: python meTTa_eval_agent.py")
    print("   2. Test the integration: python test_agentverse_integration.py")
    print("   3. Check health: curl http://localhost:8000/health")
    
    if api_key_set:
        print("\n🌐 Available endpoints:")
        print("   • POST /list-agents - List agents from Agentverse")
        print("   • POST /discover-agents - Search for agents")
        print("   • POST /detect-crypto - Detect crypto agents")
    else:
        print("\n⚠️ Agent will use mock data without API key")

if __name__ == "__main__":
    main()
