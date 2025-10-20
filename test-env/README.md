# Test Environment

This directory contains a complete local test environment for testing the Truth Swarm attestation system. It provides a comprehensive testing setup using Hardhat for local blockchain simulation and Python integration tests.

## 🎯 Overview

The test environment provides:
- **Local Blockchain**: Hardhat network for testing
- **Mock Contracts**: Simplified EAS and AttesterResolver contracts
- **Integration Tests**: End-to-end agent testing
- **Contract Tests**: Smart contract unit tests
- **Test Data**: Sample evaluation and verification data

## 🏗️ Architecture

```
test-env/
├── contracts/                 # Smart contracts for testing
│   ├── AttesterResolver.sol   # Custom resolver contract
│   ├── MockEAS.sol            # Simplified EAS for testing
│   └── lib/                   # Contract dependencies
├── scripts/                   # Deployment and utility scripts
│   └── deploy.js              # Contract deployment script
├── test/                      # Contract unit tests
│   └── AttesterResolver.test.js # Comprehensive contract tests
├── test_agent_simple.py       # Simple agent integration test
├── test_agent_integration.py  # Full integration test suite
├── test_runner.py             # Test orchestration script
├── config.local.env           # Local test configuration
├── deployment.json            # Contract deployment addresses
├── hardhat.config.js          # Hardhat configuration
├── package.json               # Node.js dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** with virtual environment
- **Node.js 18+** with npm
- **Git** for version control

### 1. Setup Environment

```bash
# Run the setup script
./setup.sh
```

This will:
- Install all dependencies
- Compile contracts
- Run contract tests
- Set up the test environment

### 2. Run Tests

```bash
# Simple agent test (recommended for quick verification)
python test_agent_simple.py

# Full integration test suite
python test_agent_integration.py

# Run all tests
python test_runner.py all
```

### 3. Manual Testing

For manual testing and debugging:

```bash
# Terminal 1: Start Hardhat node
npx hardhat node

# Terminal 2: Deploy contracts
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Run agent tests
python test_agent_simple.py
```

## 📁 File Structure

### Smart Contracts

- **`AttesterResolver.sol`**: Custom resolver contract that controls attestation authorization
- **`MockEAS.sol`**: Simplified Ethereum Attestation Service for local testing
- **`lib/`**: Contract dependencies and interfaces

### Test Scripts

- **`test_agent_simple.py`**: Basic agent functionality test
- **`test_agent_integration.py`**: Comprehensive integration test
- **`test_runner.py`**: Test orchestration and management

### Configuration

- **`config.local.env`**: Local test configuration
- **`deployment.json`**: Contract deployment addresses
- **`hardhat.config.js`**: Hardhat network configuration

## 🧪 Testing

### Contract Tests

Test smart contracts in isolation:

```bash
# Run all contract tests
npx hardhat test

# Run specific test file
npx hardhat test test/AttesterResolver.test.js

# Run tests with gas reporting
REPORT_GAS=true npx hardhat test
```

### Agent Integration Tests

Test Python agent against contracts:

```bash
# Simple test (5 phases)
python test_agent_simple.py

# Full integration test
python test_agent_integration.py

# Test specific components
python test_runner.py agent
python test_runner.py contracts
```

### Test Scenarios

The integration tests cover:

1. **Contract Deployment**: Deploy MockEAS and AttesterResolver
2. **Schema Registration**: Register agent evaluation and human verification schemas
3. **Authorization**: Test authorized vs unauthorized attesters
4. **Attestation Creation**: Create evaluation attestations
5. **Human Verification**: Create human verification attestations
6. **Error Handling**: Test various error scenarios

## 🔧 Configuration

### Local Configuration

The `config.local.env` file contains:

```bash
# Blockchain Configuration
RPC_URL=http://127.0.0.1:8545
CHAIN_ID=31337

# Contract Addresses (populated after deployment)
EAS_CONTRACT_ADDRESS=
RESOLVER_CONTRACT_ADDRESS=

# Test Accounts
AUTHORIZED_ATTESTER=0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
UNAUTHORIZED_ATTESTER=0x70997970C51812dc3A010C7d01b50e0d17dc79C8

# Test Configuration
GAS_LIMIT=3000000
GAS_PRICE=20000000000
```

### Hardhat Accounts

The test environment uses Hardhat's default accounts:

- **Account #0**: `0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266` (Authorized)
- **Account #1**: `0x70997970C51812dc3A010C7d01b50e0d17dc79C8` (Unauthorized)
- **Account #2**: `0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC` (Test account)

## 📊 Test Data

### Sample Evaluation Data

```python
evaluation_data = EvaluationScore(
    evaluatedAgentAddress="0x1234567890123456789012345678901234567890",
    evaluatorAgentAddress="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
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
```

### Sample Human Verification Data

```python
verification_data = HumanVerificationData(
    originalAttestationUID=attestation_uid,
    verifier="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
    timestamp=int(time.time()),
    approved=True,
    comment="Verified manually - agent performed well in tests"
)
```

## 🔍 Test Phases

### Simple Test (test_agent_simple.py)

1. **Phase 1**: Connect to local blockchain
2. **Phase 2**: Check agent authorization
3. **Phase 3**: Process evaluation data
4. **Phase 4**: Create evaluation attestation
5. **Phase 5**: Verify attestation creation

### Integration Test (test_agent_integration.py)

1. **Setup**: Start Hardhat node and deploy contracts
2. **Schema Registration**: Register evaluation and verification schemas
3. **Authorization Test**: Test authorized vs unauthorized attesters
4. **Evaluation Attestation**: Create agent evaluation attestations
5. **Human Verification**: Create human verification attestations
6. **Error Handling**: Test various error scenarios
7. **Cleanup**: Stop Hardhat node and clean up

## 🐛 Debugging

### Common Issues

1. **Port Already in Use**: Make sure port 8545 is free
2. **Contract Compilation Errors**: Check Solidity version compatibility
3. **Python Import Errors**: Ensure you're running from the correct directory
4. **Gas Estimation Failures**: Increase gas limits in configuration

### Debug Commands

```bash
# Check if Hardhat node is running
curl -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' \
  http://127.0.0.1:8545

# View contract deployment info
cat deployment.json | jq

# Check Hardhat logs
npx hardhat node --verbose

# Test contract interaction
npx hardhat console --network localhost
```

### Debug Mode

Enable debug logging:

```bash
# Python debug mode
DEBUG=true python test_agent_simple.py

# Hardhat debug mode
npx hardhat node --verbose
```

## 🔄 Test Workflow

### Development Workflow

1. **Make Changes**: Modify contracts or agent code
2. **Run Tests**: Execute relevant test suite
3. **Debug Issues**: Use debug commands and logging
4. **Fix Problems**: Address any test failures
5. **Verify Fixes**: Re-run tests to confirm fixes

### Continuous Integration

For CI/CD pipelines:

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run contract tests
npx hardhat test

# Run agent tests
python test_agent_simple.py
```

## 📈 Performance

### Test Performance

- **Contract Tests**: ~30 seconds for full suite
- **Agent Tests**: ~60 seconds for integration test
- **Gas Usage**: Monitored and reported in tests
- **Memory Usage**: Optimized for CI/CD environments

### Optimization

- **Parallel Testing**: Run multiple test suites in parallel
- **Caching**: Cache contract compilation results
- **Selective Testing**: Run only relevant tests during development

## 🔒 Security

### Test Security

- **Isolated Environment**: Tests run in isolated local environment
- **No Real Funds**: Uses test accounts with no real value
- **Secure Configuration**: Sensitive data in environment variables
- **Access Control**: Tests authorization mechanisms

### Best Practices

- **Never commit private keys**: Use test accounts only
- **Validate inputs**: Test input validation mechanisms
- **Error handling**: Test error scenarios and edge cases
- **Gas limits**: Test gas estimation and limits

## 🤝 Contributing

When adding new tests:

1. **Add Contract Tests**: Add tests in `test/` directory
2. **Add Agent Tests**: Add integration tests in Python files
3. **Update Documentation**: Update this README with new test scenarios
4. **Ensure Coverage**: Maintain high test coverage
5. **Test Everything**: Ensure all tests pass before committing

### Test Guidelines

- **Comprehensive Coverage**: Test all major functionality
- **Edge Cases**: Test error scenarios and edge cases
- **Clear Names**: Use descriptive test names
- **Documentation**: Document complex test scenarios
- **Performance**: Keep tests fast and efficient

## 📚 Additional Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [EAS Documentation](https://docs.attest.sh/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.html)

## 📝 Notes

- The MockEAS contract is simplified for testing and doesn't include all EAS features
- Schema UIDs are generated locally and won't match testnet/mainnet
- Gas costs are simulated and don't reflect real network costs
- This environment is for development/testing only
- Test accounts are pre-funded with test ETH for gas costs
