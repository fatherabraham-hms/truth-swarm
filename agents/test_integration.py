#!/usr/bin/env python3
"""
Test script for meTTa integration
Tests the evaluator agent with meTTa categorization
"""

import os
import json
import requests
from datetime import datetime

# Test configuration
EVALUATOR_URL = "http://localhost:8000"
TEST_AGENT_ID = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

def test_evaluator_integration():
    """Test the evaluator agent with meTTa integration"""
    
    print("🧪 Testing Evaluator Agent with meTTa Integration")
    print("=" * 60)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    try:
        response = requests.get(f"{EVALUATOR_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Evaluation with meTTa integration
    print("\n2️⃣ Testing evaluation with meTTa integration...")
    
    payload = {
        "agent_address": TEST_AGENT_ID
    }
    
    try:
        print(f"📤 Sending evaluation request for: {TEST_AGENT_ID}")
        response = requests.post(
            f"{EVALUATOR_URL}/evaluate",
            json=payload,
            timeout=30  # Longer timeout for meTTa call
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Evaluation successful!")
            
            # Check basic evaluation data
            print(f"   Agent: {data.get('agent_address')}")
            print(f"   Success: {data.get('success')}")
            print(f"   Score: {data.get('final_score')}/100")
            print(f"   Grade: {data.get('grade')}")
            print(f"   Attestation UID: {data.get('attestation_uid')}")
            
            # Check meTTa integration data
            if data.get('primary_category'):
                print(f"   Primary Category: {data.get('primary_category')}")
                print(f"   Categorization Method: {data.get('categorization_method')}")
                
                if data.get('metta_categorization'):
                    metta = data['metta_categorization']
                    print(f"   meTTa Confidence: {metta.get('primary_category', {}).get('confidence', 'N/A')}")
                    print(f"   Keywords Matched: {len(metta.get('primary_category', {}).get('keywords_matched', []))}")
                    
                    if metta.get('extracted_features'):
                        features = metta['extracted_features']
                        print(f"   Tech Stack: {features.get('tech_stack', [])}")
                        print(f"   Capabilities: {features.get('capabilities', [])}")
                        print(f"   Target Audience: {features.get('target_audience', 'N/A')}")
                
                print("✅ meTTa integration working!")
            else:
                print("⚠️ No meTTa categorization data (may be expected if meTTa unavailable)")
            
            return True
            
        else:
            print(f"❌ Evaluation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Evaluation error: {e}")
        return False

def test_metta_direct():
    """Test meTTa agent directly"""
    print("\n3️⃣ Testing meTTa agent directly...")
    
    metta_url = "https://truth-swarm-production.up.railway.app"
    payload = {
        "agent_id": TEST_AGENT_ID,
        "include_features": True,
        "include_crypto_details": True
    }
    
    try:
        response = requests.post(
            f"{metta_url}/categorize-agent",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ meTTa agent working!")
            print(f"   Primary Category: {data.get('primary_category', {}).get('category_type')}")
            print(f"   Confidence: {data.get('primary_category', {}).get('confidence')}")
            print(f"   Method: {data.get('evaluation_method')}")
            return True
        else:
            print(f"❌ meTTa agent failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ meTTa agent error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Integration Tests")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test meTTa agent directly first
    metta_ok = test_metta_direct()
    
    if metta_ok:
        # Test evaluator integration
        evaluator_ok = test_evaluator_integration()
        
        print("\n" + "=" * 60)
        print("📊 Test Results:")
        print(f"   meTTa Agent: {'✅ Working' if metta_ok else '❌ Failed'}")
        print(f"   Evaluator Integration: {'✅ Working' if evaluator_ok else '❌ Failed'}")
        
        if metta_ok and evaluator_ok:
            print("\n🎉 All tests passed! Integration is working correctly.")
        else:
            print("\n⚠️ Some tests failed. Check the logs above.")
    else:
        print("\n❌ meTTa agent not available - cannot test integration")
    
    print("\n🛑 Test completed")
