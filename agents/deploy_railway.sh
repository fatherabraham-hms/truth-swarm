#!/bin/bash

echo "🚀 RAILWAY DEPLOYMENT SCRIPT - TRUTH SWARM AGENT"
echo "================================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI ready"
echo ""

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway first:"
    echo "   railway login"
    echo ""
    read -p "Press Enter after logging in..."
fi

echo "📦 Initializing Railway project..."
railway init

echo ""
echo "🔧 Setting up environment variables..."
echo "   You'll need to set these in Railway dashboard:"
echo "   - AGENTVERSE_API_KEY: $(grep AGENTVERSE_API_KEY ../.env | cut -d'=' -f2 | cut -c1-20)..."
echo "   - AGENTVERSE_BASE_URL: https://agentverse.ai"
echo "   - AGENT_NAME: truth_swarm_categorizer_agent"
echo "   - AGENT_PORT: 8000"
echo ""

read -p "Press Enter after setting environment variables in Railway dashboard..."

echo "🚀 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment complete!"
echo "   Check your Railway dashboard for the deployment URL"
echo "   Test with: curl https://your-app.railway.app/health"
