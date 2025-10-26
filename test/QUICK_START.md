# ⚡ Quick Start - Tester Agent

## 🎯 Deploy to AgentVerse in 5 Steps

### 1. Copy Code
Open `tester-agent-agentverse.py` and copy all contents (Cmd+A, Cmd+C)

### 2. Create Agent
- Go to [agentverse.ai](https://agentverse.ai)
- Click "Create Agent"
- Paste code into editor

### 3. Set Environment Variable
```
Name: TESTER_AGENT_SEED_PHRASE
Value: your_unique_seed_phrase_here
```

### 4. Deploy
Click "Deploy" button

### 5. Test
Send a message to your agent:
```
agent1q2c8sxs5kg902j96ffruh0he2erhjf63eahrypzvj20gjraevxlggy4fq33
```

## 🧪 Test Locally First

```bash
# 1. Install dependencies
pip install uagents uagents-core python-dotenv

# 2. Set seed phrase
echo "TESTER_AGENT_SEED_PHRASE=test_seed_123" >> .env

# 3. Run tester agent
python tester-agent.py

# 4. In another terminal, run test script
# (Update TESTER_AGENT_ADDRESS in test-tester-agent.py first)
python test-tester-agent.py
```

## 📋 Files Reference

| File | Purpose |
|------|---------|
| `tester-agent-agentverse.py` | **→ USE THIS for AgentVerse** |
| `tester-agent.py` | Local development version |
| `test-tester-agent.py` | Testing script |
| `AGENTVERSE_DEPLOYMENT.md` | Full deployment guide |
| `TESTER_AGENT_README.md` | Technical docs |
| `TESTER_AGENT_SUMMARY.md` | Complete overview |

## 🎓 Key Info

**Evaluator Agent Address:**
```
agent1qtak6m7rgytst3zqmu744t0k8z4xytf3zrnct49efqvwxzqc3f3t5rkflj4
```

**Message Format to Evaluator:**
```
/agent1q.../
```

**Expected Updates from Evaluator:**
1. "Evaluation started for..."
2. "Received response from..."
3. "Attestation created: 0x..."

## 💡 Pro Tips

- **Seed Phrase:** Use a unique value (it determines your agent address)
- **Testing:** Test locally before deploying to AgentVerse
- **Monitoring:** Watch logs in AgentVerse dashboard
- **Updates:** Code is minimal and easy to customize

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent won't start | Check seed phrase is set |
| No evaluator response | Verify evaluator address |
| User not getting updates | Check logs for errors |
| Invalid address error | Must be 65 chars, start with "agent1" |

## 🎉 That's It!

Your tester agent will now:
- Accept agent addresses from users
- Forward to evaluator agent
- Provide real-time updates
- Deliver attestation results

**Questions?** Check the detailed docs or AgentVerse Discord!

