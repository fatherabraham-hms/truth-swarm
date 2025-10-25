"""Simple fallback multi-category agent detection logic"""

from typing import Dict, Any, List
from .base_detector import BaseDetector
from models.data_models import AgentProfileData, CategoryResult, FeatureExtractionResult
from utils.crypto_keywords import CRYPTO_KEYWORDS
from utils.category_taxonomy import (
    PRIMARY_CATEGORIES, CRYPTO_SUBCATEGORIES,
    get_categories_for_text, get_primary_category, 
    get_crypto_subcategories_for_text, is_unknown_category,
    PRIMARY_CATEGORY_THRESHOLD, SECONDARY_CATEGORY_THRESHOLD, SUBCATEGORY_DETECTION_THRESHOLD
)


class SimpleDetector(BaseDetector):
    """Simple multi-category agent detector using keyword matching"""
    
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Simple crypto detection fallback when meTTa is not available (backward compatibility)"""
        readme_content = agent_profile.readme_content.lower()
        capabilities = [cap.lower() for cap in agent_profile.capabilities]
        description = agent_profile.description.lower()
        
        # Find crypto keywords in different sources
        readme_matches = [kw for kw in CRYPTO_KEYWORDS if kw.lower() in readme_content]
        cap_matches = [kw for kw in CRYPTO_KEYWORDS if any(kw.lower() in cap for cap in capabilities)]
        desc_matches = [kw for kw in CRYPTO_KEYWORDS if kw.lower() in description]
        
        # Calculate scores
        total_matches = len(readme_matches) + len(cap_matches) + len(desc_matches)
        crypto_score = min(1.0, total_matches / 10)  # Normalize to 0-1 scale
        
        # Determine if it's a crypto agent
        is_crypto_agent = crypto_score > 0.3
        
        # Calculate confidence
        if total_matches > 15:
            confidence = 0.9
        elif total_matches > 10:
            confidence = 0.8
        elif total_matches > 5:
            confidence = 0.7
        elif total_matches > 2:
            confidence = 0.6
        else:
            confidence = 0.3
        
        return {
            "is_crypto_agent": is_crypto_agent,
            "crypto_score": crypto_score,
            "confidence": confidence,
            "total_matches": total_matches,
            "readme_matches": readme_matches,
            "capability_matches": cap_matches,
            "description_matches": desc_matches,
            "evaluation_method": "simple_fallback",
            "analysis": {
                "readme_crypto_mentions": len(readme_matches),
                "capability_crypto_mentions": len(cap_matches),
                "description_crypto_mentions": len(desc_matches),
                "strong_crypto_indicators": [
                    kw for kw in ["bitcoin", "ethereum", "blockchain", "defi", "crypto"] 
                    if kw in readme_matches or kw in cap_matches or kw in desc_matches
                ]
            }
        }
    
    async def categorize_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Simple multi-category detection fallback"""
        try:
            print(f"🔍 Simple detector: Starting categorization for {agent_profile.agent_id}")
            
            # Get primary category
            print("🔍 Simple detector: Getting primary category...")
            primary_category = await self.get_primary_category(agent_profile)
            print(f"🔍 Simple detector: Primary category: {primary_category.category_type}")
            
            # Get secondary categories
            print("🔍 Simple detector: Getting secondary categories...")
            secondary_categories = await self.get_secondary_categories(agent_profile)
            print(f"🔍 Simple detector: Found {len(secondary_categories)} secondary categories")
            
            # Extract features
            print("🔍 Simple detector: Extracting features...")
            features = await self.extract_features(agent_profile)
            print(f"🔍 Simple detector: Features extracted: {len(features.tech_stack)} tech items")
            
            # Get crypto details if primary category is crypto
            crypto_details = None
            if primary_category.category_type == "crypto":
                print("🔍 Simple detector: Getting crypto details...")
                crypto_details = await self._get_crypto_details(agent_profile, primary_category)
                print(f"🔍 Simple detector: Crypto details: {crypto_details}")
            
            # Check if unknown category
            print("🔍 Simple detector: Checking if unknown category...")
            is_unknown = is_unknown_category(agent_profile.readme_content)
            print(f"🔍 Simple detector: Is unknown: {is_unknown}")
            
            result = {
                "primary_category": primary_category,
                "secondary_categories": secondary_categories,
                "extracted_features": features,
                "crypto_details": crypto_details,
                "is_unknown_category": is_unknown,
                "evaluation_method": "simple_keyword_matching"
            }
            print(f"🔍 Simple detector: Categorization complete!")
            return result
            
        except Exception as e:
            raise RuntimeError(f"Simple categorization failed: {e}")
    
    async def extract_features(self, agent_profile: AgentProfileData) -> FeatureExtractionResult:
        """Simple feature extraction fallback"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        # Extract basic features using simple keyword matching
        tech_stack = self._extract_tech_stack(text_lower)
        supported_chains = self._extract_supported_chains(text_lower)
        protocols = self._extract_protocols(text_lower)
        key_features = self._extract_key_features(text_lower)
        integrations = self._extract_integrations(text_lower)
        
        return FeatureExtractionResult(
            tech_stack=tech_stack,
            supported_chains=supported_chains,
            protocols=protocols,
            key_features=key_features,
            capabilities=list(agent_profile.capabilities),
            integrations=integrations,
            target_audience=self._determine_target_audience(text_lower),
            business_model=self._determine_business_model(text_lower)
        )
    
    async def get_primary_category(self, agent_profile: AgentProfileData) -> CategoryResult:
        """Get primary category using simple keyword matching"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        category_name = get_primary_category(text_lower)
        if not category_name:
            return CategoryResult(
                category_type="unknown",
                confidence=0.0,
                keywords_matched=[],
                reasoning="No category keywords found"
            )
        
        category_def = PRIMARY_CATEGORIES[category_name]
        matched_keywords = [kw for kw in category_def.keywords if kw in text_lower]
        confidence = min(1.0, len(matched_keywords) / len(category_def.keywords))
        
        return CategoryResult(
            category_type=category_name,
            confidence=confidence,
            keywords_matched=matched_keywords,
            reasoning=f"Simple keyword matching: {len(matched_keywords)} matches"
        )
    
    async def get_secondary_categories(self, agent_profile: AgentProfileData, threshold: float = SECONDARY_CATEGORY_THRESHOLD) -> List[CategoryResult]:
        """Get secondary categories using simple keyword matching"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        category_scores = get_categories_for_text(text_lower)
        primary_scores = {k: v for k, v in category_scores.items() if k in PRIMARY_CATEGORIES}
        
        # Get crypto subcategories if crypto is detected
        crypto_subcategory_scores = {}
        if "crypto" in primary_scores and primary_scores["crypto"] > SUBCATEGORY_DETECTION_THRESHOLD:
            crypto_subcategory_scores = get_crypto_subcategories_for_text(text_lower)
        
        secondary_categories = []
        
        # Add primary categories above threshold (excluding crypto as it's handled separately)
        for category_name, confidence in primary_scores.items():
            if confidence >= threshold and category_name != "crypto":
                category_def = PRIMARY_CATEGORIES[category_name]
                matched_keywords = [kw for kw in category_def.keywords if kw in text_lower]
                
                secondary_categories.append(CategoryResult(
                    category_type=category_name,
                    confidence=confidence,
                    keywords_matched=matched_keywords,
                    reasoning=f"Secondary category: {len(matched_keywords)} keyword matches"
                ))
        
        # Add crypto subcategories
        for subcategory_name, confidence in crypto_subcategory_scores.items():
            if confidence >= threshold:
                clean_name = subcategory_name.replace("crypto_", "")
                subcategory_def = CRYPTO_SUBCATEGORIES[clean_name]
                matched_keywords = [kw for kw in subcategory_def.keywords if kw in text_lower]
                
                secondary_categories.append(CategoryResult(
                    category_type="crypto",
                    subcategory=clean_name,
                    confidence=confidence,
                    keywords_matched=matched_keywords,
                    reasoning=f"Crypto subcategory: {len(matched_keywords)} keyword matches"
                ))
        
        return sorted(secondary_categories, key=lambda x: x.confidence, reverse=True)
    
    async def _get_crypto_details(self, agent_profile: AgentProfileData, primary_category: CategoryResult):
        """Get crypto subcategory details"""
        from models.data_models import CryptoSubcategoryDetails
        
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        crypto_scores = get_crypto_subcategories_for_text(text_lower)
        
        if not crypto_scores:
            return CryptoSubcategoryDetails(
                subcategory="general",
                confidence=0.0,
                protocols_mentioned=[],
                chains_supported=[],
                features=[],
                use_cases=[]
            )
        
        best_subcategory = max(crypto_scores.items(), key=lambda x: x[1])
        subcategory_name, confidence = best_subcategory[0].replace("crypto_", ""), best_subcategory[1]
        
        return CryptoSubcategoryDetails(
            subcategory=subcategory_name,
            confidence=confidence,
            protocols_mentioned=self._extract_protocols(text_lower),
            chains_supported=self._extract_supported_chains(text_lower),
            features=self._extract_key_features(text_lower),
            use_cases=self._extract_use_cases(text_lower, subcategory_name)
        )
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        """Extract technology stack from text"""
        tech_keywords = {
            "python", "javascript", "typescript", "solidity", "rust", "go", "java", "c++", "c#",
            "react", "vue", "angular", "node.js", "express", "django", "flask", "fastapi",
            "ethereum", "web3", "hardhat", "truffle", "remix", "ganache", "infura", "alchemy"
        }
        
        return [tech for tech in tech_keywords if tech in text]
    
    def _extract_supported_chains(self, text: str) -> List[str]:
        """Extract supported blockchain networks"""
        chain_keywords = {
            "ethereum", "bitcoin", "polygon", "arbitrum", "optimism", "avalanche",
            "fantom", "bsc", "binance smart chain", "solana", "cardano", "polkadot"
        }
        
        return [chain for chain in chain_keywords if chain in text]
    
    def _extract_protocols(self, text: str) -> List[str]:
        """Extract DeFi protocols and platforms"""
        protocol_keywords = {
            "uniswap", "sushiswap", "curve", "balancer", "aave", "compound", "maker",
            "yearn", "harvest", "synthetix", "1inch", "dydx", "opensea", "rarible"
        }
        
        return [protocol for protocol in protocol_keywords if protocol in text]
    
    def _extract_key_features(self, text: str) -> List[str]:
        """Extract key features and capabilities"""
        import re
        feature_patterns = [
            r"real-time", r"automated", r"ai-powered", r"machine learning", r"ml",
            r"decentralized", r"peer-to-peer", r"p2p", r"non-custodial", r"trustless"
        ]
        
        found_features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_features.extend(matches)
        
        return list(set(found_features))
    
    def _extract_integrations(self, text: str) -> List[str]:
        """Extract third-party integrations"""
        integration_keywords = {
            "metamask", "walletconnect", "coinbase", "binance", "kraken", "gemini",
            "stripe", "paypal", "square", "shopify", "woocommerce", "wordpress"
        }
        
        return [integration for integration in integration_keywords if integration in text]
    
    def _determine_target_audience(self, text: str) -> str:
        """Determine target audience from text"""
        audience_indicators = {
            "developers": ["developer", "dev", "programmer", "coder", "api", "sdk"],
            "traders": ["trader", "trading", "investor", "investment", "portfolio"],
            "businesses": ["business", "enterprise", "corporate", "b2b", "saas"],
            "consumers": ["user", "consumer", "individual", "personal", "b2c"]
        }
        
        for audience, keywords in audience_indicators.items():
            if any(keyword in text for keyword in keywords):
                return audience
        
        return "general"
    
    def _determine_business_model(self, text: str) -> str:
        """Determine business model from text"""
        model_indicators = {
            "freemium": ["freemium", "free tier", "premium", "subscription"],
            "transaction_fees": ["fee", "commission", "transaction", "trading fee"],
            "subscription": ["subscription", "monthly", "annual", "recurring"],
            "open_source": ["open source", "github", "mit license", "free"]
        }
        
        for model, keywords in model_indicators.items():
            if any(keyword in text for keyword in keywords):
                return model
        
        return "unknown"
    
    def _extract_use_cases(self, text: str, subcategory: str) -> List[str]:
        """Extract use cases for crypto subcategory"""
        use_case_mapping = {
            "defi": ["lending", "borrowing", "trading", "yield farming"],
            "nft": ["digital art", "collectibles", "gaming", "identity"],
            "trading": ["spot trading", "derivatives", "arbitrage"],
            "wallet": ["key management", "transaction signing"],
            "dao": ["governance", "treasury management"],
            "gaming": ["play-to-earn", "in-game assets"]
        }
        
        return use_case_mapping.get(subcategory, [])
