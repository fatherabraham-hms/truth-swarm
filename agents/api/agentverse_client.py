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
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                # Try the v1 API endpoint first
                response = await client.get(f"{self.base_url}/v1/agents", headers=self.headers)
                
                # 405 means the endpoint exists but doesn't accept GET (which is expected)
                if response.status_code in [200, 405]:
                    return True
                
                # Try alternative endpoints
                response = await client.get(f"{self.base_url}/api/agents", headers=self.headers)
                if response.status_code in [200, 405]:
                    return True
                
                # Try the hosting endpoint
                response = await client.get(f"{self.base_url}/hosting/agents", headers=self.headers)
                return response.status_code in [200, 405]
        except Exception as e:
            print(f"❌ Agentverse connection test failed: {e}")
            return False
    
    async def get_agents(self) -> List[Dict[str, Any]]:
        """Get list of all agents"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                # Try multiple endpoint patterns
                endpoints = [
                    f"{self.base_url}/v1/agents",
                    f"{self.base_url}/api/agents", 
                    f"{self.base_url}/agents",
                    f"{self.base_url}/hosting/agents"
                ]
                
                for endpoint in endpoints:
                    try:
                        response = await client.get(endpoint, headers=self.headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            # Handle both list and dict responses
                            if isinstance(data, list):
                                print(f"✅ Successfully retrieved agents from {endpoint}")
                                return data
                            elif isinstance(data, dict) and 'items' in data:
                                print(f"✅ Successfully retrieved agents from {endpoint}")
                                return data['items']
                            elif isinstance(data, dict) and 'agents' in data:
                                print(f"✅ Successfully retrieved agents from {endpoint}")
                                return data['agents']
                        elif response.status_code == 405:
                            # Method not allowed, try next endpoint
                            continue
                        else:
                            print(f"⚠️ Endpoint {endpoint} returned {response.status_code}")
                            continue
                    except Exception as e:
                        print(f"⚠️ Error with endpoint {endpoint}: {e}")
                        continue
                
                print("❌ All agent endpoints failed")
                return []
        except Exception as e:
            print(f"❌ Error getting agents: {e}")
            return []
    
    async def get_agent_details(self, agent_address: str) -> Optional[Dict[str, Any]]:
        """Get details of a specific agent"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                # Try multiple endpoint patterns
                endpoints = [
                    f"{self.base_url}/v1/hosting/agents/{agent_address}",  # Try hosting first
                    f"{self.base_url}/v1/agents/{agent_address}",
                    f"{self.base_url}/api/agents/{agent_address}",
                    f"{self.base_url}/agents/{agent_address}",
                    f"{self.base_url}/hosting/agents/{agent_address}"
                ]
                
                for endpoint in endpoints:
                    try:
                        response = await client.get(endpoint, headers=self.headers)
                        
                        if response.status_code == 200:
                            print(f"✅ Successfully retrieved agent details from {endpoint}")
                            return response.json()
                        elif response.status_code == 404:
                            print(f"⚠️ Agent not found at {endpoint}")
                            continue
                        elif response.status_code == 405:
                            # Method not allowed, try next endpoint
                            continue
                        else:
                            print(f"⚠️ Endpoint {endpoint} returned {response.status_code}")
                            continue
                    except Exception as e:
                        print(f"⚠️ Error with endpoint {endpoint}: {e}")
                        continue
                
                print(f"❌ All agent detail endpoints failed for {agent_address}")
                return None
        except Exception as e:
            print(f"❌ Error getting agent details: {e}")
            return None
    
    async def get_agent_code(self, agent_address: str) -> Optional[str]:
        """Get agent code/README"""
        try:
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                # Try the main API endpoint first
                response = await client.get(f"{self.base_url}/agents/{agent_address}/code", headers=self.headers)
                
                if response.status_code == 200:
                    return response.text
                elif response.status_code == 404:
                    return None
                
                # If that fails, try the hosting endpoint
                response = await client.get(f"{self.base_url}/hosting/agents/{agent_address}/code", headers=self.headers)
                
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
            async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
                # Try multiple endpoint patterns
                endpoints = [
                    f"{self.base_url}/v1/agents",
                    f"{self.base_url}/api/agents",
                    f"{self.base_url}/agents",
                    f"{self.base_url}/hosting/agents"
                ]
                
                for endpoint in endpoints:
                    try:
                        response = await client.post(endpoint, 
                                                  headers=self.headers, 
                                                  json=agent_data)
                        if response.status_code in [200, 201]:
                            print(f"✅ Agent registered successfully at {endpoint}: {response.json()}")
                            return True
                        else:
                            print(f"⚠️ Registration failed at {endpoint}: {response.status_code} - {response.text[:200]}")
                            continue
                    except Exception as e:
                        print(f"⚠️ Error with endpoint {endpoint}: {e}")
                        continue
                
                print("❌ All registration endpoints failed")
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
