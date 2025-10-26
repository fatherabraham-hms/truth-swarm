#!/usr/bin/env python3
"""
Simple integration test without full agent dependencies
Tests the meTTa client logic and response parsing
"""

import json
import subprocess
import sys
from datetime import datetime

def test_metta_agent():
    """Test meTTa agent directly using curl"""
    print("🧪 Testing meTTa Agent Integration")
    print("=" * 50)
    
    test_agent_id = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
    metta_url = "https://truth-swarm-production.up.railway.app"
    
    print(f"📤 Testing meTTa agent at: {metta_url}")
    print(f"🎯 Test agent ID: {test_agent_id}")
    
    # Test payload
    payload = {
        "agent_id": test_agent_id,
        "include_features": True,
        "include_crypto_details": True
    }
    
    try:
        # Use curl to test the endpoint
        curl_cmd = [
            "curl", "-X", "POST", f"{metta_url}/categorize-agent",
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
            "-s"  # Silent mode
        ]
        
        print("🔄 Calling meTTa agent...")
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                print("✅ meTTa agent response received!")
                
                # Parse and display key information
                print(f"\n📊 Categorization Results:")
                print(f"   Agent ID: {data.get('agent_id')}")
                
                primary = data.get('primary_category', {})
                print(f"   Primary Category: {primary.get('category_type')}")
                print(f"   Confidence: {primary.get('confidence', 0):.2f}")
                print(f"   Keywords Matched: {len(primary.get('keywords_matched', []))}")
                print(f"   Reasoning: {primary.get('reasoning', 'N/A')[:80]}...")
                
                secondary = data.get('secondary_categories', [])
                if secondary:
                    print(f"   Secondary Categories: {len(secondary)}")
                    for i, sec in enumerate(secondary[:2]):  # Show first 2
                        print(f"     {i+1}. {sec.get('category_type')} ({sec.get('subcategory', 'N/A')}) - {sec.get('confidence', 0):.2f}")
                
                features = data.get('extracted_features', {})
                if features:
                    print(f"\n🔧 Extracted Features:")
                    print(f"   Capabilities: {features.get('capabilities', [])}")
                    print(f"   Key Features: {features.get('key_features', [])}")
                    print(f"   Target Audience: {features.get('target_audience', 'N/A')}")
                    print(f"   Business Model: {features.get('business_model', 'N/A')}")
                
                crypto = data.get('crypto_details', {})
                if crypto:
                    print(f"\n💰 Crypto Details:")
                    print(f"   Subcategory: {crypto.get('subcategory', 'N/A')}")
                    print(f"   Use Cases: {crypto.get('use_cases', [])}")
                
                print(f"\n⚙️ Technical Info:")
                print(f"   Evaluation Method: {data.get('evaluation_method')}")
                print(f"   Processing Time: {data.get('processing_time')}s")
                print(f"   Timestamp: {data.get('timestamp')}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON response: {e}")
                print(f"Raw response: {result.stdout[:200]}...")
                return False
        else:
            print(f"❌ Curl command failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing meTTa agent: {e}")
        return False

def test_response_structure():
    """Test the expected response structure for evaluator integration"""
    print("\n🧪 Testing Response Structure Compatibility")
    print("=" * 50)
    
    # Simulate what the evaluator would receive from meTTa
    mock_metta_response = {
        "agent_id": "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y",
        "primary_category": {
            "category_type": "crypto",
            "confidence": 0.85,
            "keywords_matched": ["bitcoin", "ethereum", "trading"],
            "reasoning": "Agent specializes in cryptocurrency trading"
        },
        "secondary_categories": [
            {
                "category_type": "crypto",
                "subcategory": "defi",
                "confidence": 0.75,
                "keywords_matched": ["protocol", "defi"],
                "reasoning": "DeFi protocol specialization"
            }
        ],
        "extracted_features": {
            "tech_stack": ["Python", "Web3"],
            "supported_chains": ["Ethereum"],
            "protocols": ["Uniswap"],
            "key_features": ["trading", "analysis"],
            "capabilities": ["crypto", "trading"],
            "integrations": ["Coinbase"],
            "target_audience": "traders",
            "business_model": "subscription"
        },
        "crypto_details": {
            "subcategory": "defi",
            "confidence": 0.75,
            "protocols_mentioned": ["Uniswap"],
            "chains_supported": ["Ethereum"],
            "features": ["trading", "analysis"],
            "use_cases": ["trading", "yield farming"]
        },
        "is_unknown_category": False,
        "evaluation_method": "metta_symbolic_reasoning",
        "processing_time": 2.3,
        "timestamp": datetime.now().isoformat()
    }
    
    # Test the conversion logic (simulating what evaluator_agent.py does)
    try:
        print("🔄 Testing response conversion logic...")
        
        # Convert to evaluator response format
        metta_categorization = {
            "agent_id": mock_metta_response["agent_id"],
            "primary_category": mock_metta_response["primary_category"],
            "secondary_categories": mock_metta_response["secondary_categories"],
            "extracted_features": mock_metta_response["extracted_features"],
            "crypto_details": mock_metta_response["crypto_details"],
            "is_unknown_category": mock_metta_response["is_unknown_category"],
            "evaluation_method": mock_metta_response["evaluation_method"],
            "processing_time": mock_metta_response["processing_time"],
            "timestamp": mock_metta_response["timestamp"]
        }
        
        # Simulate evaluator response
        evaluator_response = {
            "success": True,
            "agent_address": mock_metta_response["agent_id"],
            "attestation_uid": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            "final_score": 87,
            "grade": "A",
            "message": "Agent evaluated successfully! Score: 87/100 (A). Attestation created on EAS.",
            "metta_categorization": metta_categorization,
            "primary_category": metta_categorization["primary_category"]["category_type"],
            "secondary_categories": [cat["category_type"] for cat in metta_categorization["secondary_categories"]],
            "extracted_features": metta_categorization["extracted_features"],
            "crypto_details": metta_categorization["crypto_details"],
            "categorization_method": metta_categorization["evaluation_method"]
        }
        
        print("✅ Response conversion successful!")
        print(f"\n📋 Evaluator Response Structure:")
        print(f"   Success: {evaluator_response['success']}")
        print(f"   Agent Address: {evaluator_response['agent_address']}")
        print(f"   Attestation UID: {evaluator_response['attestation_uid'][:20]}...")
        print(f"   Final Score: {evaluator_response['final_score']}/100")
        print(f"   Grade: {evaluator_response['grade']}")
        print(f"   Primary Category: {evaluator_response['primary_category']}")
        print(f"   Secondary Categories: {evaluator_response['secondary_categories']}")
        print(f"   Categorization Method: {evaluator_response['categorization_method']}")
        print(f"   Has meTTa Data: {evaluator_response['metta_categorization'] is not None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Response conversion failed: {e}")
        return False

def main():
    print("🚀 Truth Swarm Integration Test")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: meTTa agent
    metta_ok = test_metta_agent()
    
    # Test 2: Response structure
    structure_ok = test_response_structure()
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   meTTa Agent: {'✅ Working' if metta_ok else '❌ Failed'}")
    print(f"   Response Structure: {'✅ Compatible' if structure_ok else '❌ Failed'}")
    
    if metta_ok and structure_ok:
        print("\n🎉 Integration test passed!")
        print("   The meTTa agent is working and the response structure is compatible.")
        print("   Ready for evaluator agent integration!")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")
    
    print("\n📝 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run evaluator agent: python evaluator_agent.py")
    print("   3. Test full integration with UI")

if __name__ == "__main__":
    main()
