# Agent Deployment Fixes - meTTa Analytics Update

## Issues Fixed

### 1. Agentverse API 307 Redirect Issue
**Problem**: The agent was getting 307 redirects when trying to connect to Agentverse API, leading to 404 errors.

**Solution**: Updated `api/agentverse_client.py` to:
- Enable automatic redirect following (`follow_redirects=True`)
- Try multiple endpoint patterns (`/agents` and `/hosting/agents`)
- Use correct base URL (`https://agentverse.ai` instead of `https://agentverse.ai/v1`)

### 2. Updated Dependencies
**Changes**: Added additional dependencies to `requirements.txt`:
- `requests>=2.31.0`
- `aiofiles>=23.0.0`

### 3. Agent Registration
**Updated**: `register_agent.py` now uses the correct base URL for Agentverse API.

## Deployment Instructions

### 1. Login to Railway
```bash
cd /Users/howardsherman/truth-swarm/agents
railway login
```

### 2. Set Environment Variables in Railway Dashboard
You'll need to set these environment variables in your Railway project:
- `AGENTVERSE_API_KEY`: Your Agentverse API key
- `AGENTVERSE_BASE_URL`: `https://agentverse.ai`
- `AGENT_NAME`: `truth_swarm_categorizer_agent`
- `AGENT_PORT`: `8000`

### 3. Deploy to Railway
```bash
railway up
```

### 4. Test the Deployment
Once deployed, test the health endpoint:
```bash
curl https://your-app.railway.app/health
```

## Key Changes Made

### API Client Updates (`api/agentverse_client.py`)
- All HTTP requests now follow redirects automatically
- Fallback endpoint patterns for better compatibility
- Improved error handling and logging

### Agent Configuration
- Updated base URL configuration
- Enhanced error handling for Agentverse connection issues
- Better fallback mechanisms when API is unavailable

## Testing Commands

### Health Check
```bash
curl https://your-app.railway.app/health
```

### Agent Categorization (NEW!)
```bash
curl -X POST https://your-app.railway.app/categorize-agent \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "example-agent-123", "include_features": true, "include_crypto_details": true}'
```

### Feature Extraction
```bash
curl -X POST https://your-app.railway.app/extract-features \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "example-agent-123"}'
```

### Get Category Taxonomy
```bash
curl https://your-app.railway.app/get-taxonomy
```

## Expected Results

After deployment, you should see:
- ✅ Agent starts successfully without 307 redirect errors
- ✅ Agentverse connection works properly
- ✅ All REST API endpoints are functional
- ✅ meTTa framework is available and working
- ✅ Agent categorization and feature extraction work correctly

## Troubleshooting

If you still encounter issues:
1. Check Railway logs: `railway logs`
2. Verify environment variables are set correctly
3. Test Agentverse API key independently
4. Check if the agent is properly registered with Agentverse
