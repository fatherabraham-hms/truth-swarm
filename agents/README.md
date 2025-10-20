# Resolver Attestation Agent

The Resolver Attestation Agent is the core component of Truth Swarm that handles agent evaluation attestations using the Ethereum Attestation Service (EAS) and custom AttesterResolver smart contracts.

## 🎯 Overview

The agent processes evaluation data from AI agents, validates it, and creates verifiable attestations on the blockchain. It supports both automated agent evaluations and human verification workflows.

## 🏗️ Architecture

The agent consists of several key components:

- **ResolverAttestationAgent**: Main agent class for attestation operations
- **EvaluationScore**: Data structure for agent evaluation results
- **HumanVerificationData**: Data structure for human verification attestations
- **AttestationRequest**: Request structure for attestation creation

## 🚀 Features

### Core Functionality

- **Agent Evaluation Processing**: Validates and processes evaluation data from AI agents
- **Attestation Creation**: Creates verifiable attestations on the blockchain
- **Human Verification**: Manages human verification workflows
- **Authorization Management**: Controls who can create attestations
- **Schema Management**: Handles attestation schemas for different data types

### Advanced Features

- **Async/Await Support**: Full async support for blockchain interactions
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Error Handling**: Robust error handling for network and contract issues
- **Gas Optimization**: Automatic gas estimation and optimization
- **Batch Processing**: Support for processing multiple evaluations

## 📦 Installation

### Prerequisites

- Python 3.13+
- Web3.py
- aiohttp
- eth-account

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy configuration template
cp config.template .env

# Edit .env with your configuration
```

## 🔧 Configuration

The agent requires the following configuration:

```python
agent = ResolverAttestationAgent(
    rpc_url="https://sepolia.infura.io/v3/YOUR_PROJECT_ID",
    eas_contract_address="0x4200000000000000000000000000000000000021",
    resolver_contract_address="YOUR_RESOLVER_CONTRACT_ADDRESS",
    private_key="YOUR_PRIVATE_KEY",
    chain_id=11155111  # Sepolia testnet
)
```

### Environment Variables

- `RPC_URL`: Ethereum RPC endpoint
- `EAS_CONTRACT_ADDRESS`: EAS contract address
- `RESOLVER_CONTRACT_ADDRESS`: AttesterResolver contract address
- `PRIVATE_KEY`: Private key for signing transactions
- `CHAIN_ID`: Ethereum chain ID

## 📖 Usage

### Basic Agent Evaluation

```python
from agents.resolver_atestation_agent import ResolverAttestationAgent, EvaluationScore
import time

# Initialize the agent
agent = ResolverAttestationAgent(
    rpc_url="https://sepolia.infura.io/v3/YOUR_PROJECT_ID",
    eas_contract_address="0x4200000000000000000000000000000000000021",
    resolver_contract_address="YOUR_RESOLVER_CONTRACT_ADDRESS",
    private_key="YOUR_PRIVATE_KEY",
    chain_id=11155111
)

# Create evaluation data
evaluation_data = EvaluationScore(
    evaluatedAgentAddress="0x1234567890123456789012345678901234567890",
    evaluatorAgentAddress=agent.address,
    timestamp=int(time.time()),
    finalScore=85,
    overallConfidence=8,
    grade="B+",
    correctnessScore=90,
    correctnessConfidence=9,
    correctnessEffectiveScore=81,
    correctnessWeight=40,
    capabilitiesScore=80,
    capabilitiesConfidence=7,
    capabilitiesEffectiveScore=56,
    capabilitiesWeight=30,
    domainScore=85,
    domainConfidence=8,
    domainEffectiveScore=68,
    domainWeight=30,
    detailsCID="bafkreih5aznjvttude6c3w2l5y6kmzq7l4fex2k4d3a2b1c9d8e7f6g5h4i3j2k1l"
)

# Process evaluation and create attestation
if await agent.process_evaluation_data(evaluation_data):
    attestation_uid = await agent.create_evaluation_attestation(evaluation_data)
    print(f"Evaluation attestation created: {attestation_uid}")
```

### Human Verification

```python
from agents.resolver_atestation_agent import HumanVerificationData

# Create human verification data
verification_data = HumanVerificationData(
    originalAttestationUID=attestation_uid,
    verifier=agent.address,
    timestamp=int(time.time()),
    approved=True,
    comment="Verified manually - agent performed well in tests"
)

# Create human verification attestation
human_attestation_uid = await agent.create_human_verification_attestation(verification_data)
print(f"Human verification attestation created: {human_attestation_uid}")
```

### Authorization Management

```python
# Check if agent is authorized
is_authorized = await agent._is_authorized_attester()
print(f"Agent authorized: {is_authorized}")

# Get authorized attesters
attesters = await agent.get_authorized_attesters()
print(f"Authorized attesters: {attesters}")
```

## 📊 Data Structures

### EvaluationScore

Represents a comprehensive agent evaluation:

```python
@dataclass
class EvaluationScore:
    evaluatedAgentAddress: str      # Address of the agent being evaluated
    evaluatorAgentAddress: str     # Address of the evaluating agent
    timestamp: int                 # Unix timestamp of evaluation
    finalScore: int               # Overall score (0-100)
    overallConfidence: int        # Confidence level (1-10)
    grade: str                    # Letter grade (A+, A, B+, etc.)
    
    # Detailed scoring breakdown
    correctnessScore: int         # Correctness score (0-100)
    correctnessConfidence: int   # Correctness confidence (1-10)
    correctnessEffectiveScore: int  # Weighted correctness score
    correctnessWeight: int        # Weight percentage for correctness
    
    capabilitiesScore: int       # Capabilities score (0-100)
    capabilitiesConfidence: int  # Capabilities confidence (1-10)
    capabilitiesEffectiveScore: int  # Weighted capabilities score
    capabilitiesWeight: int      # Weight percentage for capabilities
    
    domainScore: int             # Domain knowledge score (0-100)
    domainConfidence: int        # Domain confidence (1-10)
    domainEffectiveScore: int    # Weighted domain score
    domainWeight: int            # Weight percentage for domain
    
    detailsCID: str              # IPFS CID for detailed evaluation data
```

### HumanVerificationData

Represents human verification of an attestation:

```python
@dataclass
class HumanVerificationData:
    originalAttestationUID: str   # UID of the original attestation
    verifier: str                # Address of the human verifier
    timestamp: int              # Unix timestamp of verification
    approved: bool              # Whether the attestation is approved
    comment: str                # Human comment on the verification
```

## 🔍 API Reference

### Core Methods

#### `process_evaluation_data(evaluation_data: EvaluationScore) -> bool`

Processes and validates evaluation data before attestation creation.

**Parameters:**
- `evaluation_data`: The evaluation data to process

**Returns:**
- `bool`: True if processing successful, False otherwise

#### `create_evaluation_attestation(evaluation_data: EvaluationScore) -> str`

Creates an attestation for agent evaluation data.

**Parameters:**
- `evaluation_data`: The evaluation data to attest

**Returns:**
- `str`: Attestation UID if successful, None otherwise

#### `create_human_verification_attestation(verification_data: HumanVerificationData) -> str`

Creates a human verification attestation.

**Parameters:**
- `verification_data`: The verification data

**Returns:**
- `str`: Attestation UID if successful, None otherwise

#### `_is_authorized_attester() -> bool`

Checks if the current agent is authorized to create attestations.

**Returns:**
- `bool`: True if authorized, False otherwise

#### `get_authorized_attesters() -> List[str]`

Gets the list of authorized attesters.

**Returns:**
- `List[str]`: List of authorized attester addresses

## 🧪 Testing

### Local Testing

```bash
# Run simple agent test
cd test-env
python test_agent_simple.py

# Run integration test
python test_agent_integration.py
```

### Test Scenarios

The agent tests cover:

1. **Authorization Check**: Verify agent authorization status
2. **Evaluation Processing**: Test evaluation data validation
3. **Attestation Creation**: Test evaluation attestation creation
4. **Human Verification**: Test human verification workflow
5. **Error Handling**: Test various error scenarios

## 🔒 Security Considerations

### Private Key Management

- **Never commit private keys** to version control
- Use environment variables for sensitive data
- Consider using hardware wallets for production

### Input Validation

- All input data is validated before processing
- Schema validation ensures data integrity
- Gas limits prevent excessive transaction costs

### Authorization

- Only authorized attesters can create attestations
- Authorization is checked on-chain
- Regular authorization audits recommended

## 🐛 Error Handling

The agent includes comprehensive error handling:

- **Network Errors**: Retry logic for network issues
- **Contract Errors**: Detailed error messages for contract failures
- **Validation Errors**: Clear validation error messages
- **Gas Errors**: Automatic gas estimation and adjustment

### Common Error Scenarios

1. **Insufficient Gas**: Increase gas limit in configuration
2. **Unauthorized**: Ensure agent is in authorized attesters list
3. **Invalid Data**: Check evaluation data structure and values
4. **Network Issues**: Verify RPC endpoint connectivity

## 📈 Performance

### Optimization Features

- **Async Operations**: Non-blocking blockchain interactions
- **Gas Estimation**: Automatic gas optimization
- **Batch Processing**: Efficient handling of multiple evaluations
- **Connection Pooling**: Reuse of HTTP connections

### Monitoring

- **Comprehensive Logging**: Detailed operation logs
- **Performance Metrics**: Track operation timing
- **Error Tracking**: Monitor and alert on errors

## 🤝 Contributing

When contributing to the agent:

1. Follow existing code style and patterns
2. Add comprehensive tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

### Development Guidelines

- Use type hints for all function parameters and returns
- Include comprehensive docstrings
- Add logging for important operations
- Handle errors gracefully with appropriate messages

## 📚 Additional Resources

- [EAS Documentation](https://docs.attest.sh/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Ethereum Development Guide](https://ethereum.org/developers/)
