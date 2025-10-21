# Connections between ui - agent - contracts

## UI to Agent

- UI calls agent's REST endpoint directly at `/evaluate` (agentverse.ts)
- Detects agent addresses in chat messages and triggers evaluation
- Chat protocol supports ASI:1 integration (see: `agents/chat_protocol.py`)

## UI to Contracts

- UI needs correct schemas & deployed schema UIDs (attestation-utils.ts)
- UI needs correct graphQL endpoint to query Ethereum Attestation Service for all attestations made by Agents and Humans
- UI needs correct EAS contract address to get attestation detail info

## Agent to Contracts

- Agent needs to be connected to correct chain (RPC_URL & PRIVATE_KEY)
- Agent needs correct attestation schema uid (AGENT_EVALUATION_SCHEMA_UID / evaluator_agent.py:99)
- Agent ETH address needs to be whitelisted in resolver contract

## Agent Architecture

See `agents/ARCHITECTURE.md` for detailed module breakdown:

- `evaluator_agent.py` - Main agent logic & REST endpoint
- `chat_protocol.py` - Chat interface with ASI:1 integration
- `eval_protocol.py` - Agent-to-agent evaluation protocol
