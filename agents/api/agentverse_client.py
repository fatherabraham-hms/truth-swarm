"""Agentverse API client for agent management and communication"""

import httpx
from typing import Dict, Any, List, Optional


class AgentverseAPIClient:
    """Agentverse API client for agent management and communication"""
    
    def __init__(self, api_key: str, base_url: str = "https://agentverse.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def test_connection(self) -> bool:
        """Test API connection"""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
                response = await client.get(f"{self.base_url}/hosting/agents", headers=self.headers)
                
                # Handle redirects
                if response.status_code in [301, 302, 307, 308]:
                    redirect_location = response.headers.get("location")
                    print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                    return False
                
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Agentverse connection test failed: {e}")
            return False
    
    async def get_agents(self) -> List[Dict[str, Any]]:
        """Get list of all agents"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
                response = await client.get(f"{self.base_url}/hosting/agents", headers=self.headers)
                
                # Handle redirects
                if response.status_code in [301, 302, 307, 308]:
                    redirect_location = response.headers.get("location")
                    print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                    return []
                
                if response.status_code == 200:
                    data = response.json()
                    # Handle both list and dict responses
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and 'items' in data:
                        return data['items']
                    else:
                        return []
                else:
                    print(f"❌ Failed to get agents: {response.status_code} - {response.text[:200]}")
                    return []
        except Exception as e:
            print(f"❌ Error getting agents: {e}")
            return []
    
    async def get_agent_details(self, agent_address: str) -> Optional[Dict[str, Any]]:
        """Get details of a specific agent"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
                response = await client.get(f"{self.base_url}/v1/hosting/agents/{agent_address}", headers=self.headers)
                
                # Handle redirects
                if response.status_code in [301, 302, 307, 308]:
                    redirect_location = response.headers.get("location")
                    print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                    return None
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    return None
                else:
                    print(f"❌ Failed to get agent details: {response.status_code} - {response.text[:200]}")
                    return None
        except Exception as e:
            print(f"❌ Error getting agent details: {e}")
            return None
    
    async def get_agent_code(self, agent_address: str) -> Optional[str]:
        """Get agent code/README"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=False) as client:
                response = await client.get(f"{self.base_url}/v1/hosting/agents/{agent_address}/code", headers=self.headers)
                
                # Handle redirects
                if response.status_code in [301, 302, 307, 308]:
                    redirect_location = response.headers.get("location")
                    print(f"⚠️ Redirect detected: {response.status_code} -> {redirect_location}")
                    return None
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 404:
                    return None
                else:
                    print(f"❌ Failed to get agent code: {response.status_code} - {response.text[:200]}")
                    return None
        except Exception as e:
            print(f"❌ Error getting agent code: {e}")
            return None
    
    async def register_agent(self, agent_data: Dict[str, Any]) -> bool:
        """Register a new agent with Agentverse"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self.base_url}/hosting/agents", 
                                          headers=self.headers, 
                                          json=agent_data)
                if response.status_code in [200, 201]:
                    print(f"✅ Agent registered successfully: {response.json()}")
                    return True
                else:
                    print(f"❌ Failed to register agent: {response.status_code} - {response.text}")
                    return False
        except Exception as e:
            print(f"❌ Error registering agent: {e}")
            return False
    
    async def start_agent(self, agent_address: str) -> bool:
        """Start an agent"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self.base_url}/v1/hosting/agents/{agent_address}/start", 
                                          headers=self.headers)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Error starting agent: {e}")
            return False
    
    async def stop_agent(self, agent_address: str) -> bool:
        """Stop an agent"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{self.base_url}/v1/hosting/agents/{agent_address}/stop", 
                                          headers=self.headers)
                return response.status_code == 200
        except Exception as e:
            print(f"❌ Error stopping agent: {e}")
            return False
