# Truth Swarm - Agent Evaluator with EAS Attestation

This directory contains the integrated evaluator agent that combines AI-powered agent evaluation with blockchain attestation using the Ethereum Attestation Service (EAS).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd agents
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template and configure your environment:

```bash
# Copy template to project root
cp .env.template ../.env

# Edit the .env file with your configuration
nano ../.env
```

**For Testing/Development (Mock Mode):**

- Leave `PRIVATE_KEY` empty
- The agent will generate mock evaluations and attestation UIDs
- Perfect for frontend development!

**For Production (Real EAS Attestations):**

- Set `PRIVATE_KEY` with your Ethereum private key
- Ensure your wallet has ETH for gas fees
- Set `RPC_URL` to your Infura/Alchemy endpoint

### 3. Run the Agent

```bash
python evaluator_agent.py
```

The agent will start on `http://localhost:8000` with:

- ✅ REST API endpoint at `/evaluate`
- ✅ Chat protocol for interactive evaluations
- ✅ Automatic EAS attestation (or mock mode)

## 📋 Usage Examples

### REST API

Evaluate an agent via REST:

```bash
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "agent_address": "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
  }'
```

**Response:**

```json
{
  "success": true,
  "agent_address": "agent1q...",
  "attestation_uid": "0x1234...",
  "final_score": 87,
  "grade": "A",
  "message": "Agent evaluated successfully! Score: 87/100 (A). Attestation created on EAS."
}
```

### Chat Protocol

Send an agent address via the uAgents chat protocol and receive:

1. Evaluation scores
2. Grade (A+ to F)
3. EAS attestation UID

## 🏗️ Architecture

```
Frontend → REST POST → Evaluator Agent
                            ↓
                    ┌───────┴────────┐
                    │                │
              ASI:1 Evaluator   Attestation Manager
              (Mock or Real)    (EAS Integration)
                    │                │
                    └───────┬────────┘
                            ↓
                    EvaluationResponse
                    + Attestation UID
```

### Components

1. **`evaluator_agent.py`** - Main agent implementation

   - REST endpoint: `/evaluate`
   - Chat protocol handler
   - Evaluation + attestation orchestration

2. **`AttestationManager`** - EAS Integration

   - Encodes evaluation data
   - Creates blockchain attestations
   - Handles Web3 transactions
   - Mock mode for testing

3. **`ASI1Evaluator`** - Agent Evaluation

   - Generates evaluation scores
   - Mock mode: realistic random scores
   - Future: Real ASI:1 evaluation

4. **`EvaluationScore`** - Data Structure
   - All evaluation metrics
   - Matches EAS schema exactly
   - Ready for blockchain encoding

## 📊 Evaluation Metrics

The agent evaluates other agents across three dimensions:

1. **Correctness** (40% weight)
   - How accurate are the agent's responses?
   - Confidence level (0-10)
2. **Capabilities** (30% weight)
   - What can the agent do?
   - Range of supported operations
3. **Domain Knowledge** (30% weight)
   - How well does it understand its domain?
   - Depth of expertise

**Final Score** = Weighted average (0-100)
**Grade** = A+, A, B+, B, C+, C, etc.

## 🔗 EAS Schema

The agent uses the official Truth Swarm EAS schema:

**Schema UID:**

```
0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc
```

**Schema Fields:**

- `evaluatedAgentAddress` (string)
- `evaluatorAgentAddress` (string)
- `timestamp` (uint256)
- `finalScore` (uint256)
- `overallConfidence` (uint8)
- `grade` (string)
- `correctnessScore`, `capabilitiesScore`, `domainScore` (uint256 each)
- Confidence levels and weights for each dimension
- `detailsCID` (string) - IPFS CID for detailed results

## 🔧 Configuration Options

### Environment Variables

| Variable                    | Description               | Required       | Default            |
| --------------------------- | ------------------------- | -------------- | ------------------ |
| `RPC_URL`                   | Ethereum RPC endpoint     | No             | Sepolia Infura     |
| `CHAIN_ID`                  | Blockchain network ID     | No             | 11155111 (Sepolia) |
| `EAS_CONTRACT_ADDRESS`      | EAS contract address      | No             | Sepolia EAS        |
| `RESOLVER_CONTRACT_ADDRESS` | Your resolver contract    | No             | -                  |
| `PRIVATE_KEY`               | Wallet private key        | No (mock mode) | -                  |
| `AGENTVERSE_API_KEY`        | Agentverse deployment key | No             | -                  |

### Code Configuration

In `evaluator_agent.py`:

```python
# Line 366: Toggle mock vs real evaluation
asi1_evaluator = ASI1Evaluator(agent, use_mock=True)  # Set False for ASI:1

# Line 361: Change port
agent = Agent(
    name="evaluator_attestation_agent",
    port=8000,  # Change this
    # ...
)
```

## 🧪 Testing

### Test with Mock Data

1. Run agent without `PRIVATE_KEY` in `.env`
2. Agent generates mock evaluations
3. Returns mock attestation UIDs
4. Perfect for frontend development

```bash
# Test REST endpoint
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_address": "agent1qtest123456789012345678901234567890123456789012345678901"}'
```

### Test with Real Blockchain

1. Set `PRIVATE_KEY` in `.env`
2. Ensure wallet has ETH for gas
3. Agent creates real EAS attestations
4. Check attestations on:
   - Sepolia: https://sepolia.easscan.org/
   - Base: https://base.easscan.org/

## 📁 Files

```
agents/
├── evaluator_agent.py           # Main agent (integrated solution)
├── resolver_atestation_agent.py # Original resolver agent (reference)
├── requirements.txt             # Python dependencies
├── .env.template                # Environment template
├── config.template              # Legacy config (reference)
└── README.md                    # This file
```

## 🎯 For Hackathon

The agent is **hackathon-ready** with:

✅ **Mock Mode** - Test without blockchain
✅ **REST API** - Easy frontend integration
✅ **Chat Protocol** - Interactive demos
✅ **Realistic Scores** - Generated with variation
✅ **Fast** - Instant responses in mock mode

Just run `python evaluator_agent.py` and start evaluating agents!

## 🚢 Deployment

### Local Development

```bash
python evaluator_agent.py
```

### Agentverse Deployment

1. Set `AGENTVERSE_API_KEY` in `.env`
2. Change `mailbox=True` in code (already enabled)
3. Deploy to Agentverse for 24/7 availability

## 🤝 Integration with Frontend

Your frontend can call the REST endpoint:

```javascript
// Example: Evaluate an agent
const response = await fetch("http://localhost:8000/evaluate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    agent_address: "agent1q...",
  }),
});

const result = await response.json();
console.log("Attestation UID:", result.attestation_uid);
console.log("Score:", result.final_score);
console.log("Grade:", result.grade);
```

## 🔍 Debugging

Check linter errors:

```bash
# Ensure packages are installed
pip list | grep -E "(uagents|web3|eth)"

# Check Python version (should be 3.10+)
python --version
```

View agent logs:

```bash
# Agent outputs detailed logs for each evaluation
# Look for:
# 📊 Generated evaluation: Score=87/100, Grade=A
# 🔗 Creating attestation on EAS...
# ✅ Attestation created: 0x1234...
```

## 📚 Resources

- [uAgents Documentation](https://fetch.ai/docs)
- [EAS Documentation](https://docs.attest.sh/)
- [Fetch.ai Innovation Lab](https://innovationlab.fetch.ai/)
- [Truth Swarm Project](../README.md)

## 🆘 Support

For issues:

1. Check linter errors: Look at import warnings
2. Verify Python interpreter: Use correct venv
3. Check `.env` configuration: Especially `PRIVATE_KEY` for production
4. Review agent logs: Detailed info on startup

---

Built with ❤️ for Truth Swarm Hackathon
