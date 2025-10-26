# ASI:1 Integration Roadmap

## Making Your Evaluator Agent Discoverable by ASI:1

## 🎯 Goal

Enable ASI:1 (Fetch.ai's AI) to discover and use your evaluator agent when users ask about agent evaluation, attestations, or trust scores.

---

## 📋 Current State

### What You Have

- ✅ Working evaluator agent with REST API
- ✅ EAS attestation integration
- ✅ uAgents framework with human chat protocol & eval_protocol
- ✅ Local endpoint: `http://localhost:8000`

### What's Missing

- ❌ Agent not registered on Agentverse
- ❌ No agent protocol manifest published
- ❌ Not discoverable by other agents
- ❌ No Almanac registration

---

## 🗺️ Implementation Path

### Phase 1: Agent Registration (Week 1-2)

#### 1.1 Deploy Agent to Agentverse

**Why**: Agentverse provides hosted infrastructure, persistent address, and discoverability.

**Steps**:

```bash
# 1. Create account at agentverse.ai
# 2. Create new agent in Agentverse dashboard
# 3. Copy your agent code to Agentverse editor
# 4. Configure secrets (PRIVATE_KEY, RPC_URL, etc.)
# 5. Deploy and get permanent agent address
```

**Result**: Agent gets permanent address like `agent1q...` and runs 24/7

#### 1.2 Configure Mailbox

Your agent already has mailbox enabled:

```python
agent = Agent(
    name="evaluator_attestation_agent",
    seed="",
    port=8000,
    endpoint=["http://localhost:8000/submit"],
    mailbox=True  # ✅ Already configured
)
```

**Update for Agentverse**:

```python
# In Agentverse, mailbox is automatic
agent = Agent(
    name="evaluator_attestation_agent",
    seed=os.getenv("AGENT_SEED"),  # Set in Agentverse secrets
    mailbox=True
)
# No port/endpoint needed - Agentverse handles this
```

---

### Phase 2: Protocol Enhancement (Week 2-3)

#### 2.1 Enhanced Agent Manifest

Update your agent to publish a rich manifest that ASI:1 can discover:

```python
from uagents import Agent, Context, Model, Protocol

# Define clear message models for discoverability
class AgentEvaluationRequest(Model):
    """Request evaluation of an agent"""
    agent_address: str
    evaluation_criteria: str = "comprehensive"  # comprehensive, quick, detailed

class AgentEvaluationResponse(Model):
    """Evaluation result with attestation"""
    success: bool
    agent_address: str
    final_score: int
    grade: str
    attestation_uid: str
    eas_link: str
    details_cid: str

# Create protocol with semantic tags
eval_protocol = Protocol(
    name="agent-evaluation",
    version="1.0",
    description="Evaluate AI agents and create EAS attestations",
    tags=["evaluation", "attestation", "trust", "eas", "verification"]
)

@eval_protocol.on_message(model=AgentEvaluationRequest, replies=AgentEvaluationResponse)
async def handle_evaluation(ctx: Context, sender: str, msg: AgentEvaluationRequest):
    """Evaluate an agent and return attestation"""
    result = await process_evaluation(msg.agent_address, ctx)

    await ctx.send(sender, AgentEvaluationResponse(
        success=result.success,
        agent_address=msg.agent_address,
        final_score=result.final_score,
        grade=result.grade,
        attestation_uid=result.attestation_uid,
        eas_link=f"https://sepolia.easscan.org/attestation/view/{result.attestation_uid}",
        details_cid=evaluation_score.detailsCID
    ))

# Publish with manifest
agent.include(eval_protocol, publish_manifest=True)  # ✅ Critical!
```

#### 2.2 Add Service Metadata

```python
from uagents import Agent, Context, Bureau

# Add rich metadata for discovery
agent = Agent(
    name="truthswarm_evaluator",
    seed=os.getenv("AGENT_SEED"),
    mailbox=True
)

@agent.on_event("startup")
async def startup(ctx: Context):
    # Register service capabilities
    ctx.storage.set("service_type", "agent_evaluation")
    ctx.storage.set("capabilities", [
        "evaluate_agents",
        "create_attestations",
        "eas_integration",
        "trust_scores"
    ])
    ctx.storage.set("version", "1.0.0")
    ctx.storage.set("description",
        "Evaluate AI agents and create verifiable on-chain attestations via EAS"
    )
```

---

### Phase 3: Almanac Registration (Week 3-4)

#### 3.1 Register in Almanac

The Almanac is Fetch.ai's agent discovery service. ASI:1 queries it to find agents.

```python
from uagents import Agent, Context
from uagents.network import wait_for_tx_to_complete

@agent.on_event("startup")
async def register_in_almanac(ctx: Context):
    """Register agent service in Almanac for discovery"""

    # Define service endpoints
    service_endpoints = {
        "evaluate_agent": {
            "description": "Evaluate an AI agent and create EAS attestation",
            "model": "AgentEvaluationRequest",
            "response": "AgentEvaluationResponse"
        }
    }

    # Register (Agentverse handles this automatically when manifest published)
    ctx.logger.info(f"Agent registered at: {agent.address}")
    ctx.logger.info("Service discoverable via Almanac")
```

**Note**: When you publish manifest (`publish_manifest=True`), Agentverse automatically registers you in Almanac.

#### 3.2 Add Search Keywords

Make your agent findable by relevant queries:

```python
# In your agent metadata
keywords = [
    "agent evaluation",
    "attestation",
    "EAS",
    "ethereum attestation service",
    "trust score",
    "agent verification",
    "truth swarm",
    "reputation",
    "agent rating"
]
```

---

### Phase 4: ASI:1 Integration (Week 4-5)

#### 4.1 How ASI:1 Will Discover You

When a user asks ASI:1:

> "Can you evaluate this agent for me: agent1q..."

ASI:1 will:

1. **Parse intent**: "evaluate agent"
2. **Query Almanac**: Search for agents with "evaluation" capability
3. **Find your agent**: Via published protocol manifest
4. **Send message**: Using uAgents protocol
5. **Receive result**: Your attestation UID and scores
6. **Present to user**: Formatted response with EAS link

#### 4.2 Test Discovery

```python
# Test script to verify your agent is discoverable
from uagents import Bureau
from uagents.query import query

async def test_discovery():
    """Test if agent can be found via Almanac"""

    # Query Almanac for evaluation services
    results = await query(
        query="agent evaluation",
        service_type="agent_evaluation"
    )

    print(f"Found {len(results)} evaluation services")
    for result in results:
        print(f"  - {result.name}: {result.address}")

# Run test
bureau = Bureau()
bureau.run()
```

#### 4.3 Example ASI:1 Interaction Flow

```
User → ASI:1: "Evaluate agent1q... for me"

ASI:1 Internal:
  1. Parse: Need agent evaluation service
  2. Almanac query: Find "agent_evaluation" services
  3. Select: truthswarm_evaluator (best match)
  4. Send: AgentEvaluationRequest(agent_address="agent1q...")

Your Agent:
  1. Receive request
  2. Evaluate agent
  3. Create EAS attestation
  4. Return AgentEvaluationResponse

ASI:1 → User:
  "✅ Agent evaluated! Score: 85/100 (Grade A)
   Attestation: https://sepolia.easscan.org/attestation/view/0x...

   The agent shows strong performance across all metrics."
```

---

## 🔧 Technical Requirements

### Required Changes to Current Agent

1. **Move to Agentverse** (or keep local with public endpoint)
2. **Publish manifest**: Already have `publish_manifest=True` ✅
3. **Use semantic models**: Update message models with clear types
4. **Add metadata**: Service description, capabilities, keywords

### Infrastructure Requirements

- **Agentverse account** (free tier available)
- **Public endpoint** (if self-hosting) OR Agentverse hosting
- **Mailbox enabled** (already done ✅)
- **Stable agent seed** (for persistent address)

---

## 📊 Discoverability Checklist

- [ ] Agent deployed to Agentverse (or public endpoint)
- [ ] Protocol manifest published (`publish_manifest=True`)
- [ ] Clear message models with descriptions
- [ ] Service metadata configured
- [ ] Keywords/tags added for search
- [ ] Almanac registration verified
- [ ] Test query from another agent successful
- [ ] Documentation published (README, examples)

---

## 🚀 Quick Start Path

### Option A: Deploy to Agentverse (Recommended)

```bash
1. Go to agentverse.ai
2. Create account
3. New Agent → Copy code
4. Add secrets (PRIVATE_KEY, RPC_URL, etc.)
5. Deploy
6. Test with curl
7. Verify in Almanac
```

**Time**: 1-2 hours

### Option B: Self-Host with Public Endpoint

```bash
1. Deploy agent to cloud (Railway, Render, AWS)
2. Configure public endpoint
3. Update agent with public URL
4. Register in Almanac manually
5. Test discoverability
```

**Time**: 4-6 hours

---

## 💡 Advanced: ASI:1 Function Calling

Future enhancement - ASI:1 can call your agent as a "tool":

```python
# Your agent becomes an ASI:1 tool
{
    "name": "evaluate_agent",
    "description": "Evaluate an AI agent and create verifiable attestation",
    "parameters": {
        "agent_address": "string (required)",
        "criteria": "string (optional): comprehensive|quick|detailed"
    },
    "returns": {
        "score": "integer",
        "grade": "string",
        "attestation_uid": "string",
        "eas_link": "string"
    }
}
```

This requires Fetch.ai team integration but makes your agent a native ASI:1 capability.

---

## 📚 Resources

- [Agentverse Documentation](https://fetch.ai/docs/guides/agentverse)
- [uAgents Protocol Docs](https://fetch.ai/docs/guides/agents/communicating-with-other-agents)
- [Almanac Service Discovery](https://fetch.ai/docs/guides/agents/register-in-almanac)
- [ASI:1 Integration Guide](https://fetch.ai/docs/concepts/ai-engine)

---

## 🎯 Success Metrics

Your agent is successfully integrated when:

1. ✅ User asks ASI:1 to evaluate an agent
2. ✅ ASI:1 finds your agent in Almanac
3. ✅ ASI:1 sends evaluation request to your agent
4. ✅ Your agent returns attestation UID
5. ✅ User sees formatted result with EAS link

**End goal**: "Hey ASI:1, evaluate this agent" → Your agent gets called automatically.

---

## 🔮 Future Enhancements

- **Multi-agent orchestration**: Your agent coordinates with other verifiers
- **Reputation network**: Aggregate scores from multiple evaluators
- **Automated monitoring**: Periodic re-evaluation of agents
- **Human verification integration**: Link to human attestation workflow
- **DAO governance**: Community votes on evaluation criteria

---

**Questions?** Open an issue or check the [uAgents Discord](https://discord.gg/fetchai)
