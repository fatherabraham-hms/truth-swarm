#!/usr/bin/env python3
"""
meTTa Agent Client - HTTP client for communicating with deployed meTTa categorization agent
"""

import os
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class CategoryResult:
    """Result of agent categorization"""
    category_type: str
    confidence: float
    keywords_matched: list
    reasoning: str


@dataclass
class FeatureExtractionResult:
    """Result of feature extraction"""
    tech_stack: list
    supported_chains: list
    protocols: list
    key_features: list
    capabilities: list
    integrations: list
    target_audience: Optional[str]
    business_model: Optional[str]


@dataclass
class MeTTaCategorizationResponse:
    """Response from meTTa categorization endpoint"""
    agent_id: str
    primary_category: CategoryResult
    secondary_categories: list
    extracted_features: Optional[FeatureExtractionResult]
    crypto_details: Optional[Dict[str, Any]]
    is_unknown_category: bool
    evaluation_method: str
    processing_time: float
    timestamp: str


class MeTTaClient:
    """HTTP client for meTTa categorization agent"""
    
    def __init__(self):
        self.base_url = os.getenv("METTA_AGENT_URL", "https://truth-swarm-production.up.railway.app")
        self.timeout = int(os.getenv("METTA_TIMEOUT", "10"))
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def categorize_agent(self, agent_id: str) -> Optional[MeTTaCategorizationResponse]:
        """
        Call meTTa agent's categorize-agent endpoint
        
        Args:
            agent_id: The agent address to categorize
            
        Returns:
            MeTTaCategorizationResponse if successful, None if failed
        """
        if not self.session:
            raise RuntimeError("MeTTaClient must be used as async context manager")
        
        url = f"{self.base_url}/categorize-agent"
        payload = {
            "agent_id": agent_id,
            "include_features": True,
            "include_crypto_details": True
        }
        
        try:
            print(f"🔗 Calling meTTa agent at {url} for agent {agent_id}")
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ meTTa categorization successful: {data.get('evaluation_method', 'unknown')}")
                    
                    # Parse the response into our structured format
                    return self._parse_categorization_response(data)
                else:
                    print(f"❌ meTTa agent returned status {response.status}")
                    return None
                    
        except asyncio.TimeoutError:
            print(f"⏰ meTTa agent request timed out after {self.timeout}s")
            return None
        except Exception as e:
            print(f"❌ Error calling meTTa agent: {e}")
            return None
    
    def _parse_categorization_response(self, data: Dict[str, Any]) -> MeTTaCategorizationResponse:
        """Parse meTTa agent response into structured format"""
        
        # Parse primary category
        primary_cat_data = data.get("primary_category", {})
        primary_category = CategoryResult(
            category_type=primary_cat_data.get("category_type", "unknown"),
            confidence=primary_cat_data.get("confidence", 0.0),
            keywords_matched=primary_cat_data.get("keywords_matched", []),
            reasoning=primary_cat_data.get("reasoning", "No reasoning provided")
        )
        
        # Parse secondary categories
        secondary_categories = []
        for sec_cat_data in data.get("secondary_categories", []):
            secondary_categories.append(CategoryResult(
                category_type=sec_cat_data.get("category_type", "unknown"),
                confidence=sec_cat_data.get("confidence", 0.0),
                keywords_matched=sec_cat_data.get("keywords_matched", []),
                reasoning=sec_cat_data.get("reasoning", "No reasoning provided")
            ))
        
        # Parse extracted features
        features_data = data.get("extracted_features")
        extracted_features = None
        if features_data:
            extracted_features = FeatureExtractionResult(
                tech_stack=features_data.get("tech_stack", []),
                supported_chains=features_data.get("supported_chains", []),
                protocols=features_data.get("protocols", []),
                key_features=features_data.get("key_features", []),
                capabilities=features_data.get("capabilities", []),
                integrations=features_data.get("integrations", []),
                target_audience=features_data.get("target_audience"),
                business_model=features_data.get("business_model")
            )
        
        return MeTTaCategorizationResponse(
            agent_id=data.get("agent_id", "unknown"),
            primary_category=primary_category,
            secondary_categories=secondary_categories,
            extracted_features=extracted_features,
            crypto_details=data.get("crypto_details"),
            is_unknown_category=data.get("is_unknown_category", True),
            evaluation_method=data.get("evaluation_method", "unknown"),
            processing_time=data.get("processing_time", 0.0),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat())
        )


# Convenience function for one-off categorization calls
async def categorize_agent_with_metta(agent_id: str) -> Optional[MeTTaCategorizationResponse]:
    """
    Convenience function to categorize an agent using meTTa
    
    Args:
        agent_id: The agent address to categorize
        
    Returns:
        MeTTaCategorizationResponse if successful, None if failed
    """
    async with MeTTaClient() as client:
        return await client.categorize_agent(agent_id)


if __name__ == "__main__":
    # Test the client
    async def test_client():
        test_agent_id = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
        
        print("🧪 Testing meTTa client...")
        result = await categorize_agent_with_metta(test_agent_id)
        
        if result:
            print(f"✅ Test successful!")
            print(f"   Agent: {result.agent_id}")
            print(f"   Primary Category: {result.primary_category.category_type}")
            print(f"   Confidence: {result.primary_category.confidence}")
            print(f"   Method: {result.evaluation_method}")
        else:
            print("❌ Test failed")
    
    asyncio.run(test_client())
