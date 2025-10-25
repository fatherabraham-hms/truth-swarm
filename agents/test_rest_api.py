#!/usr/bin/env python3
"""
Simple REST API test script for the multi-category agent detection system
This bypasses the uAgents REST API and provides direct HTTP endpoints
"""

import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

from meTTa_eval_agent_refactored import (
    read_agent_profile, 
    detect_crypto_agent, 
    categorize_agent, 
    extract_features
)

# Create FastAPI app
app = FastAPI(title="Multi-Category Agent Detection API", version="1.0.0")

# Pydantic models
class AgentRequest(BaseModel):
    agent_id: str

class CategorizationRequest(BaseModel):
    agent_id: str
    include_features: bool = True
    include_crypto_details: bool = True

class FeatureRequest(BaseModel):
    agent_id: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Multi-Category Agent Detection API",
        "version": "1.0.0",
        "endpoints": [
            "GET /health",
            "POST /detect-crypto",
            "POST /categorize-agent", 
            "POST /extract-features"
        ]
    }

@app.post("/detect-crypto")
async def detect_crypto_endpoint(request: AgentRequest):
    """Crypto agent detection endpoint"""
    try:
        print(f"🔍 Detecting crypto agent: {request.agent_id}")
        
        # Read agent profile
        agent_profile = await read_agent_profile(request.agent_id)
        
        # Detect crypto agent
        result = await detect_crypto_agent(agent_profile)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        print(f"❌ Error in crypto detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/categorize-agent")
async def categorize_agent_endpoint(request: CategorizationRequest):
    """Comprehensive agent categorization endpoint"""
    try:
        print(f"🎯 Categorizing agent: {request.agent_id}")
        
        # Read agent profile
        agent_profile = await read_agent_profile(request.agent_id)
        
        # Categorize agent
        result = await categorize_agent(agent_profile)
        
        # Convert Pydantic models to dict for JSON serialization
        serializable_result = {
            "agent_id": request.agent_id,
            "primary_category": {
                "category_type": result["primary_category"].category_type,
                "subcategory": result["primary_category"].subcategory,
                "confidence": result["primary_category"].confidence,
                "keywords_matched": result["primary_category"].keywords_matched,
                "reasoning": result["primary_category"].reasoning
            },
            "secondary_categories": [
                {
                    "category_type": cat.category_type,
                    "subcategory": cat.subcategory,
                    "confidence": cat.confidence,
                    "keywords_matched": cat.keywords_matched,
                    "reasoning": cat.reasoning
                } for cat in result["secondary_categories"]
            ],
            "is_unknown_category": result["is_unknown_category"],
            "evaluation_method": result["evaluation_method"]
        }
        
        # Add extracted features if requested
        if request.include_features and result.get("extracted_features"):
            features = result["extracted_features"]
            serializable_result["extracted_features"] = {
                "tech_stack": features.tech_stack,
                "supported_chains": features.supported_chains,
                "protocols": features.protocols,
                "key_features": features.key_features,
                "capabilities": features.capabilities,
                "integrations": features.integrations,
                "target_audience": features.target_audience,
                "business_model": features.business_model
            }
        
        # Add crypto details if requested
        if request.include_crypto_details and result.get("crypto_details"):
            crypto = result["crypto_details"]
            serializable_result["crypto_details"] = {
                "subcategory": crypto.subcategory,
                "confidence": crypto.confidence,
                "protocols_mentioned": crypto.protocols_mentioned,
                "chains_supported": crypto.chains_supported,
                "features": crypto.features,
                "use_cases": crypto.use_cases
            }
        
        return JSONResponse(content=serializable_result)
        
    except Exception as e:
        print(f"❌ Error in categorization: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-features")
async def extract_features_endpoint(request: FeatureRequest):
    """Feature extraction endpoint"""
    try:
        print(f"🔧 Extracting features for: {request.agent_id}")
        
        # Read agent profile
        agent_profile = await read_agent_profile(request.agent_id)
        
        # Extract features
        features = await extract_features(agent_profile)
        
        return JSONResponse(content={
            "agent_id": request.agent_id,
            "features": features.dict()
        })
        
    except Exception as e:
        print(f"❌ Error in feature extraction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multi-Category Agent Detection API",
        "version": "1.0.0",
        "status": "running",
        "test_agent": "agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac",
        "example_curl": {
            "crypto_detection": "curl -X POST http://localhost:8001/detect-crypto -H 'Content-Type: application/json' -d '{\"agent_id\": \"agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac\"}'",
            "categorization": "curl -X POST http://localhost:8001/categorize-agent -H 'Content-Type: application/json' -d '{\"agent_id\": \"agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac\"}'"
        }
    }

if __name__ == "__main__":
    print("🚀 Starting Multi-Category Agent Detection API")
    print("=" * 50)
    print("📋 Available endpoints:")
    print("   GET  /health              - Health check")
    print("   POST /detect-crypto       - Crypto detection")
    print("   POST /categorize-agent    - Multi-category detection")
    print("   POST /extract-features    - Feature extraction")
    print()
    print("🧪 Test commands:")
    print("   curl http://localhost:8001/health")
    print("   curl -X POST http://localhost:8001/detect-crypto \\")
    print("        -H 'Content-Type: application/json' \\")
    print("        -d '{\"agent_id\": \"agent1qw6r85pxdr6d9393jp5856g3he54a6pay8x96td55n0757su9nkvxxa0tac\"}'")
    print()
    print("🌐 Starting server on http://localhost:8001")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
