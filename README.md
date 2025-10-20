# Truth Swarm

Truth Swarm is a verification mechanism for consumer protections in the age of agentic AI. It provides a decentralized attestation system that enables AI agents to create verifiable evaluations and human verifications of other agents' performance.

## 🎯 Overview

Truth Swarm implements a comprehensive attestation system using:
- **Ethereum Attestation Service (EAS)** for creating verifiable attestations
- **Smart contracts** for managing authorization and attestation logic
- **Python agents** for processing evaluations and creating attestations
- **TypeScript/JavaScript tools** for blockchain interactions
- **Next.js UI** for user interfaces

## 🏗️ Architecture

```
truth-swarm/
├── agents/                    # Python agent implementations
│   ├── resolver_atestation_agent.py  # Main attestation agent
│   └── README.md              # Agent documentation
├── contracts/                 # Smart contracts
│   └── resolver.sol          # AttesterResolver contract
├── scripts/                   # TypeScript/JavaScript tools
│   ├── src/                  # TypeScript source files
│   ├── js-build/            # Compiled JavaScript files
│   └── package.json         # Node.js dependencies
├── test-env/                 # Local testing environment
│   ├── contracts/           # Test contracts (MockEAS, AttesterResolver)
│   ├── test/               # Contract tests
│   ├── test_agent_*.py     # Agent integration tests
│   └── README.md           # Test environment documentation
├── ui/                      # Next.js user interface
│   ├── src/                # React components and utilities
│   └── package.json        # UI dependencies
├── requirements.txt         # Python dependencies
├── config.template         # Configuration template
└── README.md              # This file
```

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
cp config.template .env

# Edit .env with your settings:
# - RPC_URL: Ethereum RPC endpoint
# - PRIVATE_KEY: Your wallet private key
# - EAS_CONTRACT_ADDRESS: EAS contract address
# - RESOLVER_CONTRACT_ADDRESS: Your resolver contract address
```

### 3. Local Testing

```bash
# Run the complete test suite
cd test-env
python test_agent_simple.py
```

## 📚 Components

### 🤖 Agents (`agents/`)

The Python agent system handles:
- **Evaluation Processing**: Validates and processes agent evaluation data
- **Attestation Creation**: Creates verifiable attestations on-chain
- **Human Verification**: Manages human verification workflows
- **Authorization Management**: Controls who can create attestations

**Key Features:**
- Async/await support for blockchain interactions
- Comprehensive error handling and logging
- Batch processing capabilities
- Gas optimization

### 🔗 Smart Contracts (`contracts/`)

The AttesterResolver contract provides:
- **Authorization Control**: Manages authorized attesters
- **Attestation Validation**: Ensures only authorized users can attest
- **Schema Management**: Handles attestation schemas
- **Upgradeability**: Supports contract upgrades

### 🛠️ Scripts (`scripts/`)

TypeScript/JavaScript tools for:
- **Schema Setup**: Register attestation schemas
- **Agent Evaluation**: Process evaluation data
- **Attestation Management**: Create and manage attestations
- **IPFS Storage**: Store evaluation details on IPFS

### 🧪 Test Environment (`test-env/`)

Complete local testing setup:
- **MockEAS Contract**: Simplified EAS for testing
- **Hardhat Network**: Local blockchain
- **Integration Tests**: End-to-end agent testing
- **Contract Tests**: Smart contract unit tests

### 🎨 User Interface (`ui/`)

Next.js application providing:
- **Attestation Management**: Create and view attestations
- **Agent Evaluation**: Submit evaluation data
- **Human Verification**: Verify attestations manually
- **Dashboard**: Overview of attestation status

## 🔧 Development

### Running Tests

```bash
# Contract tests
cd test-env
npx hardhat test

# Agent integration tests
python test_agent_simple.py
python test_agent_integration.py

# Complete test suite
python test_runner.py all
```

### Building Scripts

```bash
cd scripts
npm run build
```

### Running UI

```bash
cd ui
npm run dev
```

## 📖 Documentation

- **[Agent Documentation](agents/README.md)** - Detailed agent usage and API
- **[Test Environment](test-env/README.md)** - Local testing setup and procedures
- **[Smart Contracts](contracts/)** - Contract specifications and deployment

## 🔒 Security

- **Private Key Management**: Use environment variables, never commit keys
- **Authorization**: Implement proper access controls
- **Input Validation**: Validate all data before processing
- **Gas Limits**: Monitor and set appropriate gas limits
- **Audit**: Regular security audits recommended

## 🌐 Deployment

### Testnet (Sepolia)

1. Deploy contracts to Sepolia testnet
2. Update configuration with testnet addresses
3. Run integration tests on testnet
4. Verify attestation creation and validation

### Mainnet

1. Complete security audit
2. Deploy contracts to mainnet
3. Update configuration with mainnet addresses
4. Monitor gas costs and performance

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
