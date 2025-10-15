# defi-knowledge.py
from hyperon import MeTTa, E, S, ValueAtom

def initialize_defi_knowledge_graph(metta: MeTTa):
    """
    Initialize the MeTTa knowledge graph with DeFi protocol, operation, constraint, and risk data.
    
    This knowledge graph supports evaluation across multiple metrics:
    - Capability: Protocol → Operations mapping
    - Functional Correctness: Operations → Required Parameters & Expected Outputs
    - Domain Correctness: Operations → Financial Constraints (slippage, leverage, liquidity)
    - Security & Safety: Operations → Risks & Vulnerabilities
    """
    
    # ========================================
    # CAPABILITY METRIC: Protocol → Operations
    # ========================================
    # These atoms represent what operations each protocol supports
    # Used to verify if an agent correctly claims protocol capabilities
    
    # Uniswap V3 capabilities
    metta.space().add_atom(E(S("protocol"), S("uniswap-v3"), S("swap")))
    metta.space().add_atom(E(S("protocol"), S("uniswap-v3"), S("add-liquidity")))
    metta.space().add_atom(E(S("protocol"), S("uniswap-v3"), S("remove-liquidity")))
    metta.space().add_atom(E(S("protocol"), S("uniswap-v3"), S("collect-fees")))
    
    # Aave V3 capabilities
    metta.space().add_atom(E(S("protocol"), S("aave-v3"), S("supply")))
    metta.space().add_atom(E(S("protocol"), S("aave-v3"), S("withdraw")))
    metta.space().add_atom(E(S("protocol"), S("aave-v3"), S("borrow")))
    metta.space().add_atom(E(S("protocol"), S("aave-v3"), S("repay")))
    metta.space().add_atom(E(S("protocol"), S("aave-v3"), S("liquidate")))
    
    # Compound V3 capabilities
    metta.space().add_atom(E(S("protocol"), S("compound-v3"), S("supply")))
    metta.space().add_atom(E(S("protocol"), S("compound-v3"), S("withdraw")))
    metta.space().add_atom(E(S("protocol"), S("compound-v3"), S("borrow")))
    metta.space().add_atom(E(S("protocol"), S("compound-v3"), S("repay")))
    
    # Curve capabilities
    metta.space().add_atom(E(S("protocol"), S("curve"), S("swap")))
    metta.space().add_atom(E(S("protocol"), S("curve"), S("add-liquidity")))
    metta.space().add_atom(E(S("protocol"), S("curve"), S("remove-liquidity")))
    
    # Lido capabilities
    metta.space().add_atom(E(S("protocol"), S("lido"), S("stake")))
    metta.space().add_atom(E(S("protocol"), S("lido"), S("unstake")))
    
    # ========================================
    # FUNCTIONAL CORRECTNESS: Operations → Required Parameters
    # ========================================
    # These atoms define what parameters each operation must have
    # Used to verify if agent correctly handles all required params
    
    metta.space().add_atom(E(S("requires"), S("swap"), ValueAtom("tokenIn,tokenOut,amountIn,slippage,deadline")))
    metta.space().add_atom(E(S("requires"), S("add-liquidity"), ValueAtom("token0,token1,amount0,amount1,minAmount0,minAmount1,deadline")))
    metta.space().add_atom(E(S("requires"), S("remove-liquidity"), ValueAtom("token0,token1,liquidity,minAmount0,minAmount1,deadline")))
    metta.space().add_atom(E(S("requires"), S("supply"), ValueAtom("asset,amount,onBehalfOf")))
    metta.space().add_atom(E(S("requires"), S("withdraw"), ValueAtom("asset,amount,to")))
    metta.space().add_atom(E(S("requires"), S("borrow"), ValueAtom("asset,amount,interestRateMode,onBehalfOf")))
    metta.space().add_atom(E(S("requires"), S("repay"), ValueAtom("asset,amount,interestRateMode,onBehalfOf")))
    metta.space().add_atom(E(S("requires"), S("stake"), ValueAtom("amount")))
    metta.space().add_atom(E(S("requires"), S("liquidate"), ValueAtom("collateralAsset,debtAsset,user,debtToCover")))
    
    # ========================================
    # FUNCTIONAL CORRECTNESS: Operations → Expected Outputs
    # ========================================
    # These atoms define what outputs should be produced
    
    metta.space().add_atom(E(S("output"), S("swap"), ValueAtom("amountOut,gasUsed,priceImpact")))
    metta.space().add_atom(E(S("output"), S("supply"), ValueAtom("aTokenBalance,interestRate")))
    metta.space().add_atom(E(S("output"), S("borrow"), ValueAtom("debtBalance,healthFactor,interestRate")))
    metta.space().add_atom(E(S("output"), S("stake"), ValueAtom("stETHAmount,sharesMinted")))
    
    # ========================================
    # DOMAIN CORRECTNESS: Operations → Financial Constraints
    # ========================================
    # These atoms encode DeFi-specific rules and best practices
    
    # Slippage constraints (max safe slippage %)
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("slippage_max:5.0")))
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("slippage_warn:1.0")))
    metta.space().add_atom(E(S("constraint"), S("add-liquidity"), ValueAtom("slippage_max:2.0")))
    
    # Price impact constraints (max % of pool)
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("price_impact_max:10.0")))
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("price_impact_warn:3.0")))
    
    # Leverage ratio constraints (Loan-to-Value limits)
    metta.space().add_atom(E(S("constraint"), S("borrow"), ValueAtom("ltv_max_stable:90.0")))
    metta.space().add_atom(E(S("constraint"), S("borrow"), ValueAtom("ltv_max_volatile:80.0")))
    metta.space().add_atom(E(S("constraint"), S("borrow"), ValueAtom("ltv_safe:70.0")))
    metta.space().add_atom(E(S("constraint"), S("borrow"), ValueAtom("health_factor_min:1.5")))
    
    # Liquidity constraints
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("min_liquidity_usd:10000")))
    metta.space().add_atom(E(S("constraint"), S("add-liquidity"), ValueAtom("min_liquidity_usd:1000")))
    
    # Gas constraints
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("max_gas_premium:20.0")))
    metta.space().add_atom(E(S("constraint"), S("supply"), ValueAtom("max_gas_premium:20.0")))
    
    # Deadline constraints (max minutes from now)
    metta.space().add_atom(E(S("constraint"), S("swap"), ValueAtom("deadline_max_minutes:20")))
    metta.space().add_atom(E(S("constraint"), S("add-liquidity"), ValueAtom("deadline_max_minutes:20")))
    metta.space().add_atom(E(S("constraint"), S("remove-liquidity"), ValueAtom("deadline_max_minutes:20")))
    
    # ========================================
    # SECURITY & SAFETY: Operations → Risks
    # ========================================
    # These atoms identify security risks associated with operations
    
    # MEV (Maximal Extractable Value) risks
    metta.space().add_atom(E(S("risk"), S("swap"), ValueAtom("mev:frontrun,sandwich")))
    metta.space().add_atom(E(S("risk"), S("add-liquidity"), ValueAtom("mev:frontrun")))
    
    # Liquidation risks
    metta.space().add_atom(E(S("risk"), S("borrow"), ValueAtom("liquidation:price_volatility")))
    metta.space().add_atom(E(S("risk"), S("borrow"), ValueAtom("liquidation:low_health_factor")))
    
    # Smart contract risks
    metta.space().add_atom(E(S("risk"), S("supply"), ValueAtom("contract:upgrade_risk,pause_risk")))
    metta.space().add_atom(E(S("risk"), S("stake"), ValueAtom("contract:slashing_risk")))
    
    # Approval risks
    metta.space().add_atom(E(S("risk"), S("swap"), ValueAtom("approval:infinite_approval")))
    metta.space().add_atom(E(S("risk"), S("supply"), ValueAtom("approval:infinite_approval")))
    
    # Impermanent loss risks
    metta.space().add_atom(E(S("risk"), S("add-liquidity"), ValueAtom("impermanent_loss:high_volatility")))
    
    # Reentrancy risks
    metta.space().add_atom(E(S("risk"), S("remove-liquidity"), ValueAtom("reentrancy:callback_attack")))
    
    # ========================================
    # SECURITY: Operations → Best Practices
    # ========================================
    # These atoms encode security best practices
    
    metta.space().add_atom(E(S("best-practice"), S("swap"), ValueAtom("use_deadline_parameter")))
    metta.space().add_atom(E(S("best-practice"), S("swap"), ValueAtom("validate_slippage")))
    metta.space().add_atom(E(S("best-practice"), S("swap"), ValueAtom("check_price_impact")))
    metta.space().add_atom(E(S("best-practice"), S("borrow"), ValueAtom("monitor_health_factor")))
    metta.space().add_atom(E(S("best-practice"), S("borrow"), ValueAtom("maintain_buffer_above_liquidation")))
    metta.space().add_atom(E(S("best-practice"), S("supply"), ValueAtom("use_exact_approvals")))
    metta.space().add_atom(E(S("best-practice"), S("liquidate"), ValueAtom("verify_health_factor_below_threshold")))
    
    # ========================================
    # DOMAIN KNOWLEDGE: Asset Classifications
    # ========================================
    # Used for applying appropriate constraints based on asset type
    
    # Stable coins (low volatility)
    metta.space().add_atom(E(S("asset-type"), S("USDC"), S("stable")))
    metta.space().add_atom(E(S("asset-type"), S("USDT"), S("stable")))
    metta.space().add_atom(E(S("asset-type"), S("DAI"), S("stable")))
    metta.space().add_atom(E(S("asset-type"), S("FRAX"), S("stable")))
    
    # Volatile assets
    metta.space().add_atom(E(S("asset-type"), S("ETH"), S("volatile")))
    metta.space().add_atom(E(S("asset-type"), S("WETH"), S("volatile")))
    metta.space().add_atom(E(S("asset-type"), S("WBTC"), S("volatile")))
    metta.space().add_atom(E(S("asset-type"), S("LINK"), S("volatile")))
    
    # Liquid staking tokens
    metta.space().add_atom(E(S("asset-type"), S("stETH"), S("lst")))
    metta.space().add_atom(E(S("asset-type"), S("rETH"), S("lst")))
    
    # ========================================
    # DOMAIN KNOWLEDGE: Protocol TVL Ranges
    # ========================================
    # Used for operational/reliability metrics
    
    metta.space().add_atom(E(S("tvl"), S("uniswap-v3"), ValueAtom("4000000000")))  # $4B
    metta.space().add_atom(E(S("tvl"), S("aave-v3"), ValueAtom("6000000000")))     # $6B
    metta.space().add_atom(E(S("tvl"), S("curve"), ValueAtom("3000000000")))       # $3B
    metta.space().add_atom(E(S("tvl"), S("compound-v3"), ValueAtom("2000000000"))) # $2B
    metta.space().add_atom(E(S("tvl"), S("lido"), ValueAtom("15000000000")))       # $15B
    
    # ========================================
    # FAQ: Common DeFi Questions
    # ========================================
    
    metta.space().add_atom(E(S("faq"), S("What is slippage?"), ValueAtom("Slippage is the difference between expected and actual execution price due to market movements or liquidity depth.")))
    metta.space().add_atom(E(S("faq"), S("What is impermanent loss?"), ValueAtom("Impermanent loss occurs when providing liquidity and the price ratio of deposited tokens changes, resulting in less value than holding.")))
    metta.space().add_atom(E(S("faq"), S("What is MEV?"), ValueAtom("MEV (Maximal Extractable Value) is profit extracted by reordering, including, or censoring transactions, often through frontrunning or sandwich attacks.")))
    metta.space().add_atom(E(S("faq"), S("What is health factor?"), ValueAtom("Health factor indicates the safety of your borrowed position. Below 1.0 means you can be liquidated. Keep it above 1.5 for safety.")))
    metta.space().add_atom(E(S("faq"), S("What is price impact?"), ValueAtom("Price impact is how much your trade moves the market price, typically higher for larger trades or in pools with less liquidity.")))

