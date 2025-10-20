#!/usr/bin/env python3
"""
Simple Test Runner for Resolver Attestation Agent

This script provides a simple interface to run different types of tests.
"""

import asyncio
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False

def main():
    """Main test runner"""
    print("🧪 Resolver Attestation Agent Test Runner")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_runner.py <test_type>")
        print("\nAvailable test types:")
        print("  setup     - Run initial setup")
        print("  contracts - Run contract tests only")
        print("  agent     - Run agent integration tests only")
        print("  all       - Run all tests")
        print("  deploy    - Deploy contracts only")
        sys.exit(1)
    
    test_type = sys.argv[1].lower()
    
    if test_type == "setup":
        print("🚀 Running setup...")
        success = run_command("./setup.sh", "Environment setup")
        
    elif test_type == "contracts":
        print("🔨 Running contract tests...")
        success = run_command("npx hardhat compile", "Contract compilation")
        if success:
            success = run_command("npx hardhat test", "Contract tests")
            
    elif test_type == "agent":
        print("🤖 Running agent integration tests...")
        success = run_command("python3 test_agent_integration.py", "Agent integration tests")
        
    elif test_type == "all":
        print("🎯 Running complete test suite...")
        success = run_command("./setup.sh", "Environment setup")
        if success:
            success = run_command("python3 test_agent_integration.py", "Complete test suite")
            
    elif test_type == "deploy":
        print("📦 Deploying contracts...")
        success = run_command("npx hardhat run scripts/deploy.js --network localhost", "Contract deployment")
        
    else:
        print(f"❌ Unknown test type: {test_type}")
        print("Available types: setup, contracts, agent, all, deploy")
        sys.exit(1)
    
    if success:
        print(f"\n🎉 {test_type.title()} tests completed successfully!")
    else:
        print(f"\n💥 {test_type.title()} tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
