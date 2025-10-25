"""Comprehensive category taxonomy for multi-category agent detection"""

from typing import Dict, List, Set, Optional
from dataclasses import dataclass


@dataclass
class CategoryDefinition:
    """Definition of a category with its keywords and metadata"""
    name: str
    keywords: Set[str]
    description: str
    weight: float = 1.0  # Weight for confidence calculation
    parent: Optional[str] = None  # For subcategories


# Primary Categories
PRIMARY_CATEGORIES = {
    "crypto": CategoryDefinition(
        name="Crypto",
        keywords={
            "crypto", "cryptocurrency", "cryptocurrencies", "blockchain", "web3",
            "bitcoin", "btc", "ethereum", "eth", "defi", "nft", "nfts", "token", "tokens",
            "wallet", "wallets", "mining", "hash", "consensus", "smart contract",
            "dapp", "dapps", "exchange", "trading", "decentralized", "altcoin",
            "fork", "segwit", "lightning", "gas", "mempool", "private key",
            "public key", "address", "seed phrase", "metamask", "ledger", "trezor",
            "yield farming", "liquidity", "dao", "governance", "whitepaper", "ico",
            # Additional DeFi-specific terms
            "defi", "decentralized finance", "liquidity pool", "liquidity pools", "amm",
            "automated market maker", "dex", "decentralized exchange", "swap", "swaps",
            "protocol", "protocols", "aave", "compound", "uniswap", "curve", "balancer",
            "yearn", "synthetix", "makerdao", "maker", "dai", "usdc", "usdt", "weth",
            "lending", "borrowing", "collateral", "flash loan", "flash loans",
            "yield", "apy", "apr", "staking", "stake", "staked", "rewards",
            "portfolio", "portfolio management", "arbitrage", "arbitrageur",
            "cross-chain", "bridge", "bridges", "layer 2", "l2", "polygon", "arbitrum",
            "optimism", "base", "cosmos", "fetch", "fetch.ai", "agentverse",
            "autonomous", "autonomous agent", "ai", "machine learning", "ml",
            "strategy", "strategies", "optimization", "optimize", "risk management",
            "volatility", "slippage", "impermanent loss", "rebalancing", "rebalance"
        },
        description="Cryptocurrency and blockchain-related agents",
        weight=1.2  # Higher weight for crypto as it's our primary focus
    ),
    "travel": CategoryDefinition(
        name="Travel",
        keywords={
            "travel", "trip", "booking", "flight", "flights", "airline", "airlines",
            "hotel", "hotels", "accommodation", "itinerary", "destination", "destinations",
            "tourism", "tourist", "vacation", "holiday", "resort", "cruise", "cruises",
            "passport", "visa", "airport", "airports", "luggage", "suitcase",
            "travel guide", "traveler", "backpacking", "sightseeing", "adventure"
        },
        description="Travel and tourism-related agents",
        weight=1.0
    ),
    "cooking": CategoryDefinition(
        name="Cooking",
        keywords={
            "cooking", "cook", "recipe", "recipes", "ingredient", "ingredients",
            "meal", "meals", "cuisine", "chef", "kitchen", "food", "cookbook",
            "baking", "bake", "grilling", "grill", "frying", "fry", "boiling",
            "steaming", "roasting", "seasoning", "spice", "spices", "herbs",
            "nutrition", "diet", "healthy", "vegetarian", "vegan", "gluten-free"
        },
        description="Cooking and food-related agents",
        weight=1.0
    ),
    "finance": CategoryDefinition(
        name="Finance",
        keywords={
            "finance", "financial", "payment", "payments", "invoice", "invoices",
            "accounting", "banking", "bank", "budget", "budgeting", "investment",
            "investing", "portfolio", "trading", "stocks", "bonds", "mutual fund",
            "retirement", "savings", "loan", "loans", "credit", "debt", "tax",
            "taxes", "audit", "bookkeeping", "expense", "expenses", "revenue"
        },
        description="Finance and accounting-related agents",
        weight=1.0
    ),
    "healthcare": CategoryDefinition(
        name="Healthcare",
        keywords={
            "health", "healthcare", "medical", "medicine", "doctor", "nurse",
            "patient", "patients", "diagnosis", "treatment", "therapy", "therapist",
            "wellness", "fitness", "exercise", "nutrition", "diet", "mental health",
            "psychology", "psychiatrist", "counseling", "pharmacy", "medication",
            "surgery", "hospital", "clinic", "appointment", "appointments", "symptoms"
        },
        description="Healthcare and medical-related agents",
        weight=1.0
    ),
    "education": CategoryDefinition(
        name="Education",
        keywords={
            "education", "educational", "learning", "learn", "course", "courses",
            "tutorial", "tutorials", "study", "studying", "teaching", "teacher",
            "training", "training", "school", "university", "college", "academy",
            "lesson", "lessons", "curriculum", "syllabus", "homework", "assignment",
            "exam", "exams", "test", "tests", "quiz", "quizzes", "student", "students"
        },
        description="Education and learning-related agents",
        weight=1.0
    ),
    "entertainment": CategoryDefinition(
        name="Entertainment",
        keywords={
            "entertainment", "entertaining", "game", "games", "gaming", "gamer",
            "movie", "movies", "film", "films", "music", "musical", "song", "songs",
            "streaming", "stream", "media", "content", "video", "videos", "podcast",
            "podcasts", "radio", "television", "tv", "theater", "theatre", "concert",
            "concerts", "show", "shows", "performance", "performances", "actor"
        },
        description="Entertainment and media-related agents",
        weight=1.0
    ),
    "productivity": CategoryDefinition(
        name="Productivity",
        keywords={
            "productivity", "productive", "task", "tasks", "project", "projects",
            "workflow", "workflows", "automation", "automate", "schedule", "scheduling",
            "organize", "organization", "management", "manager", "planning", "planner",
            "calendar", "agenda", "meeting", "meetings", "deadline", "deadlines",
            "efficiency", "efficient", "optimization", "optimize", "workflow", "process"
        },
        description="Productivity and workflow-related agents",
        weight=1.0
    ),
    "social": CategoryDefinition(
        name="Social",
        keywords={
            "social", "socializing", "chat", "chats", "messaging", "message",
            "community", "communities", "network", "networking", "connection",
            "connections", "forum", "forums", "discussion", "discussions", "group",
            "groups", "team", "teams", "collaboration", "collaborate", "share",
            "sharing", "post", "posts", "comment", "comments", "like", "likes"
        },
        description="Social and community-related agents",
        weight=1.0
    )
}

# Crypto Subcategories (Basic + Extended)
CRYPTO_SUBCATEGORIES = {
    "defi": CategoryDefinition(
        name="DeFi",
        keywords={
            "defi", "decentralized finance", "liquidity", "yield", "swap", "swaps",
            "amm", "automated market maker", "lending", "borrowing", "borrow",
            "lend", "protocol", "protocols", "compound", "aave", "uniswap",
            "sushiswap", "curve", "balancer", "maker", "yearn", "harvest",
            # Additional DeFi terms from the README
            "liquidity pool", "liquidity pools", "yield farming", "yield farm",
            "apy", "apr", "annual percentage yield", "annual percentage rate",
            "portfolio management", "portfolio manager", "autonomous execution",
            "risk management", "volatility", "slippage", "impermanent loss",
            "rebalancing", "rebalance", "arbitrage", "cross-chain", "bridge",
            "flash loan", "flash loans", "collateral", "collateralized",
            "liquidation", "health factor", "ltv", "loan-to-value",
            "overcollateralized", "under-collateralized", "credit", "debt",
            "repay", "repayment", "refinance", "refinancing", "credit score",
            "risk assessment", "strategy", "strategies", "optimization", "optimize",
            "autonomous agent", "ai", "machine learning", "ml", "reinforcement learning",
            "multi-chain", "ethereum", "polygon", "arbitrum", "base", "cosmos",
            "fetch", "fetch.ai", "agentverse", "agent", "agents", "autonomous"
        },
        description="Decentralized Finance protocols and applications",
        weight=1.2,  # Higher weight for DeFi
        parent="crypto"
    ),
    "nft": CategoryDefinition(
        name="NFT",
        keywords={
            "nft", "nfts", "non-fungible", "collectible", "collectibles", "artwork",
            "art", "metadata", "opensea", "marketplace", "mint", "minting", "minted",
            "rarible", "foundation", "superrare", "crypto punks", "bored ape",
            "digital art", "digital collectible", "token standard", "erc-721", "erc-1155"
        },
        description="Non-Fungible Tokens and digital collectibles",
        weight=1.0,
        parent="crypto"
    ),
    "trading": CategoryDefinition(
        name="Trading",
        keywords={
            "trading", "trader", "traders", "exchange", "exchanges", "order book",
            "dex", "cex", "trading bot", "arbitrage", "arbitrageur", "market maker",
            "liquidity provider", "trading pair", "trading pairs", "spot trading",
            "futures", "options", "derivatives", "margin", "leverage", "stop loss",
            "take profit", "technical analysis", "chart", "charts", "candlestick"
        },
        description="Cryptocurrency trading and exchange platforms",
        weight=1.0,
        parent="crypto"
    ),
    "wallet": CategoryDefinition(
        name="Wallet",
        keywords={
            "wallet", "wallets", "custody", "custodial", "non-custodial", "private key",
            "private keys", "seed phrase", "seed phrases", "mnemonic", "hardware wallet",
            "metamask", "trust wallet", "coinbase wallet", "ledger", "trezor",
            "cold storage", "hot wallet", "cold wallet", "key management", "signature",
            "signing", "transaction", "transactions", "address", "addresses"
        },
        description="Cryptocurrency wallet and key management",
        weight=1.0,
        parent="crypto"
    ),
    "exchange": CategoryDefinition(
        name="Exchange",
        keywords={
            "exchange", "exchanges", "trading pair", "trading pairs", "liquidity pool",
            "liquidity pools", "order matching", "order book", "kyc", "aml",
            "compliance", "regulatory", "fiat", "fiat on-ramp", "fiat off-ramp",
            "deposit", "deposits", "withdrawal", "withdrawals", "trading fee",
            "trading fees", "maker", "taker", "spread", "spreads", "volume"
        },
        description="Cryptocurrency exchange platforms",
        weight=1.0,
        parent="crypto"
    ),
    "dao": CategoryDefinition(
        name="DAO",
        keywords={
            "dao", "daos", "decentralized autonomous organization", "governance",
            "voting", "vote", "votes", "proposal", "proposals", "treasury", "treasuries",
            "multisig", "multi-signature", "consensus", "quorum", "delegation",
            "delegate", "delegates", "token holder", "token holders", "community",
            "governance token", "governance tokens", "snapshot", "discord", "forum"
        },
        description="Decentralized Autonomous Organizations",
        weight=1.0,
        parent="crypto"
    ),
    "gaming": CategoryDefinition(
        name="Gaming",
        keywords={
            "gaming", "game", "games", "play-to-earn", "p2e", "gamefi", "in-game",
            "metaverse", "virtual world", "virtual worlds", "nft game", "nft games",
            "crypto game", "crypto games", "blockchain game", "blockchain games",
            "axie infinity", "sandbox", "decentraland", "cryptokitties", "gaming nft",
            "gaming nfts", "virtual land", "virtual lands", "avatar", "avatars"
        },
        description="Blockchain gaming and play-to-earn",
        weight=1.0,
        parent="crypto"
    ),
    "lending": CategoryDefinition(
        name="Lending",
        keywords={
            "lending", "lend", "borrowing", "borrow", "collateral", "collateralized",
            "interest rate", "interest rates", "flash loan", "flash loans", "liquidation",
            "liquidated", "liquidation threshold", "health factor", "ltv", "loan-to-value",
            "overcollateralized", "under-collateralized", "credit", "debt", "repay",
            "repayment", "refinance", "refinancing", "credit score", "risk assessment"
        },
        description="Cryptocurrency lending and borrowing",
        weight=1.0,
        parent="crypto"
    ),
    "yield_farming": CategoryDefinition(
        name="Yield Farming",
        keywords={
            "yield farming", "yield farm", "yield farms", "farming", "farm", "farms",
            "apy", "apr", "annual percentage yield", "annual percentage rate", "stake",
            "staking", "staked", "reward", "rewards", "harvest", "harvesting",
            "harvested", "compound", "compounding", "auto-compound", "auto-compounding",
            "liquidity mining", "mining", "miner", "miners", "pool", "pools"
        },
        description="Yield farming and staking protocols",
        weight=1.0,
        parent="crypto"
    ),
    "staking": CategoryDefinition(
        name="Staking",
        keywords={
            "staking", "stake", "staked", "validator", "validators", "consensus",
            "consensus mechanism", "proof of stake", "pos", "delegation", "delegate",
            "delegates", "delegated", "unbonding", "unbond", "slashing", "slashed",
            "rewards", "reward", "commission", "commission rate", "node", "nodes",
            "validator node", "validator nodes", "beacon chain", "shard", "shards"
        },
        description="Cryptocurrency staking and validation",
        weight=1.0,
        parent="crypto"
    ),
    "bridge": CategoryDefinition(
        name="Bridge",
        keywords={
            "bridge", "bridges", "cross-chain", "multichain", "wrapped token",
            "wrapped tokens", "bridge protocol", "bridge protocols", "layer 2",
            "l2", "sidechain", "sidechains", "rollup", "rollups", "optimistic",
            "zk-rollup", "zk-rollups", "polygon", "arbitrum", "optimism", "avalanche",
            "fantom", "bsc", "binance smart chain", "ethereum bridge", "bitcoin bridge"
        },
        description="Cross-chain bridges and layer 2 solutions",
        weight=1.0,
        parent="crypto"
    ),
    "analytics": CategoryDefinition(
        name="Analytics",
        keywords={
            "analytics", "analysis", "on-chain", "onchain", "metrics", "metric",
            "dashboard", "dashboards", "blockchain explorer", "explorer", "explorers",
            "transaction", "transactions", "address", "addresses", "balance",
            "balances", "volume", "volumes", "price", "prices", "market cap",
            "market capitalization", "circulating supply", "total supply", "max supply"
        },
        description="Blockchain analytics and on-chain data",
        weight=1.0,
        parent="crypto"
    ),
    "privacy": CategoryDefinition(
        name="Privacy",
        keywords={
            "privacy", "private", "zero-knowledge", "zk", "zk-proof", "zk-proofs",
            "mixer", "mixers", "anonymous", "anonymity", "private transaction",
            "private transactions", "tornado", "tornado cash", "monero", "zcash",
            "privacy coin", "privacy coins", "confidential", "confidentiality",
            "obfuscation", "obfuscate", "stealth", "stealth address", "ring signature"
        },
        description="Privacy-focused cryptocurrency solutions",
        weight=1.0,
        parent="crypto"
    ),
    "launchpad": CategoryDefinition(
        name="Launchpad",
        keywords={
            "launchpad", "launchpads", "ido", "initial dex offering", "token sale",
            "token sales", "fundraising", "fundraise", "vesting", "vested", "vest",
            "token launch", "token launches", "new token", "new tokens", "presale",
            "presales", "public sale", "public sales", "private sale", "private sales",
            "seed round", "seed rounds", "series a", "series b", "vc", "venture capital"
        },
        description="Token launch and fundraising platforms",
        weight=1.0,
        parent="crypto"
    )
}

# Confidence thresholds - High selectivity with generous confidence calculation
PRIMARY_CATEGORY_THRESHOLD = 0.7  # High threshold for primary classification (was 0.6)
SECONDARY_CATEGORY_THRESHOLD = 0.5  # High threshold for secondary categories (was 0.4)
UNKNOWN_CATEGORY_THRESHOLD = 0.4  # Mark as unknown if low confidence (was 0.3)

# Subcategory detection threshold - high selectivity for subcategories
SUBCATEGORY_DETECTION_THRESHOLD = 0.3  # High threshold to detect subcategories (was 0.25)

# Multi-category detection threshold
MULTI_CATEGORY_THRESHOLD = 0.5  # High threshold for multi-category detection (was 0.4)


def get_all_categories() -> Dict[str, CategoryDefinition]:
    """Get all primary categories"""
    return PRIMARY_CATEGORIES.copy()


def get_crypto_subcategories() -> Dict[str, CategoryDefinition]:
    """Get all crypto subcategories"""
    return CRYPTO_SUBCATEGORIES.copy()


def get_category_keywords(category_name: str) -> Set[str]:
    """Get keywords for a specific category"""
    if category_name in PRIMARY_CATEGORIES:
        return PRIMARY_CATEGORIES[category_name].keywords
    elif category_name in CRYPTO_SUBCATEGORIES:
        return CRYPTO_SUBCATEGORIES[category_name].keywords
    else:
        return set()


def get_categories_for_text(text: str) -> Dict[str, float]:
    """
    Get category confidence scores for given text
    
    Args:
        text: Text to analyze (lowercase)
        
    Returns:
        Dictionary mapping category names to confidence scores
    """
    text_lower = text.lower()
    scores = {}
    
    # Check primary categories
    for category_name, category_def in PRIMARY_CATEGORIES.items():
        matches = sum(1 for keyword in category_def.keywords if keyword in text_lower)
        if matches > 0:
            # More generous confidence calculation:
            # 1. Base confidence from match ratio (with square root scaling)
            # 2. Logarithmic boost for multiple matches
            # 3. Minimum confidence floor for any matches
            # 4. Apply category weight
            
            # Use square root to reduce penalty for large keyword sets
            match_ratio = matches / len(category_def.keywords)
            sqrt_ratio = match_ratio ** 0.5  # Square root scaling
            
            # Logarithmic boost for multiple matches (more generous)
            import math
            log_boost = min(0.4, math.log(1 + matches) * 0.1)  # Up to 0.4 boost
            
            # Base confidence with square root scaling
            base_confidence = sqrt_ratio * category_def.weight
            
            # Minimum confidence floor for any matches
            min_confidence = 0.15  # 15% minimum for any matches
            
            # Combine all factors
            confidence = min(1.0, max(min_confidence, base_confidence + log_boost))
            scores[category_name] = confidence
    
    # Check crypto subcategories if crypto is detected (use more permissive threshold)
    if "crypto" in scores and scores["crypto"] > SUBCATEGORY_DETECTION_THRESHOLD:
        for subcategory_name, subcategory_def in CRYPTO_SUBCATEGORIES.items():
            matches = sum(1 for keyword in subcategory_def.keywords if keyword in text_lower)
            if matches > 0:
                # Same generous calculation for subcategories
                match_ratio = matches / len(subcategory_def.keywords)
                sqrt_ratio = match_ratio ** 0.5  # Square root scaling
                
                # Logarithmic boost for multiple matches (more generous)
                import math
                log_boost = min(0.4, math.log(1 + matches) * 0.1)  # Up to 0.4 boost
                
                # Base confidence with square root scaling
                base_confidence = sqrt_ratio * subcategory_def.weight
                
                # Minimum confidence floor for any matches (lower for subcategories)
                min_confidence = 0.1  # 10% minimum for subcategory matches
                
                # Combine all factors
                confidence = min(1.0, max(min_confidence, base_confidence + log_boost))
                scores[f"crypto_{subcategory_name}"] = confidence
    
    return scores


def get_primary_category(text: str) -> Optional[str]:
    """Get the primary category for given text"""
    scores = get_categories_for_text(text)
    
    # Filter to only primary categories
    primary_scores = {k: v for k, v in scores.items() if k in PRIMARY_CATEGORIES}
    
    if not primary_scores:
        return None
    
    # Return category with highest confidence above threshold
    best_category = max(primary_scores.items(), key=lambda x: x[1])
    if best_category[1] >= PRIMARY_CATEGORY_THRESHOLD:
        return best_category[0]
    
    return None


def get_crypto_subcategories_for_text(text: str) -> Dict[str, float]:
    """Get crypto subcategory confidence scores for given text"""
    scores = get_categories_for_text(text)
    
    # Filter to only crypto subcategories
    crypto_subcategory_scores = {k: v for k, v in scores.items() if k.startswith("crypto_")}
    
    return crypto_subcategory_scores


def is_unknown_category(text: str) -> bool:
    """Check if text doesn't match any category above threshold"""
    scores = get_categories_for_text(text)
    primary_scores = {k: v for k, v in scores.items() if k in PRIMARY_CATEGORIES}
    
    if not primary_scores:
        return True
    
    max_confidence = max(primary_scores.values())
    return max_confidence < UNKNOWN_CATEGORY_THRESHOLD
