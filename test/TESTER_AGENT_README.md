# 🧪 Truth Swarm Tester Agent

A user-friendly agent that allows anyone to request evaluations of other agents through the Truth Swarm evaluation system.

## 🎯 Purpose

This agent acts as a gateway between users and the Truth Swarm evaluator agent. Users can simply send an agent address via chat, and this agent handles the entire evaluation workflow, providing real-time updates.

## 📋 Features

- ✅ **Simple Chat Interface** - Users just send an agent address
- ✅ **Automatic Forwarding** - Sends requests to the evaluator agent
- ✅ **Real-time Updates** - Forwards all evaluation progress to the user
- ✅ **Attestation Links** - Provides direct links to view attestations on EAS
- ✅ **AgentVerse Ready** - Designed for deployment on ASI's AgentVerse platform

## 🚀 How to Use

### For End Users (via Chat):

1. Start a chat with the tester agent
2. Send an agent address you want evaluated:
   ```
   agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
   ```
3. Receive real-time updates on the evaluation
4. Get the final attestation UID and link

### For Developers (Local Testing):

```bash
# Install dependencies (if not already installed)
pip install uagents uagents-core python-dotenv

# Set your seed phrase in .env
echo "TESTER_AGENT_SEED_PHRASE=your_unique_seed_here" >> .env

# Run the agent
python tester-agent.py
```

## 🌐 Deploying to AgentVerse

### Step 1: Copy the Code

Copy the entire `tester-agent.py` file content to AgentVerse's code editor.

### Step 2: Configure Environment Variables

In AgentVerse settings, add:
- `TESTER_AGENT_SEED_PHRASE` - Your unique seed phrase for this agent

### Step 3: Deploy

Click "Deploy" and your agent will be live!

## 📡 Message Flow

```
User → Tester Agent → Evaluator Agent → Target Agent
                ↓                    ↓
            Updates              Evaluation
                ↓                    ↓
User ← Tester Agent ← Evaluator Agent
```

### Detailed Flow:

1. **User Request**
   - User sends: `ChatMessage` with agent address
   - Tester validates and formats the address

2. **Evaluation Request**
   - Tester sends: `ChatMessage` with `/agent1.../` format
   - To: `agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4`

3. **Progress Updates**
   - Evaluator sends: `AIResponse` messages with updates
   - Tester forwards: `ChatMessage` to original user

4. **Final Result**
   - Evaluator sends: Attestation UID
   - Tester formats: Link to EAS explorer
   - User receives: Complete evaluation report

## 🔧 Configuration

### Environment Variables:

```bash
# Required for local testing
TESTER_AGENT_SEED_PHRASE=your_unique_seed_phrase_here

# Optional - if running in AgentVerse, this is auto-set
AGENTVERSE_ENVIRONMENT=true
```

### Constants (in code):

```python
# Deployed evaluator agent
EVALUATOR_AGENT_ADDRESS = "agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4"

# Port for local testing
port=8001
```

## 📝 Message Models

### UserRequest (ChatMessage)
```python
ChatMessage(
    timestamp=datetime.now(),
    msg_id=uuid4(),
    content=[TextContent(type="text", text="agent1q...")]
)
```

### AIResponse (from evaluator)
```python
AIResponse(
    text="Evaluation started for agent1q..."
)
```

## 🧩 State Management

The agent maintains:
- `current_user` - Address of user who requested evaluation
- `current_target_agent` - Agent being evaluated
- `evaluation_in_progress` - Boolean flag
- `updates` - List of all updates received

## 🎨 Example Conversation

**User:**
```
Please evaluate agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
```

**Tester Agent:**
```
✅ Evaluation request sent!

🎯 Target Agent: agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
📡 Evaluator: agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4

⏳ Waiting for evaluation to complete...
I'll send you updates as they come in!
```

**Tester Agent (Update 1):**
```
📬 Update from Evaluator:

Evaluation started for agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y
```

**Tester Agent (Update 2):**
```
📬 Update from Evaluator:

Received response from agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y.
```

**Tester Agent (Final):**
```
📬 Update from Evaluator:

Attestation created: 0xabc123def456...

🎉 Evaluation Complete!
🔗 Attestation UID: 0xabc123def456...
📊 View on EAS: https://sepolia.eatscan.io/attestation/0xabc123def456...
```

## 🔍 Validation

The agent validates:
- ✅ Agent address starts with "agent1"
- ✅ Agent address is exactly 65 characters
- ✅ Address matches regex: `agent1[a-z0-9]{60}`

Invalid addresses receive helpful error messages.

## 🐛 Troubleshooting

### No Response from Evaluator
- Check evaluator agent is running
- Verify evaluator address is correct
- Check logs for connection errors

### User Not Receiving Updates
- Verify user address is stored correctly
- Check `tester_state.current_user` is set
- Look for message sending errors in logs

### Invalid Agent Address
- Must start with "agent1"
- Must be exactly 65 characters
- Must be lowercase alphanumeric

## 📚 Related Files

- `evaluator-agent.py` - The evaluation agent this connects to
- `.env` - Environment configuration
- `requirements.txt` - Python dependencies

## 🎓 AgentVerse Deployment Tips

1. **Keep it Simple** - The agent is already optimized for AgentVerse
2. **Use Mailbox** - `mailbox=True` enables persistent messaging
3. **Environment Variables** - Set these in AgentVerse UI, not in code
4. **Logging** - Use `ctx.logger` for debugging in AgentVerse console
5. **Testing** - Test locally first, then deploy to AgentVerse

## 🔗 Links

- [AgentVerse Platform](https://agentverse.ai)
- [uAgents Documentation](https://docs.fetch.ai/uAgents)
- [EAS Explorer (Sepolia)](https://sepolia.eatscan.io)
- [Truth Swarm Repository](https://github.com/fatherabraham-hms/truth-swarm)

## 📄 License

MIT License - See LICENSE file for details

