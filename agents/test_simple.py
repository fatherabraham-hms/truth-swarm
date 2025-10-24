#!/usr/bin/env python3
"""
Simple test script for meTTa_eval_agent
Tests basic functionality with and without meTTa framework.
"""

import requests
import json
from datetime import datetime, UTC

def test_basic_endpoints():
    """Test basic REST API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing meTTa_eval_agent...")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Health Check:")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data['status']}")
            print(f"   🤖 Agent: {data['agent_name']}")
            print(f"   🧠 meTTa: {data['metta_available']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
    
    print()
    
    # Test meTTa status endpoint
    print("2. meTTa Status:")
    try:
        response = requests.get(f"{base_url}/metta-status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ meTTa available: {data['metta_available']}")
            print(f"   ✅ Interpreter: {data['interpreter_initialized']}")
            print(f"   ✅ Method: {data['evaluation_method']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    print()
    
    # Test evaluation endpoint
    print("3. Evaluation Test:")
    evaluation_request = {
        "evaluation_type": "truth_verification",
        "data": {
            "content": "The sky is blue on a clear day.",
            "source": "common_knowledge"
        },
        "parameters": {
            "strict_mode": False
        }
    }
    
    try:
        response = requests.post(
            f"{base_url}/evaluate",
            json=evaluation_request,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Evaluation completed:")
            print(f"      Type: {result['evaluation_type']}")
            print(f"      Confidence: {result['confidence_score']:.2f}")
            print(f"      Processing time: {result['processing_time']:.3f}s")
            print(f"      Method: {result['result'].get('method', 'unknown')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"      {response.text}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")


def main():
    """Main test function"""
    print("🚀 meTTa_eval_agent Simple Test")
    print("=" * 60)
    print()
    
    print("⚠️  Make sure meTTa_eval_agent is running on localhost:8000")
    print("   Start it with: python meTTa_eval_agent.py")
    print()
    
    test_basic_endpoints()
    
    print("🎉 Test completed!")
    print()
    print("💡 Notes:")
    print("   • Agent works with or without meTTa framework")
    print("   • Check /metta-status endpoint for framework availability")
    print("   • Install meTTa with: pip install metta")


if __name__ == "__main__":
    main()
