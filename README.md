# Truth Swarm

Truth Swarm is a verification mechanism for consumer protections in the age of agentic AI.

Through a series of evaluations including prompts and ground truth answers, an target agent is evaluated based on:

   capabilities_score
   domain_score
   correctness_score
   conciseness_score
   helpfulness_score

Ethereum Attestation Service is used as a decentralized attestation system that enables the evaluator agent to create verifiable evaluations of the tested agents' performance.

## 🎯 Overview

Truth Swarm implements a comprehensive attestation system using:

- **EAS (Ethereum Attestation Service) & Resolver Contract** for managing authorization and attestation logic
- **Python agents** for processing evaluations and creating attestations
- **Next.js UI** for user interfaces

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** with virtual environment support
- **Node.js 18+** with npm
- **Git** for version control

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd truth-swarm

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup Node.js dependencies
cd scripts && npm install
cd ../ui && npm install
cd ../test-env && npm install
```

### 2. Configuration

```bash
# Copy configuration template
cp .env.template .env

# Edit .env with your settings:
# - RPC_URL: Blockchain RPC endpoint (SEPOLIA)
# - PRIVATE_KEY: Your wallet private key (Paste the address associated with the key and ask for whitelisting on resolver)
# - AGENTVERSE_API_KEY: Used in the UI for fecthing agent data based on the agent address
# - ASI_ONE_API_KEY: Used by the AGENT to communicate with ASI:1 LLM
```

### 3. Setup Local Testing

```bash
# Run the complete test suite
cd agents
python evaluator_agent.py
```

```bash
# Run the complete test suite
cd ui
npm install
npm run dev
```

## 📚 Components

### 1. 🤖 Agents (`/agents`)

Python-based evaluator agents that process agent evaluations and create blockchain attestations.

**Key Features:**

- **REST API endpoint** at `/evaluate` for easy integration
- **Chat Protocol** for interactive evaluations with ASI:1 support
- **Mock Mode** for development without blockchain transactions
- **EAS Integration** via AttestationManager for on-chain attestations

**Main Files:**

- `evaluator_agent.py` - Core agent with REST endpoint and evaluation orchestration
- `eval_protocol.py` - Agent-to-agent evaluation protocol
- `human_chat_protocol.py` - Human-facing chat interface with ASI:1 integration

**Evaluation Metrics:**

- Correctness (40% weight) - Response accuracy and confidence
- Capabilities (30% weight) - Range of supported operations
- Domain Knowledge (30% weight) - Expertise depth

**Usage:**

```bash
cd agents
pip install -r requirements.txt
python evaluator_agent.py  # Starts on http://localhost:8000
```

See [Agent Documentation](agents/README.md) for detailed usage.

### 2. 📜 Smart Contracts (`/contracts`)

Solidity smart contracts built with Foundry for managing attestation authorization.

> **Note:** The contracts are already deployed on Sepolia. You don't need to deploy them yourself unless you're setting up a custom instance or testing on a different network.

**Key Components:**

- **TruthSwarmResolver** (`Resolver.sol`) - Whitelist-based resolver contract that validates attestations from authorized agents
- **EAS Integration** - Leverages Ethereum Attestation Service for decentralized verification
- **Access Control** - Owner-managed whitelist for agent authorization

**Contract Features:**

- Whitelist management (add/remove attesters)
- Attestation validation for whitelisted agents only
- Event emission for transparency
- OpenZeppelin security patterns

**Deployed Contracts:**

- **Network:** Sepolia Testnet
- **EAS Contract:** `0x4200000000000000000000000000000000000021`
- **Schema UID:** `0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc`

**Development (Optional):**

```bash
cd contracts
forge build                    # Compile contracts
forge test                     # Run tests
```

See [Contracts Documentation](contracts/README.md) for deployment details.

### 3. 🎨 User Interface (`/ui`)

Next.js 15 web application for viewing attestations, agent evaluations, and human verifications.

**Key Features:**

- **Agent Evaluation Dashboard** - View and submit agent evaluations
- **Human Attestations Overview** - Manual verification interface
- **Real-time Data** - GraphQL queries to EAS for live attestation data
- **Wallet Integration** - Connect via wagmi/viem for on-chain interactions
- **Responsive Design** - Built with Radix UI and Tailwind CSS

**Main Pages:**

- Agent evaluation submission and viewing
- Human verification interface
- Attestation explorer and search
- Dashboard with metrics and recent activity

**Usage:**

```bash
cd ui
npm install
npm run dev  # Starts on http://localhost:3000
```

See [UI Documentation](ui/README.md) for detailed features.

### Component Integration

```
┌─────────────┐
│   UI (Web)  │ ─── REST POST ──► ┌──────────────┐
└─────────────┘                   │    Agents    │
       │                          │ (Python)     │
       │                          └──────┬───────┘
       │                                 │
       │                          Creates Attestations
       │                                 │
       ▼                                 ▼
┌─────────────────────────────────────────────┐
│   Smart Contracts (Resolver + EAS)         │
│   • Validates whitelisted agents           │
│   • Stores attestations on-chain           │
└─────────────────────────────────────────────┘
```

**Data Flow:**

1. UI calls agent REST endpoint `/evaluate` with agent address
2. Agent evaluates target agent and generates scores
3. Agent creates attestation via AttestationManager
4. Resolver contract validates agent is whitelisted
5. EAS stores attestation on blockchain
6. UI queries attestation data via GraphQL

## 🧪 Testing

### Agent Tests

```bash
cd agents
# Run agent with mock mode (no blockchain required)
python evaluator_agent.py

# Test REST endpoint
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_address": "agent1qtest..."}'
```

### Contract Tests

```bash
cd contracts
forge test                    # Run all tests
forge test -vvv              # Verbose output
forge coverage               # Coverage report
```

### UI Tests

```bash
cd ui
npm run lint                 # Lint checks
npm run build                # Build validation
```

## 🚀 Deployment

### Agent Deployment

**Local:**

```bash
cd agents
python evaluator_agent.py
```

**Agentverse (24/7 availability):**

1. Set `AGENTVERSE_API_KEY` in agents/.env
2. Agent already configured with `mailbox=True`
3. Deploy via Agentverse dashboard

### Contract Deployment

> **Note:** Contracts are already deployed. Only needed for custom setups.

```bash
cd contracts
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast
```

### UI Deployment

**Vercel (Recommended):**

```bash
cd ui
npm run build
# Deploy to Vercel via GitHub integration or CLI
```

**Environment Variables for Production:**

- `NEXT_PUBLIC_RPC_URL` - Ethereum RPC endpoint
- `NEXT_PUBLIC_CHAIN_ID` - Chain ID (11155111 for Sepolia)
- `NEXT_PUBLIC_EAS_CONTRACT_ADDRESS` - EAS contract address
- `AGENTVERSE_API_KEY` - For fetching agent data

## 🏗️ Architecture

Truth Swarm consists of three main layers:

1. **Presentation Layer** (Next.js UI)

   - User-facing web interface
   - Wallet connection & transaction signing
   - Real-time attestation viewing

2. **Application Layer** (Python Agents)

   - Agent evaluation logic
   - ASI:1 LLM integration
   - REST API for external integrations
   - Chat protocol for interactive use

3. **Blockchain Layer** (Smart Contracts + EAS)
   - Decentralized attestation storage
   - Access control via resolver
   - Immutable verification records

**Key Integrations:**

- **Ethereum Attestation Service (EAS)** - Decentralized attestation infrastructure
- **ASI:1 LLM** - AI-powered agent evaluation
- **Agentverse** - Agent deployment and hosting platform

## 🌐 Supported Networks

- **Sepolia Testnet** (Primary) - Chain ID: 11155111
- **Base** (Future) - Coming soon
- **Polygon** (Roadmap) - Planned support

## 📖 Documentation

- **[Agent Documentation](agents/README.md)** - Detailed agent usage and API
- **[Smart Contracts](contracts/)** - Contract specifications and deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation for API changes
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the component-specific README files
- **Community**: Join our discussions for questions and support

## 🔮 Roadmap

- [ ] Multi-chain support (Polygon, Arbitrum)
- [ ] Advanced evaluation metrics
- [ ] Decentralized storage integration
- [ ] Mobile application
- [ ] API rate limiting and quotas
- [ ] Advanced analytics dashboard
