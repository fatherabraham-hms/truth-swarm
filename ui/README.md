# UI Directory

This directory contains the Next.js user interface for Truth Swarm, providing a web-based interface for managing attestations, viewing agent evaluations, and handling human verifications.

## 🎯 Overview

The UI provides:

- **Attestation Management**: Create and view attestations
- **Agent Evaluation**: Submit and review evaluation data
- **Human Verification**: Verify attestations manually
- **Dashboard**: Overview of attestation status and metrics
- **Real-time Updates**: Live updates of attestation status

## 🏗️ Structure

```
ui/
├── src/
│   ├── actions/              # Server actions
│   │   └── attestation.ts    # Attestation-related actions
│   ├── hooks/                # React hooks
│   │   └── useAttestation.ts # Attestation management hook
│   ├── lib/                  # Utility libraries
│   │   └── attestation-utils.ts # Attestation utilities
│   ├── types/                # TypeScript type definitions
│   │   └── attestation.ts    # Attestation types
│   └── components/           # React components (to be added)
├── next-env.d.ts            # Next.js type definitions
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** with npm
- **Next.js 14+** (installed via npm)
- **Access to Ethereum RPC** endpoint
- **Wallet connection** (MetaMask, WalletConnect, etc.)

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Configuration

Create a `.env.local` file in the ui directory:

```bash
# Ethereum Configuration
NEXT_PUBLIC_RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
NEXT_PUBLIC_CHAIN_ID=11155111

# Contract Addresses
NEXT_PUBLIC_EAS_CONTRACT_ADDRESS=0x4200000000000000000000000000000000000021
NEXT_PUBLIC_RESOLVER_CONTRACT_ADDRESS=your_resolver_contract_address

# IPFS Configuration
NEXT_PUBLIC_IPFS_GATEWAY=https://ipfs.io/ipfs/
```

## 📖 Features

### Attestation Management

- **Create Attestations**: Submit new agent evaluations
- **View Attestations**: Browse existing attestations
- **Search & Filter**: Find specific attestations
- **Export Data**: Download attestation data

### Agent Evaluation

- **Submit Evaluations**: Upload agent evaluation data
- **Review Scores**: View detailed scoring breakdowns
- **Track Progress**: Monitor evaluation status
- **Historical Data**: Access past evaluations

### Human Verification

- **Verify Attestations**: Manually verify agent evaluations
- **Add Comments**: Provide feedback on evaluations
- **Approve/Reject**: Make verification decisions
- **Track Verification**: Monitor verification status

### Dashboard

- **Overview Metrics**: Key performance indicators
- **Recent Activity**: Latest attestations and verifications
- **Status Summary**: Overall system status
- **Quick Actions**: Common tasks and shortcuts

## 🔧 Components

### useAttestation Hook

Custom React hook for attestation management:

```typescript
import { useAttestation } from "@/hooks/useAttestation";

function AttestationComponent() {
  const {
    attestations,
    loading,
    error,
    createAttestation,
    verifyAttestation,
    refreshAttestations,
  } = useAttestation();

  // Use the hook in your component
}
```

**Hook Methods:**

- `createAttestation(data)`: Create a new attestation
- `verifyAttestation(uid, approved, comment)`: Verify an attestation
- `refreshAttestations()`: Refresh attestation data
- `getAttestation(uid)`: Get specific attestation details

### Attestation Actions

Server actions for attestation operations:

```typescript
import { createAttestation, verifyAttestation } from "@/actions/attestation";

// Create attestation
const result = await createAttestation({
  schemaUID: "0x...",
  data: "0x...",
  expirationTime: 0,
  revocable: true,
});

// Verify attestation
const verification = await verifyAttestation({
  attestationUID: "0x...",
  approved: true,
  comment: "Verified manually",
});
```

### Attestation Utilities

Utility functions for attestation operations:

```typescript
import {
  formatAttestationData,
  validateAttestationData,
  calculateEffectiveScore,
} from "@/lib/attestation-utils";

// Format evaluation data for attestation
const formattedData = formatAttestationData(evaluationData);

// Validate attestation data
const isValid = validateAttestationData(attestationData);

// Calculate effective score
const effectiveScore = calculateEffectiveScore(scores, weights);
```

## 📊 Data Types

### Attestation Types

```typescript
interface Attestation {
  uid: string;
  schemaUID: string;
  attester: string;
  recipient: string;
  data: string;
  timestamp: number;
  expirationTime: number;
  revocable: boolean;
  revoked: boolean;
  refUID: string;
  value: string;
}

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

interface HumanVerificationData {
  originalAttestationUID: string;
  verifier: string;
  timestamp: number;
  approved: boolean;
  comment: string;
}
```

## 🎨 UI Components

### Planned Components

- **AttestationCard**: Display individual attestations
- **EvaluationForm**: Submit agent evaluations
- **VerificationPanel**: Human verification interface
- **Dashboard**: Overview and metrics
- **SearchBar**: Find attestations
- **StatusIndicator**: Show attestation status
- **ScoreBreakdown**: Detailed scoring visualization

### Component Structure

```typescript
// Example component structure
interface AttestationCardProps {
  attestation: Attestation;
  onVerify?: (uid: string, approved: boolean) => void;
  onView?: (uid: string) => void;
}

function AttestationCard({
  attestation,
  onVerify,
  onView,
}: AttestationCardProps) {
  // Component implementation
}
```

## 🔧 Development

### Running the Application

```bash
# Development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Environment Setup

1. **Copy environment template**:

   ```bash
   cp .env.example .env.local
   ```

2. **Configure environment variables**:

   - Set RPC URL and chain ID
   - Add contract addresses
   - Configure IPFS gateway

3. **Install dependencies**:
   ```bash
   npm install
   ```

### Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## 📦 Dependencies

### Core Dependencies

- **next**: React framework for production
- **react**: UI library
- **react-dom**: React DOM rendering
- **ethers**: Ethereum library for blockchain interactions
- **wagmi**: React hooks for Ethereum
- **viem**: TypeScript interface for Ethereum

### UI Dependencies

- **@radix-ui/react-\***: UI component primitives
- **tailwindcss**: CSS framework
- **lucide-react**: Icon library
- **framer-motion**: Animation library

### Development Dependencies

- **typescript**: TypeScript compiler
- **@types/react**: React type definitions
- **@types/node**: Node.js type definitions
- **eslint**: Code linting
- **prettier**: Code formatting

## 🔒 Security Considerations

### Wallet Integration

- **Secure wallet connection**: Use established wallet providers
- **Private key protection**: Never expose private keys
- **Transaction signing**: Handle signing securely

### Data Validation

- **Input validation**: Validate all user inputs
- **Schema validation**: Ensure data matches expected schemas
- **Sanitization**: Sanitize user-generated content

### Error Handling

- **Graceful failures**: Handle errors without exposing sensitive data
- **User feedback**: Provide clear error messages
- **Logging**: Log errors for debugging without exposing data

## 🐛 Troubleshooting

### Common Issues

1. **Wallet Connection**: Ensure wallet is properly connected
2. **RPC Errors**: Verify RPC endpoint connectivity
3. **Contract Errors**: Check contract addresses and ABI
4. **Build Errors**: Ensure all dependencies are installed

### Debug Mode

Enable debug logging:

```bash
DEBUG=true npm run dev
```

### Browser Console

Check browser console for:

- Wallet connection errors
- Contract interaction errors
- Network connectivity issues

## 🤝 Contributing

When contributing to the UI:

1. Follow existing code style and patterns
2. Add comprehensive tests for new components
3. Update documentation for API changes
4. Ensure all tests pass before submitting

### Development Guidelines

- Use TypeScript for all new code
- Follow React best practices
- Include comprehensive JSDoc comments
- Add error handling for all operations
- Follow the existing component structure

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Wagmi Documentation](https://wagmi.sh/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Radix UI Documentation](https://www.radix-ui.com/)
