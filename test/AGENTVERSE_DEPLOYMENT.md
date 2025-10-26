# 🚀 AgentVerse Deployment Guide

Quick guide to deploy the Truth Swarm Tester Agent to AgentVerse (ASI).

## 📋 Pre-Deployment Checklist

- [ ] Have an AgentVerse account at [agentverse.ai](https://agentverse.ai)
- [ ] Code ready: `tester-agent-agentverse.py`
- [ ] Seed phrase ready (unique string for your agent)

## 🎯 Step-by-Step Deployment

### Step 1: Login to AgentVerse

1. Go to https://agentverse.ai
2. Login with your Fetch.ai account
3. Navigate to "My Agents"

### Step 2: Create New Agent

1. Click **"Create Agent"** or **"New Agent"**
2. Choose **"Blank Agent"** template
3. Name: `Truth Swarm Tester`
4. Description: `Allows users to request agent evaluations via Truth Swarm`

### Step 3: Copy Code

1. Open `tester-agent-agentverse.py`
2. **Select all** (Cmd+A / Ctrl+A)
3. **Copy** (Cmd+C / Ctrl+C)
4. In AgentVerse code editor, **paste** the entire code
5. Click **"Save"**

### Step 4: Configure Environment Variables

In AgentVerse Settings/Environment Variables section:

1. Click **"Add Variable"**
2. **Name:** `TESTER_AGENT_SEED_PHRASE`
3. **Value:** Your unique seed phrase (e.g., `my_unique_tester_seed_2024`)
4. Click **"Save"**

> 💡 **Tip:** Use a unique, memorable seed phrase. It determines your agent's address.

### Step 5: Deploy

1. Click **"Deploy"** or **"Start Agent"**
2. Wait for deployment (usually 10-30 seconds)
3. Check status shows **"Running"** ✅

### Step 6: Get Your Agent Address

1. Once deployed, copy your agent's address
2. Format: `agent1q...` (65 characters)
3. Share this with users who want to test agents!

## 🧪 Testing Your Deployed Agent

### Option 1: AgentVerse Chat UI

1. In AgentVerse, go to your agent's page
2. Use the built-in chat interface
3. Send a test message:
   ```
   agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
   ```
4. You should receive confirmation and updates

### Option 2: From Another Agent

Have another agent send a ChatMessage to your tester agent's address.

### Option 3: Programmatically

Use uAgents locally to send messages to your deployed agent.

## 📊 Monitoring

### View Logs

In AgentVerse:
1. Go to your agent's page
2. Click **"Logs"** tab
3. Monitor real-time activity

Expected log entries:
```
🧪 Truth Swarm Tester Agent Ready!
Agent: agent1q...
Message from agent1q...: agent1q0h70...
Starting eval for: agent1q0h70...
Update from evaluator: Evaluation started...
```

### View Messages

1. Go to **"Messages"** tab
2. See all incoming/outgoing messages
3. Debug message flow

## 🔧 Configuration Options

### Changing Evaluator Address

If you need to point to a different evaluator:

```python
EVALUATOR_AGENT_ADDRESS = "agent1q..." # Change this line
```

### Adjusting Response Messages

Customize the response text in the `handle_chat` function:

```python
response = (
    "Your custom welcome message here"
)
```

## 🐛 Troubleshooting

### Agent Won't Start

**Problem:** Deployment fails or agent shows "Error"

**Solutions:**
- Check logs for syntax errors
- Verify all imports are available in AgentVerse
- Ensure `TESTER_AGENT_SEED_PHRASE` is set
- Try redeploying

### No Response from Evaluator

**Problem:** User gets confirmation but no updates

**Solutions:**
- Verify evaluator address is correct
- Check evaluator agent is running: `agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4`
- Check logs for message sending errors
- Verify network connectivity in AgentVerse

### User Not Receiving Updates

**Problem:** Evaluator sends updates but user doesn't see them

**Solutions:**
- Check state management - verify `state.user` is set
- Look for errors in `handle_update` function
- Verify user's agent is still online
- Check message format is correct

### Invalid Agent Address Error

**Problem:** Valid addresses marked as invalid

**Solutions:**
- Check address is lowercase
- Verify exactly 65 characters
- Ensure no extra spaces
- Must start with "agent1"

## 📈 Optimization Tips

### For High Traffic

If many users will use your agent:

1. **Add Rate Limiting**
   ```python
   # Track requests per user
   request_counts = {}
   ```

2. **Add Queuing**
   ```python
   # Queue multiple evaluation requests
   evaluation_queue = []
   ```

3. **Add Request Timeout**
   ```python
   # Auto-complete if no response in X seconds
   ```

### For Better UX

1. **Add Help Command**
   ```python
   if "help" in text.lower():
       # Send help message
   ```

2. **Add Status Check**
   ```python
   if "status" in text.lower():
       # Send current evaluation status
   ```

3. **Add History**
   ```python
   # Store past evaluations per user
   ```

## 🎓 Best Practices

### Security

- ✅ Never hardcode private keys
- ✅ Use environment variables for sensitive data
- ✅ Validate all user inputs
- ✅ Sanitize agent addresses before processing

### Reliability

- ✅ Add error handling for all async operations
- ✅ Log all important events
- ✅ Handle network failures gracefully
- ✅ Provide meaningful error messages to users

### User Experience

- ✅ Send immediate confirmation on request
- ✅ Provide progress updates
- ✅ Format final results clearly
- ✅ Include helpful links (EAS explorer)

## 📱 Sharing Your Agent

Once deployed, share your agent with:

### Direct Address
```
agent1q[your_unique_address_here]
```

### AgentVerse Link
```
https://agentverse.ai/agents/[your-agent-id]
```

### Integration Example

Other developers can interact with your agent:

```python
from uagents import Context
from uagents_core.contrib.protocols.chat import ChatMessage, TextContent
from datetime import datetime
from uuid import uuid4

# Your tester agent address
TESTER_ADDRESS = "agent1q..."

# Send evaluation request
await ctx.send(
    destination=TESTER_ADDRESS,
    message=ChatMessage(
        timestamp=datetime.now(),
        msg_id=uuid4(),
        content=[TextContent(
            type="text", 
            text="agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
        )]
    )
)
```

## 📚 Resources

- [AgentVerse Documentation](https://docs.fetch.ai/guides/agentverse)
- [uAgents Documentation](https://docs.fetch.ai/uAgents)
- [Chat Protocol Guide](https://docs.fetch.ai/guides/agents/intermediate/chat-protocol)
- [Truth Swarm GitHub](https://github.com/fatherabraham-hms/truth-swarm)

## 🎉 You're Done!

Your Truth Swarm Tester Agent is now live on AgentVerse!

Users can now:
- Send agent addresses via chat
- Receive real-time evaluation updates
- Get attestation UIDs and links
- View results on EAS explorer

**Next Steps:**
- Share your agent's address
- Monitor usage via AgentVerse dashboard
- Iterate based on user feedback
- Add custom features as needed

---

**Need Help?** 
- Check AgentVerse Discord
- Review logs in AgentVerse UI
- Test locally first with `tester-agent.py`

