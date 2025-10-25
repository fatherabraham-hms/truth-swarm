# Railway Deployment Guide for Truth Swarm Categorizer Agent

This guide walks you through deploying the meTTa evaluation agent to Railway with Agentverse mailbox integration.

## Prerequisites

- Railway account (sign up at [railway.app](https://railway.app))
- Agentverse account and API key
- Git repository with your agent code

## Step 1: Agentverse Mailbox Registration

1. **Get Agentverse API Key:**
   - Go to [Agentverse](https://agentverse.ai)
   - Log in with your Gmail account
   - Navigate to Profile → API Keys
   - Create a new API key with appropriate permissions

2. **Register Agent for Mailbox:**
   - Use the `register_agent.py` script to register your agent
   - This will give you a mailbox key for agent-to-agent communication
   - Save the mailbox key for Railway environment variables

## Step 2: Railway Project Setup

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Project:**
   ```bash
   cd agents
   railway init
   ```

4. **Connect to Git (Optional):**
   - Railway can auto-deploy from your Git repository
   - Or you can deploy directly from CLI

## Step 3: Environment Variables

Set these environment variables in Railway dashboard:

### Required Variables:
- `AGENTVERSE_API_KEY` - Your Agentverse API key
- `AGENT_MAILBOX_KEY` - Mailbox key from agent registration

### Auto-Set by Railway:
- `PORT` - Railway sets this automatically
- `RAILWAY_PUBLIC_DOMAIN` - Your app's public URL

### Optional Variables:
- `AGENTVERSE_BASE_URL` - Defaults to https://agentverse.ai

## Step 4: Deploy to Railway

### Option A: Deploy via CLI
```bash
railway up
```

### Option B: Deploy via Git
1. Push your code to GitHub/GitLab
2. Connect repository in Railway dashboard
3. Railway will auto-deploy on push

## Step 5: Verify Deployment

1. **Check Health Endpoint:**
   ```bash
   curl https://your-app.railway.app/health
   ```

2. **Test Agent Registration:**
   - Your agent should appear in Agentverse
   - Public name: "truth_swarm_catagorizer_agent"
   - Verify mailbox communication is working

3. **Test API Endpoints:**
   ```bash
   # Test crypto detection
   curl -X POST https://your-app.railway.app/detect-crypto \
        -H "Content-Type: application/json" \
        -d '{"agent_id": "test-agent-123"}'
   
   # List agents
   curl -X POST https://your-app.railway.app/list-agents \
        -H "Content-Type: application/json" \
        -d '{"limit": 10}'
   ```

## Step 6: Monitor and Debug

1. **View Logs:**
   ```bash
   railway logs
   ```

2. **Check Agent Status:**
   - Railway dashboard shows deployment status
   - Agentverse shows agent registration status

3. **Debug Issues:**
   - Check environment variables are set correctly
   - Verify Python 3.9 is being used (required for hyperon)
   - Check that all dependencies installed successfully

## Configuration Files

The following files are included for Railway deployment:

- `railway.toml` - Railway configuration
- `runtime.txt` - Python version specification
- `Procfile` - Alternative deployment method
- `requirements.txt` - Python dependencies
- `.env.railway.example` - Environment variable template

## Troubleshooting

### Common Issues:

1. **Python Version Error:**
   - Ensure `runtime.txt` specifies Python 3.9
   - Hyperon only supports Python 3.8-3.9

2. **Import Errors:**
   - Check that `hyperon` package is installed
   - Verify all dependencies in requirements.txt

3. **Mailbox Connection Issues:**
   - Verify `AGENT_MAILBOX_KEY` is set correctly
   - Check agent registration in Agentverse

4. **Port Binding Issues:**
   - Railway sets `PORT` environment variable
   - Agent uses `os.getenv("PORT", 8000)` for dynamic port

### Getting Help:

1. Check Railway logs: `railway logs`
2. Verify environment variables in Railway dashboard
3. Test locally with Railway-like environment:
   ```bash
   export PORT=8000
   export RAILWAY_PUBLIC_DOMAIN=localhost:8000
   python meTTa_eval_agent_refactored.py
   ```

## Next Steps

After successful deployment:

1. **Agent Discovery:** Other agents can now find and communicate with yours
2. **API Integration:** Use the REST endpoints for external integrations
3. **Monitoring:** Set up monitoring and alerting for production use
4. **Scaling:** Railway can auto-scale based on demand

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Agentverse Documentation: [agentverse.ai](https://agentverse.ai)
- uAgents Framework: [uagents.ai](https://uagents.ai)
