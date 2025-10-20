# Scripts Directory

This directory contains TypeScript/JavaScript tools and utilities for interacting with the Truth Swarm attestation system. These scripts provide command-line interfaces and utilities for managing attestations, schemas, and blockchain interactions.

## 🎯 Overview

The scripts directory provides:
- **Schema Management**: Register and manage attestation schemas
- **Agent Evaluation**: Process agent evaluation data
- **Attestation Creation**: Create and manage attestations
- **IPFS Storage**: Store evaluation details on IPFS
- **Blockchain Utilities**: Helper functions for blockchain interactions

## 🏗️ Structure

```
scripts/
├── src/                      # TypeScript source files
│   ├── 0-evaluation-script.ts    # Main evaluation processing script
│   ├── 1-agent-evaluation.ts     # Agent evaluation utilities
│   ├── 2-agent-attestation.ts    # Attestation creation utilities
│   ├── abis.ts                   # Contract ABIs and interfaces
│   ├── attestation-info.ts        # Attestation information utilities
│   ├── human-attestation.ts      # Human verification utilities
│   ├── ipfs-storage.ts           # IPFS storage utilities
│   ├── schema-setup.ts           # Schema registration utilities
│   ├── type.ts                   # TypeScript type definitions
│   └── utils.ts                  # General utility functions
├── js-build/                 # Compiled JavaScript files
│   ├── *.js                      # Compiled JavaScript versions
├── package.json              # Node.js dependencies
├── tsconfig.json             # TypeScript configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** with npm
- **TypeScript** (installed via npm)
- **Access to Ethereum RPC** endpoint
- **Private key** for signing transactions

### Installation

```bash
# Install dependencies
npm install

# Build TypeScript files
npm run build
```

### Configuration

Create a `.env` file in the scripts directory:

```bash
# Ethereum Configuration
RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_private_key_here
CHAIN_ID=11155111

# Contract Addresses
EAS_CONTRACT_ADDRESS=0x4200000000000000000000000000000000000021
RESOLVER_CONTRACT_ADDRESS=your_resolver_contract_address

# IPFS Configuration
IPFS_GATEWAY=https://ipfs.io/ipfs/
```

## 📖 Usage

### Schema Setup

Register attestation schemas for agent evaluations and human verifications:

```bash
# Register agent evaluation schema
node js-build/schema-setup.js --type agent-evaluation

# Register human verification schema
node js-build/schema-setup.js --type human-verification
```

### Agent Evaluation

Process agent evaluation data and create attestations:

```bash
# Run evaluation script
node js-build/0-evaluation-script.js

# Process specific evaluation
node js-build/1-agent-evaluation.js --evaluation-id "eval_001"
```

### Attestation Management

Create and manage attestations:

```bash
# Create agent evaluation attestation
node js-build/2-agent-attestation.js --evaluation-data "path/to/evaluation.json"

# Create human verification attestation
node js-build/human-attestation.js --verification-data "path/to/verification.json"
```

### IPFS Storage

Store evaluation details on IPFS:

```bash
# Store evaluation data
node js-build/ipfs-storage.js --data "path/to/data.json" --type evaluation

# Retrieve stored data
node js-build/ipfs-storage.js --cid "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
```

## 🔧 Script Details

### 0-evaluation-script.ts

Main evaluation processing script that:
- Validates evaluation data
- Stores data on IPFS
- Creates attestations
- Handles error scenarios

**Usage:**
```bash
node js-build/0-evaluation-script.js [options]
```

**Options:**
- `--evaluation-file`: Path to evaluation data file
- `--schema-uid`: Schema UID for attestation
- `--dry-run`: Validate without creating attestation

### 1-agent-evaluation.ts

Agent evaluation utilities for:
- Processing evaluation scores
- Validating evaluation data
- Calculating effective scores
- Generating evaluation summaries

**Usage:**
```bash
node js-build/1-agent-evaluation.js --evaluation-id "eval_001"
```

### 2-agent-attestation.ts

Attestation creation utilities for:
- Creating evaluation attestations
- Managing attestation metadata
- Handling attestation errors
- Verifying attestation creation

**Usage:**
```bash
node js-build/2-agent-attestation.js --evaluation-data "path/to/evaluation.json"
```

### schema-setup.ts

Schema registration utilities for:
- Registering agent evaluation schemas
- Registering human verification schemas
- Managing schema metadata
- Updating schema configurations

**Usage:**
```bash
node js-build/schema-setup.js --type agent-evaluation
node js-build/schema-setup.js --type human-verification
```

### ipfs-storage.ts

IPFS storage utilities for:
- Storing evaluation data
- Retrieving stored data
- Managing IPFS metadata
- Handling storage errors

**Usage:**
```bash
node js-build/ipfs-storage.js --data "path/to/data.json" --type evaluation
node js-build/ipfs-storage.js --cid "bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
```

### human-attestation.ts

Human verification utilities for:
- Creating human verification attestations
- Managing verification data
- Handling verification errors
- Verifying attestation approval

**Usage:**
```bash
node js-build/human-attestation.js --verification-data "path/to/verification.json"
```

## 📊 Data Structures

### Evaluation Data

```typescript
interface EvaluationData {
  evaluatedAgentAddress: string;
  evaluatorAgentAddress: string;
  timestamp: number;
  finalScore: number;
  overallConfidence: number;
  grade: string;
  correctnessScore: number;
  correctnessConfidence: number;
  correctnessEffectiveScore: number;
  correctnessWeight: number;
  capabilitiesScore: number;
  capabilitiesConfidence: number;
  capabilitiesEffectiveScore: number;
  capabilitiesWeight: number;
  domainScore: number;
  domainConfidence: number;
  domainEffectiveScore: number;
  domainWeight: number;
  detailsCID: string;
}
```

### Human Verification Data

```typescript
interface HumanVerificationData {
  originalAttestationUID: string;
  verifier: string;
  timestamp: number;
  approved: boolean;
  comment: string;
}
```

### Attestation Request

```typescript
interface AttestationRequest {
  schemaUID: string;
  data: string;
  expirationTime: number;
  revocable: boolean;
  refUID: string;
  value: string;
  deadline: number;
}
```

## 🔧 Development

### Building

```bash
# Build TypeScript files
npm run build

# Watch for changes
npm run watch

# Clean build directory
npm run clean
```

### Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

### Linting

```bash
# Lint TypeScript files
npm run lint

# Fix linting issues
npm run lint:fix
```

## 📦 Dependencies

### Core Dependencies

- **ethers**: Ethereum library for blockchain interactions
- **ipfs-http-client**: IPFS client for decentralized storage
- **dotenv**: Environment variable management
- **commander**: Command-line interface framework

### Development Dependencies

- **typescript**: TypeScript compiler
- **@types/node**: Node.js type definitions
- **ts-node**: TypeScript execution for Node.js
- **jest**: Testing framework
- **eslint**: Code linting

## 🔒 Security Considerations

### Private Key Management

- **Never commit private keys** to version control
- Use environment variables for sensitive data
- Consider using hardware wallets for production

### Input Validation

- All input data is validated before processing
- Schema validation ensures data integrity
- Gas limits prevent excessive transaction costs

### Error Handling

- Comprehensive error handling for all operations
- Detailed error messages for debugging
- Graceful failure handling

## 🐛 Troubleshooting

### Common Issues

1. **RPC Connection Errors**: Verify RPC endpoint connectivity
2. **Gas Estimation Failures**: Increase gas limits in configuration
3. **Schema Registration Errors**: Ensure schema data is valid
4. **IPFS Storage Errors**: Check IPFS gateway connectivity

### Debug Mode

Enable debug logging:

```bash
DEBUG=true node js-build/0-evaluation-script.js
```

### Logging

All scripts provide detailed logging:
- **INFO**: General operation status
- **WARNING**: Non-critical issues
- **ERROR**: Critical failures
- **DEBUG**: Detailed debugging information

## 🤝 Contributing

When contributing to the scripts:

1. Follow existing code style and patterns
2. Add comprehensive tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

### Development Guidelines

- Use TypeScript for all new code
- Include comprehensive JSDoc comments
- Add error handling for all operations
- Follow the existing file structure

## 📚 Additional Resources

- [Ethers.js Documentation](https://docs.ethers.org/)
- [IPFS Documentation](https://docs.ipfs.io/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Node.js Documentation](https://nodejs.org/docs/)
