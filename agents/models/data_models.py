"""Pydantic data models for the agent system"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Union
from uagents import Model


class AgentProfileData(Model):
    """Model for agent profile information"""
    agent_id: str
    agent_name: str
    description: str
    capabilities: List[str] = []
    readme_content: str
    profile_url: str
    last_updated: str
    source: str = "agentverse"


class CryptoDetectionRequest(Model):
    """Request model for crypto agent detection"""
    agent_id: str
    timestamp: str = ""


class CryptoDetectionResponse(Model):
    """Response model for crypto detection results"""
    agent_id: str
    is_crypto_agent: bool
    crypto_score: float
    confidence: float
    total_matches: int
    readme_matches: List[str] = []
    capability_matches: List[str] = []
    description_matches: List[str] = []
    evaluation_method: str
    processing_time: float
    timestamp: str = ""


class ErrorResponse(Model):
    """Error response model"""
    request_id: str
    error: str
    error_code: str = "UNKNOWN_ERROR"
    timestamp: str = ""


class HealthResponse(Model):
    """Health check response model"""
    status: str
    agent_name: str
    agent_address: str
    uptime: str
    metta_available: bool
    agentverse_available: bool
    version: str = "1.0.0"


class AgentListRequest(Model):
    """Request model for listing agents"""
    limit: int = 10
    offset: int = 0


class AgentListResponse(Model):
    """Response model for agent list"""
    agents: List[Dict[str, Any]] = []
    total_count: int = 0
    limit: int = 10
    offset: int = 0
    agentverse_available: bool = False


class AgentDiscoveryRequest(Model):
    """Request model for agent discovery"""
    search_term: str = ""
    capabilities: List[str] = []
    limit: int = 10


class AgentDiscoveryResponse(Model):
    """Response model for agent discovery"""
    matching_agents: List[Dict[str, Any]] = []
    total_found: int = 0
    search_term: str = ""
    capabilities_searched: List[str] = []
    agentverse_available: bool = False


# New models for multi-category detection
class CategoryResult(Model):
    """Result for a single category classification"""
    category_type: str
    subcategory: Optional[str] = None
    confidence: float
    keywords_matched: List[str] = []
    reasoning: Optional[str] = None


class FeatureExtractionResult(Model):
    """Result of feature extraction from agent profile"""
    tech_stack: List[str] = []
    supported_chains: List[str] = []
    protocols: List[str] = []
    key_features: List[str] = []
    capabilities: List[str] = []
    integrations: List[str] = []
    target_audience: Optional[str] = None
    business_model: Optional[str] = None


class CryptoSubcategoryDetails(Model):
    """Detailed information for crypto subcategories"""
    subcategory: str
    confidence: float
    protocols_mentioned: List[str] = []
    chains_supported: List[str] = []
    features: List[str] = []
    use_cases: List[str] = []


class AgentCategorizationRequest(Model):
    """Request model for comprehensive agent categorization"""
    agent_id: str
    include_features: bool = True
    include_crypto_details: bool = True
    multi_category_threshold: float = 0.4
    timestamp: str = ""


class AgentCategorizationResponse(Model):
    """Response model for comprehensive agent categorization"""
    agent_id: str
    primary_category: CategoryResult
    secondary_categories: List[CategoryResult] = []
    extracted_features: Optional[FeatureExtractionResult] = None
    crypto_details: Optional[CryptoSubcategoryDetails] = None
    is_unknown_category: bool = False
    evaluation_method: str
    processing_time: float
    timestamp: str = ""


class FeatureExtractionRequest(Model):
    """Request model for standalone feature extraction"""
    agent_id: str
    timestamp: str = ""


class FeatureExtractionResponse(Model):
    """Response model for feature extraction"""
    agent_id: str
    features: FeatureExtractionResult
    processing_time: float
    timestamp: str = ""


class TaxonomyResponse(Model):
    """Response model for category taxonomy information"""
    primary_categories: List[Dict[str, Any]] = []
    crypto_subcategories: List[Dict[str, Any]] = []
    total_primary_categories: int = 0
    total_crypto_subcategories: int = 0
    confidence_thresholds: Dict[str, float] = {}


# Backward compatibility aliases
CryptoDetectionRequest = AgentCategorizationRequest
CryptoDetectionResponse = AgentCategorizationResponse
