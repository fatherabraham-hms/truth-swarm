#!/usr/bin/env python3
"""
Comprehensive test suite for multi-category agent detection and feature extraction
"""

import asyncio
import json
from datetime import datetime, timezone
from models.data_models import AgentProfileData
from detection.metta_categorizer import MeTTaCategorizer
from detection.simple_detector import SimpleDetector
from utils.category_taxonomy import PRIMARY_CATEGORIES, CRYPTO_SUBCATEGORIES


def create_test_agent_profile(category: str, subcategory: str = None, content: str = "") -> AgentProfileData:
    """Create a test agent profile for a specific category"""
    
    # Sample content for different categories
    sample_content = {
        "crypto": {
            "defi": """
# DeFi Trading Bot

A sophisticated DeFi trading bot that provides automated yield farming, liquidity provision, and arbitrage opportunities across multiple protocols.

## Features
- Automated yield farming on Uniswap, SushiSwap, and Curve
- Cross-chain arbitrage between Ethereum, Polygon, and Arbitrum
- Real-time price monitoring and MEV protection
- Integration with Aave, Compound, and Maker protocols
- Smart contract interaction using Web3.py and Solidity

## Supported Chains
- Ethereum Mainnet
- Polygon
- Arbitrum
- Avalanche

## Tech Stack
- Python 3.9
- Web3.py
- Solidity
- Hardhat
- Infura API
- The Graph Protocol

## Use Cases
- Yield farming optimization
- Liquidity provision strategies
- Cross-chain arbitrage
- Portfolio rebalancing
""",
            "nft": """
# NFT Marketplace Agent

An AI-powered NFT marketplace agent that helps users discover, trade, and manage their digital collectibles.

## Features
- NFT discovery and recommendation engine
- Automated bidding and trading strategies
- Metadata analysis and rarity scoring
- Integration with OpenSea, Rarible, and Foundation
- Real-time floor price monitoring

## Supported Platforms
- OpenSea
- Rarible
- Foundation
- SuperRare
- LooksRare

## Tech Stack
- JavaScript/TypeScript
- React
- Node.js
- IPFS
- Ethereum Web3

## Use Cases
- NFT trading and arbitrage
- Collection management
- Rarity analysis
- Market trend analysis
""",
            "trading": """
# Crypto Trading Bot

Professional-grade cryptocurrency trading bot with advanced technical analysis and risk management.

## Features
- Spot and futures trading
- Technical analysis indicators
- Risk management and stop-loss
- Portfolio optimization
- Real-time market data

## Supported Exchanges
- Binance
- Coinbase Pro
- Kraken
- KuCoin

## Tech Stack
- Python
- CCXT library
- Pandas
- NumPy
- Matplotlib

## Use Cases
- Automated trading strategies
- Portfolio management
- Market making
- Arbitrage opportunities
"""
        },
        "travel": """
# Travel Planning Agent

An intelligent travel planning agent that helps users discover destinations, book flights, and create personalized itineraries.

## Features
- Destination recommendations
- Flight and hotel booking
- Itinerary optimization
- Budget planning
- Real-time travel updates

## Integrations
- Expedia API
- Booking.com
- Google Maps
- Weather services

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Redis
- Docker

## Use Cases
- Trip planning
- Travel booking
- Itinerary management
- Travel recommendations
""",
        "cooking": """
# Recipe Recommendation Agent

A smart cooking assistant that suggests recipes, manages ingredients, and provides cooking guidance.

## Features
- Recipe recommendations based on preferences
- Ingredient management and shopping lists
- Nutritional analysis
- Cooking timers and instructions
- Dietary restriction filtering

## Integrations
- Spoonacular API
- Nutrition databases
- Shopping list apps

## Tech Stack
- Python
- Flask
- SQLite
- BeautifulSoup
- Pandas

## Use Cases
- Recipe discovery
- Meal planning
- Nutrition tracking
- Cooking guidance
""",
        "finance": """
# Personal Finance Manager

An AI-powered personal finance management agent that helps users track expenses, create budgets, and optimize investments.

## Features
- Expense tracking and categorization
- Budget creation and monitoring
- Investment portfolio analysis
- Bill reminders and payments
- Financial goal tracking

## Integrations
- Bank APIs
- Investment platforms
- Credit card providers
- Tax software

## Tech Stack
- Python
- Django
- PostgreSQL
- Celery
- Redis

## Use Cases
- Budget management
- Expense tracking
- Investment optimization
- Financial planning
"""
    }
    
    # Get content based on category and subcategory
    if category == "crypto" and subcategory:
        content = sample_content["crypto"].get(subcategory, sample_content["crypto"]["defi"])
    else:
        content = sample_content.get(category, content or f"# {category.title()} Agent\n\nA {category} agent for testing purposes.")
    
    # Generate capabilities based on category
    capabilities = {
        "crypto": ["blockchain", "defi", "trading", "web3"],
        "travel": ["booking", "itinerary", "destination", "tourism"],
        "cooking": ["recipe", "ingredient", "meal", "cuisine"],
        "finance": ["payment", "budget", "investment", "accounting"]
    }.get(category, [category])
    
    return AgentProfileData(
        agent_id=f"test_{category}_{subcategory or 'general'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        agent_name=f"{category.title()} Agent {subcategory or ''}",
        description=f"A {category} agent specializing in {subcategory or 'general'} functionality",
        capabilities=capabilities,
        readme_content=content,
        profile_url=f"https://agentverse.ai/agents/test_{category}_{subcategory or 'general'}",
        last_updated=datetime.now(timezone.utc).isoformat(),
        source="test_data"
    )


async def test_primary_category_detection():
    """Test primary category detection for various agent types"""
    print("🧪 Testing Primary Category Detection")
    print("=" * 50)
    
    # Test categories
    test_categories = [
        ("crypto", "defi"),
        ("crypto", "nft"), 
        ("crypto", "trading"),
        ("travel", None),
        ("cooking", None),
        ("finance", None)
    ]
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    for category, subcategory in test_categories:
        print(f"\n📋 Testing {category.upper()}{f' - {subcategory.upper()}' if subcategory else ''}")
        
        # Create test agent
        agent_profile = create_test_agent_profile(category, subcategory)
        
        # Test with meTTa categorizer (if available)
        if metta_categorizer.is_available():
            try:
                primary_category = await metta_categorizer.get_primary_category(agent_profile)
                print(f"   meTTa: {primary_category.category_type} (confidence: {primary_category.confidence:.2f})")
                print(f"   Keywords: {primary_category.keywords_matched[:5]}")
            except Exception as e:
                print(f"   meTTa: Error - {e}")
        
        # Test with simple detector
        try:
            primary_category = await simple_detector.get_primary_category(agent_profile)
            print(f"   Simple: {primary_category.category_type} (confidence: {primary_category.confidence:.2f})")
            print(f"   Keywords: {primary_category.keywords_matched[:5]}")
        except Exception as e:
            print(f"   Simple: Error - {e}")


async def test_crypto_subcategory_detection():
    """Test crypto subcategory detection"""
    print("\n\n🧪 Testing Crypto Subcategory Detection")
    print("=" * 50)
    
    # Test crypto subcategories
    crypto_subcategories = ["defi", "nft", "trading", "wallet", "dao", "gaming"]
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    for subcategory in crypto_subcategories:
        print(f"\n📋 Testing Crypto - {subcategory.upper()}")
        
        # Create test agent
        agent_profile = create_test_agent_profile("crypto", subcategory)
        
        # Test with meTTa categorizer (if available)
        if metta_categorizer.is_available():
            try:
                secondary_categories = await metta_categorizer.get_secondary_categories(agent_profile)
                crypto_secondaries = [cat for cat in secondary_categories if cat.category_type == "crypto"]
                if crypto_secondaries:
                    best_crypto = max(crypto_secondaries, key=lambda x: x.confidence)
                    print(f"   meTTa: {best_crypto.subcategory} (confidence: {best_crypto.confidence:.2f})")
                else:
                    print(f"   meTTa: No crypto subcategory detected")
            except Exception as e:
                print(f"   meTTa: Error - {e}")
        
        # Test with simple detector
        try:
            secondary_categories = await simple_detector.get_secondary_categories(agent_profile)
            crypto_secondaries = [cat for cat in secondary_categories if cat.category_type == "crypto"]
            if crypto_secondaries:
                best_crypto = max(crypto_secondaries, key=lambda x: x.confidence)
                print(f"   Simple: {best_crypto.subcategory} (confidence: {best_crypto.confidence:.2f})")
            else:
                print(f"   Simple: No crypto subcategory detected")
        except Exception as e:
            print(f"   Simple: Error - {e}")


async def test_feature_extraction():
    """Test feature extraction capabilities"""
    print("\n\n🧪 Testing Feature Extraction")
    print("=" * 50)
    
    # Test with crypto DeFi agent
    agent_profile = create_test_agent_profile("crypto", "defi")
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    print(f"\n📋 Testing Feature Extraction for Crypto DeFi Agent")
    
    # Test with meTTa categorizer (if available)
    if metta_categorizer.is_available():
        try:
            features = await metta_categorizer.extract_features(agent_profile)
            print(f"   meTTa Features:")
            print(f"     Tech Stack: {features.tech_stack[:5]}")
            print(f"     Chains: {features.supported_chains[:5]}")
            print(f"     Protocols: {features.protocols[:5]}")
            print(f"     Target Audience: {features.target_audience}")
            print(f"     Business Model: {features.business_model}")
        except Exception as e:
            print(f"   meTTa: Error - {e}")
    
    # Test with simple detector
    try:
        features = await simple_detector.extract_features(agent_profile)
        print(f"   Simple Features:")
        print(f"     Tech Stack: {features.tech_stack[:5]}")
        print(f"     Chains: {features.supported_chains[:5]}")
        print(f"     Protocols: {features.protocols[:5]}")
        print(f"     Target Audience: {features.target_audience}")
        print(f"     Business Model: {features.business_model}")
    except Exception as e:
        print(f"   Simple: Error - {e}")


async def test_multi_category_detection():
    """Test multi-category detection"""
    print("\n\n🧪 Testing Multi-Category Detection")
    print("=" * 50)
    
    # Create a hybrid agent (crypto + finance)
    hybrid_content = """
# Crypto Finance Manager

A comprehensive financial management agent that combines traditional finance with cryptocurrency investment strategies.

## Features
- Portfolio management for both traditional and crypto assets
- DeFi yield farming optimization
- Tax reporting for crypto transactions
- Budget tracking and expense management
- Investment analysis and recommendations

## Supported Assets
- Traditional: Stocks, Bonds, ETFs
- Crypto: Bitcoin, Ethereum, DeFi tokens
- DeFi Protocols: Aave, Compound, Uniswap

## Tech Stack
- Python
- Web3.py
- Pandas
- SQLite
- FastAPI

## Use Cases
- Hybrid portfolio management
- Crypto tax optimization
- DeFi yield strategies
- Financial planning
"""
    
    agent_profile = AgentProfileData(
        agent_id="test_hybrid_crypto_finance",
        agent_name="Crypto Finance Manager",
        description="Hybrid financial management agent for traditional and crypto assets",
        capabilities=["finance", "crypto", "defi", "investment", "portfolio"],
        readme_content=hybrid_content,
        profile_url="https://agentverse.ai/agents/test_hybrid",
        last_updated=datetime.now(timezone.utc).isoformat(),
        source="test_data"
    )
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    print(f"\n📋 Testing Multi-Category Detection for Hybrid Agent")
    
    # Test with meTTa categorizer (if available)
    if metta_categorizer.is_available():
        try:
            categorization = await metta_categorizer.categorize_agent(agent_profile)
            print(f"   meTTa Results:")
            print(f"     Primary: {categorization['primary_category'].category_type} (confidence: {categorization['primary_category'].confidence:.2f})")
            print(f"     Secondary: {[cat.category_type for cat in categorization['secondary_categories'][:3]]}")
            print(f"     Unknown: {categorization['is_unknown_category']}")
        except Exception as e:
            print(f"   meTTa: Error - {e}")
    
    # Test with simple detector
    try:
        categorization = await simple_detector.categorize_agent(agent_profile)
        print(f"   Simple Results:")
        print(f"     Primary: {categorization['primary_category'].category_type} (confidence: {categorization['primary_category'].confidence:.2f})")
        print(f"     Secondary: {[cat.category_type for cat in categorization['secondary_categories'][:3]]}")
        print(f"     Unknown: {categorization['is_unknown_category']}")
    except Exception as e:
        print(f"   Simple: Error - {e}")


async def test_backward_compatibility():
    """Test backward compatibility with old crypto detection API"""
    print("\n\n🧪 Testing Backward Compatibility")
    print("=" * 50)
    
    # Test with crypto agent
    agent_profile = create_test_agent_profile("crypto", "defi")
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    print(f"\n📋 Testing Backward Compatibility for Crypto Agent")
    
    # Test with meTTa categorizer (if available)
    if metta_categorizer.is_available():
        try:
            result = await metta_categorizer.detect_crypto_agent(agent_profile)
            print(f"   meTTa Crypto Detection:")
            print(f"     Is Crypto: {result['is_crypto_agent']}")
            print(f"     Score: {result['crypto_score']:.2f}")
            print(f"     Confidence: {result['confidence']:.2f}")
            print(f"     Method: {result['evaluation_method']}")
        except Exception as e:
            print(f"   meTTa: Error - {e}")
    
    # Test with simple detector
    try:
        result = await simple_detector.detect_crypto_agent(agent_profile)
        print(f"   Simple Crypto Detection:")
        print(f"     Is Crypto: {result['is_crypto_agent']}")
        print(f"     Score: {result['crypto_score']:.2f}")
        print(f"     Confidence: {result['confidence']:.2f}")
        print(f"     Method: {result['evaluation_method']}")
    except Exception as e:
        print(f"   Simple: Error - {e}")


async def test_unknown_category_detection():
    """Test detection of unknown categories"""
    print("\n\n🧪 Testing Unknown Category Detection")
    print("=" * 50)
    
    # Create an agent with minimal content
    agent_profile = AgentProfileData(
        agent_id="test_unknown",
        agent_name="Unknown Agent",
        description="A generic agent with no specific category indicators",
        capabilities=["generic", "utility"],
        readme_content="# Generic Agent\n\nThis is a generic agent with no specific category indicators.",
        profile_url="https://agentverse.ai/agents/test_unknown",
        last_updated=datetime.now(timezone.utc).isoformat(),
        source="test_data"
    )
    
    # Initialize detectors
    metta_categorizer = MeTTaCategorizer()
    simple_detector = SimpleDetector()
    
    print(f"\n📋 Testing Unknown Category Detection")
    
    # Test with meTTa categorizer (if available)
    if metta_categorizer.is_available():
        try:
            categorization = await metta_categorizer.categorize_agent(agent_profile)
            print(f"   meTTa Results:")
            print(f"     Primary: {categorization['primary_category'].category_type} (confidence: {categorization['primary_category'].confidence:.2f})")
            print(f"     Unknown: {categorization['is_unknown_category']}")
        except Exception as e:
            print(f"   meTTa: Error - {e}")
    
    # Test with simple detector
    try:
        categorization = await simple_detector.categorize_agent(agent_profile)
        print(f"   Simple Results:")
        print(f"     Primary: {categorization['primary_category'].category_type} (confidence: {categorization['primary_category'].confidence:.2f})")
        print(f"     Unknown: {categorization['is_unknown_category']}")
    except Exception as e:
        print(f"   Simple: Error - {e}")


async def test_taxonomy_information():
    """Test taxonomy information retrieval"""
    print("\n\n🧪 Testing Taxonomy Information")
    print("=" * 50)
    
    print(f"📋 Primary Categories: {len(PRIMARY_CATEGORIES)}")
    for name, category in list(PRIMARY_CATEGORIES.items())[:5]:
        print(f"   {name}: {category.name} ({len(category.keywords)} keywords)")
    
    print(f"\n📋 Crypto Subcategories: {len(CRYPTO_SUBCATEGORIES)}")
    for name, subcategory in list(CRYPTO_SUBCATEGORIES.items())[:5]:
        print(f"   {name}: {subcategory.name} ({len(subcategory.keywords)} keywords)")


async def main():
    """Run all tests"""
    print("🚀 Starting Multi-Category Agent Detection Tests")
    print("=" * 60)
    
    try:
        await test_primary_category_detection()
        await test_crypto_subcategory_detection()
        await test_feature_extraction()
        await test_multi_category_detection()
        await test_backward_compatibility()
        await test_unknown_category_detection()
        await test_taxonomy_information()
        
        print("\n\n✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
