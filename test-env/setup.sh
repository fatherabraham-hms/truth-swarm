#!/bin/bash

# Test Environment Setup Script
# This script sets up and runs the local test environment for the Resolver Attestation Agent

set -e

echo "🚀 Setting up Resolver Attestation Agent Test Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the test-env directory."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
else
    echo "✅ Node.js dependencies already installed"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install web3 eth-account eth-abi aiohttp python-dotenv pytest pytest-asyncio

echo "✅ Python dependencies installed"

# Compile contracts
echo "🔨 Compiling contracts..."
npx hardhat compile

if [ $? -eq 0 ]; then
    echo "✅ Contracts compiled successfully"
else
    echo "❌ Contract compilation failed"
    exit 1
fi

# Run contract tests
echo "🧪 Running contract tests..."
npx hardhat test

if [ $? -eq 0 ]; then
    echo "✅ Contract tests passed"
else
    echo "❌ Contract tests failed"
    exit 1
fi

echo ""
echo "🎉 Test environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'python3 test_agent_integration.py' to test the agent integration"
echo "2. Or run 'npx hardhat node' in one terminal and 'python3 test_agent_integration.py' in another"
echo ""
echo "Available commands:"
echo "  npx hardhat node                    - Start local blockchain"
echo "  npx hardhat run scripts/deploy.js   - Deploy contracts"
echo "  npx hardhat test                    - Run contract tests"
echo "  python3 test_agent_integration.py  - Run agent integration tests"
echo ""
echo "Happy testing! 🚀"
