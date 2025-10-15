# defi-knowledge.py
from hyperon import MeTTa, E, S, ValueAtom

(WIP)
def initialize_defi_knowledge_graph(metta: MeTTa):
    """
    Initialize minimal MeTTa knowledge graph for DeFi agent evaluation.
    
    Supports 3 evaluation metrics:
    1. Correctness (50%): Base chain facts, addresses, slippage formula
    2. Capabilities (35%): Uniswap V3 swap operation
    3. Domain Knowledge (15%): Price impact constraints
    """
    
    # ========================================
    # CORRECTNESS METRIC: Blockchain Facts
    # ========================================
    # Test: Exact match questions about Base chain
    
    # Base chain information
    metta.space().add_atom(E(S("chain"), S("base"), ValueAtom("chainId:8453")))
    
    # Canonical USDC address on Base
    metta.space().add_atom(E(S("token-address"), S("USDC-base"), ValueAtom("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913")))
    
    # Uniswap V3 router address on Base
    metta.space().add_atom(E(S("protocol-address"), S("uniswap-v3-base"), ValueAtom("0x2626664c2603336E57B271c5C0b26F421741e481")))
    
    # Slippage calculation formula (simple deterministic equation)
    # Formula: slippage_percent = ((expected_price - actual_price) / expected_price) * 100
    metta.space().add_atom(E(S("formula"), S("slippage"), ValueAtom("slippage_percent = ((expected_price - actual_price) / expected_price) * 100")))
    
    # ========================================
    # CAPABILITIES METRIC: Swap Operation
    # ========================================
    # Test: Execute "buy 100 USDC → ETH at max 1% slippage on uniswap v3"
    
    # Uniswap V3 supports swap operation
    metta.space().add_atom(E(S("protocol"), S("uniswap-v3"), S("swap")))
    
    # Required parameters for swap operation
    metta.space().add_atom(E(S("requires"), S("swap"), ValueAtom("tokenIn,tokenOut,amountIn,slippage")))
    
    # Expected outputs from swap
    metta.space().add_atom(E(S("output"), S("swap"), ValueAtom("amountOut,transactionHash")))
    
    # ========================================
    # DOMAIN KNOWLEDGE: Price Impact
    # ========================================
    # Test: Swaps causing >10% price impact should trigger warnings
    
    # Price impact constraint (warn if >10%)
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("price_impact_max:10.0")))
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("price_impact_warn:10.0")))
    
    # Liquidity depth awareness
    metta.space().add_atom(E(S("best-practice"), S("swap"), ValueAtom("check_price_impact")))
    metta.space().add_atom(E(S("best-practice"), S("swap"), ValueAtom("warn_on_high_impact")))
    
    # ========================================
    # SUPPORTING KNOWLEDGE: Asset Types
    # ========================================
    # For context on token types
    
    metta.space().add_atom(E(S("asset-type"), S("USDC"), S("stable")))
    metta.space().add_atom(E(S("asset-type"), S("ETH"), S("volatile")))

