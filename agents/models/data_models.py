"""Pydantic data models for the agent system"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
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
