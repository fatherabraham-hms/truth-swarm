# Truth Swarm - Smart Contracts

This directory contains the Solidity smart contracts for Truth Swarm's attestation system, built with Foundry.

## 🎯 Overview

Truth Swarm uses a custom resolver contract that integrates with the Ethereum Attestation Service (EAS) to create a permissioned attestation system. Only whitelisted agents can create attestations, ensuring quality control and preventing spam.

## 📜 Contracts

### TruthSwarmResolver (`src/Resolver.sol`)

A schema resolver that validates attestations from whitelisted agents.

**Key Features:**

- **Whitelist Management** - Owner-controlled list of authorized attesters
- **Attestation Validation** - Only whitelisted agents can create attestations
- **Event Emission** - Transparent logging of whitelist changes
- **Enumeration** - Query all whitelisted addresses

**Main Functions:**

```solidity
// Add an agent to the whitelist (owner only)
function addAttester(address attester) external onlyOwner

// Remove an agent from the whitelist (owner only)
function removeAttester(address attester) external onlyOwner

// Check if an address is whitelisted
function isWhitelisted(address attester) external view returns (bool)

// Get all whitelisted attesters
function getWhitelistedAttesters() external view returns (address[] memory)

// Get count of whitelisted attesters
function getWhitelistedCount() external view returns (uint256)
```

**Internal Hooks:**

```solidity
// Validates attestations (called by EAS)
function onAttest(Attestation calldata attestation, uint256 value)
    internal view override returns (bool)

// Validates revocations (called by EAS)
function onRevoke(Attestation calldata attestation, uint256 value)
    internal pure override returns (bool)
```

## 🚀 Deployed Contracts

> **Note:** The contracts are already deployed on Sepolia. You don't need to deploy them yourself unless you're setting up a custom instance.

### Sepolia Testnet

- **Network:** Sepolia
- **Chain ID:** 11155111
- **EAS Contract:** `0x4200000000000000000000000000000000000021`
- **TruthSwarmResolver:** _[Your deployed resolver address]_
- **Schema UID:** `0xcd0ab40423e8919b72b665cb563c82b895acc2b690626f2c8180e1db83f6f5bc`

### EAS Schema

The attestation schema includes:

```
string evaluatedAgentAddress,
string evaluatorAgentAddress,
uint256 timestamp,
uint256 finalScore,
uint8 overallConfidence,
string grade,
uint256 correctnessScore,
uint8 correctnessConfidence,
uint256 correctnessEffectiveScore,
uint8 correctnessWeight,
uint256 capabilitiesScore,
uint8 capabilitiesConfidence,
uint256 capabilitiesEffectiveScore,
uint8 capabilitiesWeight,
uint256 domainScore,
uint8 domainConfidence,
uint256 domainEffectiveScore,
uint8 domainWeight,
string detailsCID
```

## 🛠️ Development Setup

### Prerequisites

- **Foundry** - Fast Ethereum development toolkit
  ```bash
  curl -L https://foundry.paradigm.xyz | bash
  foundryup
  ```

### Installation

```bash
cd contracts
forge install  # Install dependencies
forge build    # Compile contracts
```

### Dependencies

- **EAS Contracts** (`lib/eas-contracts`) - Ethereum Attestation Service
- **OpenZeppelin** (`lib/openzeppelin-contracts`) - Security and access control

## 🧪 Testing

```bash
# Run all tests
forge test

# Run with verbose output
forge test -vvv

# Run specific test
forge test --match-test testAddAttester

# Generate gas report
forge test --gas-report

# Generate coverage report
forge coverage
```

### Test Files

Tests are located in `test/` directory:

- `Resolver.t.sol` - TruthSwarmResolver tests
- Coverage for whitelist management
- Attestation validation tests
- Access control tests

## 🚀 Deployment (Optional)

> **Note:** Only needed if deploying your own instance or testing on a different network.

### Deploy Script

Create `script/Deploy.s.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Script} from "forge-std/Script.sol";
import {TruthSwarmResolver} from "../src/Resolver.sol";
import {IEAS} from "../lib/eas-contracts/contracts/IEAS.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address easAddress = vm.envAddress("EAS_CONTRACT_ADDRESS");

        vm.startBroadcast(deployerPrivateKey);

        // Deploy with initial attesters
        address[] memory initialAttesters = new address[](1);
        initialAttesters[0] = vm.addr(deployerPrivateKey);

        TruthSwarmResolver resolver = new TruthSwarmResolver(
            IEAS(easAddress),
            initialAttesters
        );

        vm.stopBroadcast();

        console.log("Resolver deployed at:", address(resolver));
    }
}
```

### Deploy to Sepolia

```bash
# Set environment variables
export PRIVATE_KEY=your_private_key
export RPC_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID
export EAS_CONTRACT_ADDRESS=0x4200000000000000000000000000000000000021

# Deploy
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url $RPC_URL \
  --private-key $PRIVATE_KEY \
  --broadcast \
  --verify
```

### Register Schema on EAS

After deploying the resolver:

1. Go to [EAS Schema Registry](https://sepolia.easscan.org/schema/create)
2. Define the schema (see schema above)
3. Set the resolver address to your deployed `TruthSwarmResolver`
4. Note the schema UID for your agents

## 🔧 Foundry Commands

### Build

```bash
forge build                 # Compile contracts
forge build --watch        # Watch mode
```

### Test

```bash
forge test                 # Run all tests
forge test -vvv           # Verbose output
forge test --match-test testName  # Run specific test
```

### Format

```bash
forge fmt                  # Format all Solidity files
forge fmt --check         # Check formatting without changes
```

### Gas Snapshots

```bash
forge snapshot            # Generate gas snapshots
```

### Local Node

```bash
anvil                     # Start local Ethereum node
```

### Cast (Interact with Contracts)

```bash
# Query whitelist status
cast call $RESOLVER_ADDRESS "isWhitelisted(address)" $AGENT_ADDRESS --rpc-url $RPC_URL

# Get whitelisted count
cast call $RESOLVER_ADDRESS "getWhitelistedCount()" --rpc-url $RPC_URL

# Add attester (owner only)
cast send $RESOLVER_ADDRESS "addAttester(address)" $NEW_AGENT_ADDRESS \
  --private-key $PRIVATE_KEY \
  --rpc-url $RPC_URL
```

## 🔒 Security

### Access Control

- **Owner Role** - Can add/remove attesters from whitelist
- **Whitelisted Attesters** - Can create attestations via EAS
- **Public View Functions** - Anyone can query whitelist status

### Best Practices

- ✅ Uses OpenZeppelin's `Ownable` for access control
- ✅ Validates zero addresses
- ✅ Emits events for transparency
- ✅ Implements proper error handling
- ✅ Follows checks-effects-interactions pattern

### Auditing

Before deploying to mainnet:

1. Run comprehensive test suite
2. Perform gas optimization
3. Consider professional security audit
4. Test on testnets extensively

## 📁 Project Structure

```
contracts/
├── src/
│   └── Resolver.sol           # Main resolver contract
├── test/
│   └── Resolver.t.sol         # Contract tests
├── script/
│   └── Deploy.s.sol           # Deployment script
├── lib/
│   ├── eas-contracts/         # EAS dependencies
│   └── openzeppelin-contracts/ # OpenZeppelin libraries
├── foundry.toml               # Foundry configuration
└── README.md                  # This file
```

## 🔗 Useful Links

- **Foundry Book** - https://book.getfoundry.sh/
- **EAS Documentation** - https://docs.attest.sh/
- **EAS Sepolia Explorer** - https://sepolia.easscan.org/
- **OpenZeppelin Contracts** - https://docs.openzeppelin.com/contracts/

## 🐛 Troubleshooting

### Common Issues

1. **Build Errors**

   ```bash
   forge clean && forge build  # Clean and rebuild
   ```

2. **Dependency Issues**

   ```bash
   git submodule update --init --recursive
   forge install
   ```

3. **RPC Connection Issues**
   - Verify RPC URL is correct
   - Check API key limits
   - Try alternative RPC providers

### Getting Help

```bash
forge --help              # General help
forge build --help       # Command-specific help
cast --help              # Cast command help
```

## 🤝 Contributing

When contributing to contracts:

1. Write comprehensive tests for new features
2. Follow Solidity style guide
3. Add NatSpec documentation
4. Run `forge fmt` before committing
5. Ensure all tests pass with `forge test`
6. Check gas usage with `forge snapshot`

## 📄 License

This project is licensed under the MIT License.
