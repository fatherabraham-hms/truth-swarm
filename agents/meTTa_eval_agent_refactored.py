#!/usr/bin/env python3
"""
Crypto Detection Agent - Detects crypto-related agents using meTTa framework
and AgentVerse integration for comprehensive agent analysis.
"""

import os
import time
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from uuid import uuid4

from uagents import Agent, Context, Protocol

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    import os
    # Load .env from parent directory (truth-swarm root)
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from: {env_path}")
except ImportError:
    print("⚠️ python-dotenv not available, using system environment variables only")
    pass

# Import modular components
from models.data_models import (
    AgentProfileData, CryptoDetectionRequest, CryptoDetectionResponse,
    AgentCategorizationRequest, AgentCategorizationResponse,
    FeatureExtractionRequest, FeatureExtractionResponse,
    FeatureExtractionResult, CategoryResult, TaxonomyResponse, 
    ErrorResponse, HealthResponse, AgentListRequest, AgentListResponse, 
    AgentDiscoveryRequest, AgentDiscoveryResponse
)
from detection.metta_detector import MeTTaDetector
from detection.metta_categorizer import MeTTaCategorizer
from detection.simple_detector import SimpleDetector
from api.agentverse_client import AgentverseAPIClient
from utils.category_taxonomy import (
    PRIMARY_CATEGORIES, CRYPTO_SUBCATEGORIES,
    PRIMARY_CATEGORY_THRESHOLD, SECONDARY_CATEGORY_THRESHOLD
)

# Try to import meTTa framework (Hyperon)
try:
    from hyperon import Interpreter
    METTA_AVAILABLE = True
    print("✅ meTTa framework (Hyperon) available")
except ImportError:
    METTA_AVAILABLE = False
    print("⚠️ meTTa framework not available. Install with: pip install hyperon")


# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

# Get deployment environment
railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
agent_port = int(os.getenv("PORT", 8000))
agent_name = os.getenv("AGENT_NAME", "truth_swarm_categorizer_agent")

if railway_url:
    endpoint_url = f"https://{railway_url}/submit"
else:
    endpoint_url = "http://localhost:8000/submit"

# Initialize the crypto detection agent
crypto_detection_agent = Agent(
    name=agent_name,
    seed="crypto_detection_seed_2024_truth_swarm",
    port=agent_port,
    endpoint=[endpoint_url],
    mailbox=True  # Enable mailbox for Agentverse integration
)

# Initialize detection components
metta_detector = MeTTaDetector() if METTA_AVAILABLE else None
metta_categorizer = MeTTaCategorizer() if METTA_AVAILABLE else None
simple_detector = SimpleDetector()

# Initialize AgentVerse API client
agentverse_api_key = os.getenv("AGENTVERSE_API_KEY")
agentverse_base_url = os.getenv("AGENTVERSE_BASE_URL", "https://agentverse.ai")
agentverse_client = None

if agentverse_api_key:
    try:
        agentverse_client = AgentverseAPIClient(agentverse_api_key, agentverse_base_url)
        print("✅ AgentVerse API client initialized")
    except Exception as e:
        print(f"❌ Failed to initialize AgentVerse API client: {e}")
        agentverse_client = None
else:
    print("⚠️ AGENTVERSE_API_KEY not found in environment variables")

# Agent capabilities
AGENT_CAPABILITIES = [
    "multi_category_detection",
    "crypto_agent_detection", 
    "agent_categorization",
    "feature_extraction",
    "agent_profile_reading",
    "agentverse_integration"
]


# ============================================================================
# CORE DETECTION LOGIC
# ============================================================================

async def detect_crypto_agent(agent_profile: AgentProfileData) -> Dict[str, Any]:
    """
    Detect if an agent is a crypto agent by analyzing README content for crypto keywords.
    Uses meTTa framework if available, otherwise falls back to simple detection.
    """
    if metta_detector and metta_detector.is_available():
        try:
            return await metta_detector.detect_crypto_agent(agent_profile)
        except Exception as e:
            print(f"❌ meTTa detection failed, falling back to simple: {e}")
            return await simple_detector.detect_crypto_agent(agent_profile)
    else:
        return await simple_detector.detect_crypto_agent(agent_profile)


async def categorize_agent(agent_profile: AgentProfileData) -> Dict[str, Any]:
    """
    Categorize an agent into primary and secondary categories using meTTa framework.
    Falls back to simple detection if meTTa is not available.
    """
    if metta_categorizer and metta_categorizer.is_available():
        try:
            return await metta_categorizer.categorize_agent(agent_profile)
        except Exception as e:
            print(f"❌ meTTa categorization failed, falling back to simple: {e}")
            return await simple_detector.categorize_agent(agent_profile)
    else:
        return await simple_detector.categorize_agent(agent_profile)


async def extract_features(agent_profile: AgentProfileData) -> FeatureExtractionResult:
    """
    Extract features from agent profile using meTTa framework.
    Falls back to simple extraction if meTTa is not available.
    """
    if metta_categorizer and metta_categorizer.is_available():
        try:
            return await metta_categorizer.extract_features(agent_profile)
        except Exception as e:
            print(f"❌ meTTa feature extraction failed, falling back to simple: {e}")
            return await simple_detector.extract_features(agent_profile)
    else:
        return await simple_detector.extract_features(agent_profile)


async def read_agent_profile(agent_id: str) -> AgentProfileData:
    """
    Read agent profile and README from AgentVerse using the official API.
    """
    if not agentverse_client:
        # Return a mock profile for testing when API is not available
        return AgentProfileData(
            agent_id=agent_id,
            agent_name=f"Agent_{agent_id}",
            description=f"Mock agent profile for testing. Agent ID: {agent_id}",
            capabilities=["crypto", "blockchain", "trading", "defi"],
            readme_content=f"""# Agent {agent_id}

This is a mock agent profile for testing purposes.

## Capabilities
- Crypto trading
- Blockchain analysis
- DeFi protocols
- Smart contract interaction

## Description
This agent specializes in cryptocurrency and blockchain technologies.
It can analyze market trends, execute trades, and interact with DeFi protocols.

## Features
- Real-time crypto price monitoring
- Automated trading strategies
- Portfolio management
- Risk assessment
""",
            profile_url=f"https://agentverse.ai/agents/{agent_id}",
            last_updated=datetime.now(timezone.utc).isoformat(),
            source="mock_for_testing"
        )
    
    try:
        # Get agent details using the API client
        print(f"🔍 Fetching details for agent: {agent_id}")
        agent_data = await agentverse_client.get_agent_details(agent_id)
        print(f"📊 Agent data received: {agent_data is not None}")
        
        if not agent_data:
            # Try to find the agent in the list as a fallback
            print(f"⚠️ Individual agent details failed, trying to find in agent list...")
            agents_list = await agentverse_client.get_agents()
            agent_data = None
            for agent in agents_list:
                if agent.get('address') == agent_id or agent.get('agent_address') == agent_id:
                    agent_data = agent
                    print(f"✅ Found agent in list: {agent.get('name', 'Unknown')}")
                    break
            
            if not agent_data:
                raise Exception(f"Agent {agent_id} not found on AgentVerse")
        
        # Get agent README from agent details (not code endpoint)
        readme_content = agent_data.get("readme", "")
        
        if not readme_content:
            readme_content = "# Agent README\n\nNo README content available for this agent."
        
        # Debug: Print README content
        print(f"🔍 DEBUG: README content retrieved: {len(readme_content)} characters")
        print(f"🔍 DEBUG: README preview: {readme_content[:300]}...")
        
        # Extract agent information
        agent_name = agent_data.get("name", agent_data.get("agent_name", f"Agent_{agent_id}"))
        description = agent_data.get("description", agent_data.get("summary", "No description available"))
        
        # Extract capabilities from various possible fields
        capabilities = []
        if "capabilities" in agent_data:
            capabilities = agent_data["capabilities"]
        elif "tags" in agent_data:
            capabilities = agent_data["tags"]
        elif "skills" in agent_data:
            capabilities = agent_data["skills"]
        
        # Ensure capabilities is a list
        if not isinstance(capabilities, list):
            capabilities = [str(capabilities)] if capabilities else []
        
        return AgentProfileData(
            agent_id=agent_id,
            agent_name=agent_name,
            description=description,
            capabilities=capabilities,
            readme_content=readme_content,
            profile_url=f"https://agentverse.ai/agents/{agent_id}",
            last_updated=agent_data.get("updated_at", agent_data.get("last_updated", datetime.now(timezone.utc).isoformat())),
            source="agentverse_api"
        )
            
    except Exception as e:
        print(f"⚠️ API error for agent {agent_id}: {str(e)}, using mock data")
        return AgentProfileData(
            agent_id=agent_id,
            agent_name=f"Agent_{agent_id}",
            description=f"Mock agent profile for testing. Agent ID: {agent_id}",
            capabilities=["crypto", "blockchain", "trading", "defi"],
            readme_content=f"""# Agent {agent_id}

This is a mock agent profile for testing purposes.

## Capabilities
- Crypto trading
- Blockchain analysis
- DeFi protocols
- Smart contract interaction

## Description
This agent specializes in cryptocurrency and blockchain technologies.
It can analyze market trends, execute trades, and interact with DeFi protocols.

## Features
- Real-time crypto price monitoring
- Automated trading strategies
- Portfolio management
- Risk assessment
""",
            profile_url=f"https://agentverse.ai/agents/{agent_id}",
            last_updated=datetime.now(timezone.utc).isoformat(),
            source="mock_error_fallback"
        )


def calculate_match_score(agent: Dict[str, Any], search_term: str, capabilities: List[str]) -> float:
    """Calculate a match score for agent discovery"""
    score = 0.0
    
    # Name match (highest weight)
    if search_term and search_term in agent.get("name", "").lower():
        score += 0.5
    
    # Description match
    if search_term and search_term in agent.get("description", "").lower():
        score += 0.3
    
    # Capability matches
    agent_caps = [cap.lower() for cap in agent.get("capabilities", agent.get("tags", []))]
    for cap in capabilities:
        if any(cap in agent_cap for agent_cap in agent_caps):
            score += 0.2
    
    return min(score, 1.0)


# ============================================================================
# PROTOCOLS
# ============================================================================

# Crypto detection protocol
crypto_detection_protocol = Protocol(name="crypto_detection_protocol", version="1.0")

@crypto_detection_protocol.on_message(model=CryptoDetectionRequest, replies={CryptoDetectionResponse, ErrorResponse})
async def handle_crypto_detection_request(ctx: Context, sender: str, msg: CryptoDetectionRequest):
    """Handle crypto agent detection requests"""
    try:
        ctx.logger.info(f"📨 Received crypto detection request for {msg.agent_id} from {sender}")
        
        # Read agent profile from AgentVerse
        start_time = time.time()
        agent_profile = await read_agent_profile(msg.agent_id)
        profile_time = time.time() - start_time
        
        ctx.logger.info(f"📖 Agent profile read in {profile_time:.2f}s")
        
        # Detect crypto agent
        eval_start_time = time.time()
        detection_result = await detect_crypto_agent(agent_profile)
        eval_time = time.time() - eval_start_time
        
        # Create response
        response = CryptoDetectionResponse(
            agent_id=msg.agent_id,
            is_crypto_agent=detection_result.get("is_crypto_agent", False),
            crypto_score=detection_result.get("crypto_score", 0.0),
            confidence=detection_result.get("confidence", 0.0),
            total_matches=detection_result.get("total_matches", 0),
            readme_matches=detection_result.get("readme_matches", []),
            capability_matches=detection_result.get("capability_matches", []),
            description_matches=detection_result.get("description_matches", []),
            evaluation_method=detection_result.get("evaluation_method", "unknown"),
            processing_time=profile_time + eval_time,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        ctx.logger.info(f"✅ Crypto detection completed in {profile_time + eval_time:.2f}s")
        await ctx.send(sender, response)
        
    except Exception as e:
        ctx.logger.error(f"❌ Crypto detection failed for {msg.agent_id}: {e}")
        await ctx.send(sender, ErrorResponse(
            request_id=str(uuid4()),
            error=str(e),
            error_code="CRYPTO_DETECTION_ERROR",
            timestamp=datetime.now(timezone.utc).isoformat()
        ))


# ============================================================================
# EVENT HANDLERS
# ============================================================================

@crypto_detection_agent.on_event("startup")
async def startup(ctx: Context):
    """Handle agent startup"""
    ctx.logger.info("🚀 Crypto Detection Agent started successfully!")
    ctx.logger.info(f"📍 Agent address: {crypto_detection_agent.address}")
    ctx.logger.info(f"🔧 Port: {agent_port}")
    ctx.logger.info(f"🌐 Endpoint: {endpoint_url}")
    ctx.logger.info(f"🛠️ Capabilities: {', '.join(AGENT_CAPABILITIES)}")
    
    # Show meTTa status
    ctx.logger.info("🧠 meTTa Framework Status:")
    ctx.logger.info(f"   Available: {METTA_AVAILABLE}")
    ctx.logger.info(f"   Crypto Detector: {'Available' if metta_detector and metta_detector.is_available() else 'Not Available'}")
    ctx.logger.info(f"   Categorizer: {'Available' if metta_categorizer and metta_categorizer.is_available() else 'Not Available'}")
    ctx.logger.info(f"   Detection method: {'meTTa symbolic reasoning' if metta_categorizer and metta_categorizer.is_available() else 'simple keyword matching'}")
    
    # Show AgentVerse API status
    ctx.logger.info("🌐 AgentVerse API Status:")
    ctx.logger.info(f"   Available: {agentverse_client is not None}")
    ctx.logger.info(f"   API Key: {'Set' if agentverse_api_key else 'Not Set'}")
    ctx.logger.info(f"   Base URL: {agentverse_base_url}")
    ctx.logger.info(f"   Profile reading: {'Enabled' if agentverse_client else 'Disabled'}")
    
    # Test Agentverse connection if available
    if agentverse_client:
        ctx.logger.info("🔗 Testing Agentverse connection...")
        try:
            connection_ok = await agentverse_client.test_connection()
            if connection_ok:
                ctx.logger.info("✅ Agentverse connection successful!")
                
                # Try to get agent count
                try:
                    agents = await agentverse_client.get_agents()
                    ctx.logger.info(f"📊 Found {len(agents)} agents on Agentverse")
                except Exception as e:
                    ctx.logger.warning(f"⚠️ Could not fetch agent list: {e}")
            else:
                ctx.logger.warning("⚠️ Agentverse connection failed - will use fallback mode")
        except Exception as e:
            ctx.logger.warning(f"⚠️ Agentverse connection test failed: {e}")
    else:
        ctx.logger.info("ℹ️ Agentverse API not available - using fallback mode")
    
    ctx.logger.info("💡 Ready to detect crypto agents!")


@crypto_detection_agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """Handle agent shutdown"""
    ctx.logger.info("🛑 Crypto Detection Agent shutting down...")
    ctx.logger.info("🧹 Cleaning up resources...")
    ctx.logger.info("✅ Shutdown complete")


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@crypto_detection_agent.on_rest_get("/health", HealthResponse)
async def health_endpoint(ctx: Context) -> HealthResponse:
    """Health check endpoint"""
    ctx.logger.info("💓 Health check requested")
    
    return HealthResponse(
        status="healthy",
        agent_name="crypto_detection_agent",
        agent_address=str(crypto_detection_agent.address),
        uptime=datetime.now(timezone.utc).isoformat(),
        metta_available=METTA_AVAILABLE,
        agentverse_available=agentverse_client is not None
    )


@crypto_detection_agent.on_rest_post("/detect-crypto", CryptoDetectionRequest, CryptoDetectionResponse)
async def detect_crypto_endpoint(ctx: Context, request: CryptoDetectionRequest) -> CryptoDetectionResponse:
    """Crypto agent detection endpoint for direct REST API calls"""
    ctx.logger.info(f"📨 REST crypto detection request for: {request.agent_id}")
    
    try:
        # Read agent profile from AgentVerse
        start_time = time.time()
        agent_profile = await read_agent_profile(request.agent_id)
        profile_time = time.time() - start_time
        
        # Detect crypto agent
        eval_start_time = time.time()
        detection_result = await detect_crypto_agent(agent_profile)
        eval_time = time.time() - eval_start_time
        
        return CryptoDetectionResponse(
            agent_id=request.agent_id,
            is_crypto_agent=detection_result.get("is_crypto_agent", False),
            crypto_score=detection_result.get("crypto_score", 0.0),
            confidence=detection_result.get("confidence", 0.0),
            total_matches=detection_result.get("total_matches", 0),
            readme_matches=detection_result.get("readme_matches", []),
            capability_matches=detection_result.get("capability_matches", []),
            description_matches=detection_result.get("description_matches", []),
            evaluation_method=detection_result.get("evaluation_method", "unknown"),
            processing_time=profile_time + eval_time,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST crypto detection failed: {e}")
        # Return a fallback response instead of raising an exception
        return CryptoDetectionResponse(
            agent_id=request.agent_id,
            is_crypto_agent=False,
            crypto_score=0.0,
            confidence=0.0,
            total_matches=0,
            readme_matches=[],
            capability_matches=[],
            description_matches=[],
            evaluation_method="error_fallback",
            processing_time=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )


@crypto_detection_agent.on_rest_post("/list-agents", AgentListRequest, AgentListResponse)
async def list_agents_endpoint(ctx: Context, request: AgentListRequest) -> AgentListResponse:
    """List agents from Agentverse"""
    ctx.logger.info(f"📨 REST agent list request: limit={request.limit}, offset={request.offset}")
    
    if not agentverse_client:
        return AgentListResponse(
            agents=[],
            total_count=0,
            limit=request.limit,
            offset=request.offset,
            agentverse_available=False
        )
    
    try:
        # Get agents from Agentverse
        agents_data = await agentverse_client.get_agents()
        
        # Apply pagination
        total_count = len(agents_data)
        start_idx = request.offset
        end_idx = min(request.offset + request.limit, total_count)
        paginated_agents = agents_data[start_idx:end_idx]
        
        # Format agent data for response
        formatted_agents = []
        for agent in paginated_agents:
            formatted_agent = {
                "agent_id": agent.get("address", agent.get("id", "unknown")),
                "name": agent.get("name", "Unknown Agent"),
                "description": agent.get("description", "No description available"),
                "status": agent.get("status", "unknown"),
                "created_at": agent.get("created_at", ""),
                "updated_at": agent.get("updated_at", ""),
                "capabilities": agent.get("capabilities", agent.get("tags", [])),
                "profile_url": f"https://agentverse.ai/agents/{agent.get('address', agent.get('id', 'unknown'))}"
            }
            formatted_agents.append(formatted_agent)
        
        return AgentListResponse(
            agents=formatted_agents,
            total_count=total_count,
            limit=request.limit,
            offset=request.offset,
            agentverse_available=True
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST agent list failed: {e}")
        return AgentListResponse(
            agents=[],
            total_count=0,
            limit=request.limit,
            offset=request.offset,
            agentverse_available=False
        )


@crypto_detection_agent.on_rest_post("/discover-agents", AgentDiscoveryRequest, AgentDiscoveryResponse)
async def discover_agents_endpoint(ctx: Context, request: AgentDiscoveryRequest) -> AgentDiscoveryResponse:
    """Discover agents based on search terms and capabilities"""
    ctx.logger.info(f"📨 REST agent discovery request: search='{request.search_term}', capabilities={request.capabilities}")
    
    if not agentverse_client:
        return AgentDiscoveryResponse(
            matching_agents=[],
            total_found=0,
            search_term=request.search_term,
            capabilities_searched=request.capabilities,
            agentverse_available=False
        )
    
    try:
        # Get all agents from Agentverse
        agents_data = await agentverse_client.get_agents()
        
        # Filter agents based on search criteria
        matching_agents = []
        search_term_lower = request.search_term.lower() if request.search_term else ""
        capabilities_lower = [cap.lower() for cap in request.capabilities] if request.capabilities else []
        
        for agent in agents_data:
            agent_name = agent.get("name", "").lower()
            agent_desc = agent.get("description", "").lower()
            agent_caps = [cap.lower() for cap in agent.get("capabilities", agent.get("tags", []))]
            
            # Check if agent matches search criteria
            matches_search = not search_term_lower or (
                search_term_lower in agent_name or 
                search_term_lower in agent_desc
            )
            
            matches_capabilities = not capabilities_lower or any(
                any(cap in agent_cap for cap in capabilities_lower) 
                for agent_cap in agent_caps
            )
            
            if matches_search and matches_capabilities:
                formatted_agent = {
                    "agent_id": agent.get("address", agent.get("id", "unknown")),
                    "name": agent.get("name", "Unknown Agent"),
                    "description": agent.get("description", "No description available"),
                    "status": agent.get("status", "unknown"),
                    "capabilities": agent.get("capabilities", agent.get("tags", [])),
                    "profile_url": f"https://agentverse.ai/agents/{agent.get('address', agent.get('id', 'unknown'))}",
                    "match_score": calculate_match_score(agent, search_term_lower, capabilities_lower)
                }
                matching_agents.append(formatted_agent)
        
        # Sort by match score (highest first)
        matching_agents.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        
        # Apply limit
        if request.limit > 0:
            matching_agents = matching_agents[:request.limit]
        
        return AgentDiscoveryResponse(
            matching_agents=matching_agents,
            total_found=len(matching_agents),
            search_term=request.search_term,
            capabilities_searched=request.capabilities,
            agentverse_available=True
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST agent discovery failed: {e}")
        return AgentDiscoveryResponse(
            matching_agents=[],
            total_found=0,
            search_term=request.search_term,
            capabilities_searched=request.capabilities,
            agentverse_available=False
        )


# ============================================================================
# NEW MULTI-CATEGORY ENDPOINTS
# ============================================================================

@crypto_detection_agent.on_rest_post("/categorize-agent", AgentCategorizationRequest, AgentCategorizationResponse)
async def categorize_agent_endpoint(ctx: Context, request: AgentCategorizationRequest) -> AgentCategorizationResponse:
    """Comprehensive agent categorization endpoint"""
    ctx.logger.info(f"📨 REST agent categorization request for: {request.agent_id}")
    
    try:
        # Read agent profile from AgentVerse
        start_time = time.time()
        agent_profile = await read_agent_profile(request.agent_id)
        profile_time = time.time() - start_time
        
        # Categorize agent
        eval_start_time = time.time()
        categorization_result = await categorize_agent(agent_profile)
        eval_time = time.time() - eval_start_time
        
        # Extract features if requested
        features = None
        if request.include_features:
            features = await extract_features(agent_profile)
        
        # Get crypto details if requested and primary category is crypto
        crypto_details = None
        if request.include_crypto_details and categorization_result.get("primary_category", {}).get("category_type") == "crypto":
            crypto_details = categorization_result.get("crypto_details")
        
        return AgentCategorizationResponse(
            agent_id=request.agent_id,
            primary_category=categorization_result["primary_category"],
            secondary_categories=categorization_result.get("secondary_categories", []),
            extracted_features=features,
            crypto_details=crypto_details,
            is_unknown_category=categorization_result.get("is_unknown_category", False),
            evaluation_method=categorization_result.get("evaluation_method", "unknown"),
            processing_time=profile_time + eval_time,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST agent categorization failed: {e}")
        # Return a fallback response
        return AgentCategorizationResponse(
            agent_id=request.agent_id,
            primary_category=CategoryResult(
                category_type="unknown",
                confidence=0.0,
                keywords_matched=[],
                reasoning="Error during categorization"
            ),
            secondary_categories=[],
            extracted_features=None,
            crypto_details=None,
            is_unknown_category=True,
            evaluation_method="error_fallback",
            processing_time=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )


@crypto_detection_agent.on_rest_post("/extract-features", FeatureExtractionRequest, FeatureExtractionResponse)
async def extract_features_endpoint(ctx: Context, request: FeatureExtractionRequest) -> FeatureExtractionResponse:
    """Standalone feature extraction endpoint"""
    ctx.logger.info(f"📨 REST feature extraction request for: {request.agent_id}")
    
    try:
        # Read agent profile from AgentVerse
        start_time = time.time()
        agent_profile = await read_agent_profile(request.agent_id)
        profile_time = time.time() - start_time
        
        # Extract features
        eval_start_time = time.time()
        features = await extract_features(agent_profile)
        eval_time = time.time() - eval_start_time
        
        return FeatureExtractionResponse(
            agent_id=request.agent_id,
            features=features,
            processing_time=profile_time + eval_time,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST feature extraction failed: {e}")
        # Return a fallback response
        return FeatureExtractionResponse(
            agent_id=request.agent_id,
            features=FeatureExtractionResult(
                tech_stack=[],
                supported_chains=[],
                protocols=[],
                key_features=[],
                capabilities=[],
                integrations=[],
                target_audience="unknown",
                business_model="unknown"
            ),
            processing_time=0.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )


@crypto_detection_agent.on_rest_get("/get-taxonomy", TaxonomyResponse)
async def get_taxonomy_endpoint(ctx: Context) -> TaxonomyResponse:
    """Get category taxonomy information"""
    ctx.logger.info("📨 REST taxonomy request")
    
    try:
        # Format primary categories
        primary_categories = []
        for category_name, category_def in PRIMARY_CATEGORIES.items():
            primary_categories.append({
                "name": category_def.name,
                "key": category_name,
                "description": category_def.description,
                "keyword_count": len(category_def.keywords),
                "weight": category_def.weight
            })
        
        # Format crypto subcategories
        crypto_subcategories = []
        for subcategory_name, subcategory_def in CRYPTO_SUBCATEGORIES.items():
            crypto_subcategories.append({
                "name": subcategory_def.name,
                "key": subcategory_name,
                "description": subcategory_def.description,
                "keyword_count": len(subcategory_def.keywords),
                "weight": subcategory_def.weight,
                "parent": subcategory_def.parent
            })
        
        return TaxonomyResponse(
            primary_categories=primary_categories,
            crypto_subcategories=crypto_subcategories,
            total_primary_categories=len(PRIMARY_CATEGORIES),
            total_crypto_subcategories=len(CRYPTO_SUBCATEGORIES),
            confidence_thresholds={
                "primary_category": PRIMARY_CATEGORY_THRESHOLD,
                "secondary_category": SECONDARY_CATEGORY_THRESHOLD
            }
        )
        
    except Exception as e:
        ctx.logger.error(f"❌ REST taxonomy request failed: {e}")
        return TaxonomyResponse(
            primary_categories=[],
            crypto_subcategories=[],
            total_primary_categories=0,
            total_crypto_subcategories=0,
            confidence_thresholds={}
        )


# ============================================================================
# PROTOCOL INTEGRATION
# ============================================================================

# Include the crypto detection protocol in the agent
crypto_detection_agent.include(crypto_detection_protocol, publish_manifest=True)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("""
🤖 Starting Crypto Detection Agent...

This agent detects crypto-related agents by analyzing their AgentVerse profiles
using meTTa framework symbolic reasoning and comprehensive keyword matching.

📋 Available capabilities:
   • Crypto agent detection using meTTa
   • Agent profile reading from AgentVerse
   • AgentVerse API integration

🧠 meTTa Framework:
   • Status: {'Available' if METTA_AVAILABLE else 'Not Available'}
   • Detector: {'Available' if metta_detector and metta_detector.is_available() else 'Not Available'}
   • Detection: {'meTTa symbolic reasoning' if metta_detector and metta_detector.is_available() else 'Simple fallback'}

🌐 AgentVerse API Integration:
   • Status: {'Available' if agentverse_client else 'Not Available'}
   • API Key: {'Set' if agentverse_api_key else 'Not Set'}
   • Base URL: {agentverse_base_url}
   • Profile Reading: {'Enabled' if agentverse_client else 'Disabled'}

🌐 REST API endpoints:
   • GET  /health              - Health check
   • POST /detect-crypto       - Detect crypto agent by ID (backward compatible)
   • POST /categorize-agent    - Comprehensive agent categorization
   • POST /extract-features    - Standalone feature extraction
   • GET  /get-taxonomy        - Get category taxonomy information
   • POST /list-agents         - List agents from Agentverse
   • POST /discover-agents     - Discover agents by search/capabilities

🔗 Test commands:
   # Health check
   curl http://localhost:8000/health
   
   # Comprehensive agent categorization (NEW!)
   curl -X POST http://localhost:8000/categorize-agent \\
        -H "Content-Type: application/json" \\
        -d '{"agent_id": "example-agent-123", "include_features": true, "include_crypto_details": true}'
   
   # Feature extraction only
   curl -X POST http://localhost:8000/extract-features \\
        -H "Content-Type: application/json" \\
        -d '{"agent_id": "example-agent-123"}'
   
   # Get category taxonomy
   curl http://localhost:8000/get-taxonomy
   
   # Crypto agent detection (backward compatible)
   curl -X POST http://localhost:8000/detect-crypto \\
        -H "Content-Type: application/json" \\
        -d '{"agent_id": "example-agent-123"}'
   
   # List agents from Agentverse
   curl -X POST http://localhost:8000/list-agents \\
        -H "Content-Type: application/json" \\
        -d '{"limit": 10, "offset": 0}'
   
   # Discover agents by search term
   curl -X POST http://localhost:8000/discover-agents \\
        -H "Content-Type: application/json" \\
        -d '{"search_term": "crypto", "capabilities": ["trading"], "limit": 5}'

🛑 Stop with Ctrl+C
    """)
    
    crypto_detection_agent.run()
