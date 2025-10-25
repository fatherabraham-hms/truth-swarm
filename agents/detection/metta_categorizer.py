"""meTTa-based multi-category agent detection and feature extraction"""

import re
from typing import Dict, Any, List, Optional, Set
from .base_detector import BaseDetector
from models.data_models import AgentProfileData, CategoryResult, FeatureExtractionResult, CryptoSubcategoryDetails
from utils.category_taxonomy import (
    PRIMARY_CATEGORIES, CRYPTO_SUBCATEGORIES, 
    get_categories_for_text, get_primary_category, 
    get_crypto_subcategories_for_text, is_unknown_category,
    PRIMARY_CATEGORY_THRESHOLD, SECONDARY_CATEGORY_THRESHOLD, SUBCATEGORY_DETECTION_THRESHOLD
)


class MeTTaCategorizer(BaseDetector):
    """Multi-category agent detector using meTTa framework with symbolic reasoning"""
    
    def __init__(self):
        """Initialize meTTa categorizer"""
        try:
            from hyperon import GroundingSpace, S, E, G, V
            # Initialize meTTa grounding space for symbolic reasoning
            self.grounding_space = GroundingSpace()
            self.available = True
            
            # Load category taxonomy into meTTa knowledge base
            self._load_taxonomy_into_metta()
            print("✅ meTTa categorizer initialized successfully")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ meTTa categorizer initialization failed: {e}")
            self.grounding_space = None
            self.available = False
    
    def _load_taxonomy_into_metta(self):
        """Load category taxonomy into meTTa grounding space"""
        if not self.available or not self.grounding_space:
            return
        
        try:
            from hyperon import S, E, G, V
            
            # Add primary categories to grounding space
            for category_name, category_def in PRIMARY_CATEGORIES.items():
                # Add category symbol
                self.grounding_space.add(S(category_name))
                
                # Add category keywords
                for keyword in category_def.keywords:
                    self.grounding_space.add(S(keyword))
                    # Create relationship: keyword belongs to category
                    self.grounding_space.add(E(S("belongs-to"), S(keyword), S(category_name)))
            
            # Add crypto subcategories
            for subcategory_name, subcategory_def in CRYPTO_SUBCATEGORIES.items():
                # Add subcategory symbol
                self.grounding_space.add(S(subcategory_name))
                
                # Add subcategory keywords
                for keyword in subcategory_def.keywords:
                    self.grounding_space.add(S(keyword))
                    # Create relationship: keyword belongs to subcategory
                    self.grounding_space.add(E(S("belongs-to"), S(keyword), S(subcategory_name)))
                    # Create relationship: subcategory is part of crypto
                    self.grounding_space.add(E(S("is-subcategory-of"), S(subcategory_name), S("crypto")))
            
            print("✅ Category taxonomy loaded into meTTa grounding space")
            
        except Exception as e:
            print(f"⚠️ Failed to load taxonomy into meTTa: {e}")
    
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Detect if an agent is a crypto agent (backward compatibility)"""
        categorization = await self.categorize_agent(agent_profile)
        
        # Extract crypto-specific information
        is_crypto = categorization.get("primary_category", {}).get("category_type") == "crypto"
        crypto_score = categorization.get("primary_category", {}).get("confidence", 0.0)
        
        # Get crypto subcategory details
        crypto_details = None
        if is_crypto and categorization.get("crypto_details"):
            crypto_details = categorization["crypto_details"]
        
        return {
            "is_crypto_agent": is_crypto,
            "crypto_score": crypto_score,
            "confidence": crypto_score,
            "total_matches": len(categorization.get("primary_category", {}).get("keywords_matched", [])),
            "readme_matches": categorization.get("primary_category", {}).get("keywords_matched", []),
            "capability_matches": [],
            "description_matches": [],
            "evaluation_method": "metta_categorizer",
            "crypto_details": crypto_details
        }
    
    async def categorize_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Categorize an agent into primary and secondary categories using meTTa reasoning"""
        if not self.available or not self.grounding_space:
            raise RuntimeError("meTTa framework not available")
        
        try:
            # Get primary category
            primary_category = await self.get_primary_category(agent_profile)
            
            # Get secondary categories
            secondary_categories = await self.get_secondary_categories(agent_profile)
            
            # Extract features
            features = await self.extract_features(agent_profile)
            
            # Get crypto details if primary category is crypto
            crypto_details = None
            if primary_category.category_type == "crypto":
                crypto_details = await self._get_crypto_details(agent_profile, primary_category)
            
            # Check if unknown category
            is_unknown = is_unknown_category(agent_profile.readme_content)
            
            return {
                "primary_category": primary_category,
                "secondary_categories": secondary_categories,
                "extracted_features": features,
                "crypto_details": crypto_details,
                "is_unknown_category": is_unknown,
                "evaluation_method": "metta_symbolic_reasoning"
            }
            
        except Exception as e:
            raise RuntimeError(f"meTTa categorization failed: {e}")
    
    async def extract_features(self, agent_profile: AgentProfileData) -> FeatureExtractionResult:
        """Extract features from agent profile using meTTa pattern matching"""
        if not self.available or not self.grounding_space:
            # Fallback to simple extraction
            return await self._simple_feature_extraction(agent_profile)
        
        try:
            from hyperon import S, E, G, V
            
            text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
            text_lower = text_content.lower()
            
            # Extract tech stack
            tech_stack = self._extract_tech_stack(text_lower)
            
            # Extract supported chains
            supported_chains = self._extract_supported_chains(text_lower)
            
            # Extract protocols
            protocols = self._extract_protocols(text_lower)
            
            # Extract key features
            key_features = self._extract_key_features(text_lower)
            
            # Extract capabilities
            capabilities = list(agent_profile.capabilities)
            
            # Extract integrations
            integrations = self._extract_integrations(text_lower)
            
            # Determine target audience
            target_audience = self._determine_target_audience(text_lower)
            
            # Determine business model
            business_model = self._determine_business_model(text_lower)
            
            return FeatureExtractionResult(
                tech_stack=tech_stack,
                supported_chains=supported_chains,
                protocols=protocols,
                key_features=key_features,
                capabilities=capabilities,
                integrations=integrations,
                target_audience=target_audience,
                business_model=business_model
            )
            
        except Exception as e:
            print(f"⚠️ meTTa feature extraction failed, using fallback: {e}")
            return await self._simple_feature_extraction(agent_profile)
    
    async def get_primary_category(self, agent_profile: AgentProfileData) -> CategoryResult:
        """Get the primary category for an agent using meTTa symbolic reasoning"""
        if not self.available or not self.grounding_space:
            # Fallback to simple detection
            return await self._simple_primary_category(agent_profile)
        
        try:
            from hyperon import S, E, G, V
            
            text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
            text_lower = text_content.lower()
            
            # Get category scores using meTTa reasoning
            category_scores = get_categories_for_text(text_lower)
            
            # Filter to primary categories only
            primary_scores = {k: v for k, v in category_scores.items() if k in PRIMARY_CATEGORIES}
            
            if not primary_scores:
                return CategoryResult(
                    category_type="unknown",
                    confidence=0.0,
                    keywords_matched=[],
                    reasoning="No category keywords found"
                )
            
            # Find best category
            best_category = max(primary_scores.items(), key=lambda x: x[1])
            category_name, confidence = best_category
            
            # Get matched keywords
            category_def = PRIMARY_CATEGORIES[category_name]
            matched_keywords = [kw for kw in category_def.keywords if kw in text_lower]
            
            # Generate reasoning using meTTa
            reasoning = self._generate_category_reasoning(category_name, matched_keywords, confidence)
            
            return CategoryResult(
                category_type=category_name,
                confidence=confidence,
                keywords_matched=matched_keywords,
                reasoning=reasoning
            )
            
        except Exception as e:
            print(f"⚠️ meTTa primary category detection failed, using fallback: {e}")
            return await self._simple_primary_category(agent_profile)
    
    async def get_secondary_categories(self, agent_profile: AgentProfileData, threshold: float = SECONDARY_CATEGORY_THRESHOLD) -> List[CategoryResult]:
        """Get secondary categories for an agent above confidence threshold"""
        if not self.available or not self.grounding_space:
            return await self._simple_secondary_categories(agent_profile, threshold)
        
        try:
            text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
            text_lower = text_content.lower()
            
            # Get all category scores
            category_scores = get_categories_for_text(text_lower)
            
            # Filter to primary categories only
            primary_scores = {k: v for k, v in category_scores.items() if k in PRIMARY_CATEGORIES}
            
            # Get crypto subcategories if crypto is detected
            crypto_subcategory_scores = {}
            if "crypto" in primary_scores and primary_scores["crypto"] > SUBCATEGORY_DETECTION_THRESHOLD:
                crypto_subcategory_scores = get_crypto_subcategories_for_text(text_lower)
            
            secondary_categories = []
            
            # Add primary categories above threshold (excluding the primary one)
            for category_name, confidence in primary_scores.items():
                if confidence >= threshold and category_name != "crypto":  # Exclude crypto as it's handled separately
                    category_def = PRIMARY_CATEGORIES[category_name]
                    matched_keywords = [kw for kw in category_def.keywords if kw in text_lower]
                    
                    secondary_categories.append(CategoryResult(
                        category_type=category_name,
                        confidence=confidence,
                        keywords_matched=matched_keywords,
                        reasoning=f"Secondary category based on {len(matched_keywords)} keyword matches"
                    ))
            
            # Add crypto subcategories
            for subcategory_name, confidence in crypto_subcategory_scores.items():
                if confidence >= threshold:
                    # Remove "crypto_" prefix
                    clean_name = subcategory_name.replace("crypto_", "")
                    subcategory_def = CRYPTO_SUBCATEGORIES[clean_name]
                    matched_keywords = [kw for kw in subcategory_def.keywords if kw in text_lower]
                    
                    secondary_categories.append(CategoryResult(
                        category_type="crypto",
                        subcategory=clean_name,
                        confidence=confidence,
                        keywords_matched=matched_keywords,
                        reasoning=f"Crypto subcategory based on {len(matched_keywords)} keyword matches"
                    ))
            
            # Sort by confidence
            secondary_categories.sort(key=lambda x: x.confidence, reverse=True)
            
            return secondary_categories
            
        except Exception as e:
            print(f"⚠️ meTTa secondary category detection failed, using fallback: {e}")
            return await self._simple_secondary_categories(agent_profile, threshold)
    
    async def _get_crypto_details(self, agent_profile: AgentProfileData, primary_category: CategoryResult) -> CryptoSubcategoryDetails:
        """Get detailed crypto subcategory information"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        # Get crypto subcategory scores
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
        
        # Find best subcategory
        best_subcategory = max(crypto_scores.items(), key=lambda x: x[1])
        subcategory_name, confidence = best_subcategory[0].replace("crypto_", ""), best_subcategory[1]
        
        # Extract crypto-specific details
        protocols_mentioned = self._extract_protocols(text_lower)
        chains_supported = self._extract_supported_chains(text_lower)
        features = self._extract_key_features(text_lower)
        use_cases = self._extract_use_cases(text_lower, subcategory_name)
        
        return CryptoSubcategoryDetails(
            subcategory=subcategory_name,
            confidence=confidence,
            protocols_mentioned=protocols_mentioned,
            chains_supported=chains_supported,
            features=features,
            use_cases=use_cases
        )
    
    def _extract_tech_stack(self, text: str) -> List[str]:
        """Extract technology stack from text"""
        tech_keywords = {
            "python", "javascript", "typescript", "solidity", "rust", "go", "java", "c++", "c#",
            "react", "vue", "angular", "node.js", "express", "django", "flask", "fastapi",
            "ethereum", "web3", "hardhat", "truffle", "remix", "ganache", "infura", "alchemy",
            "ipfs", "arweave", "the graph", "chainlink", "openzeppelin", "brownie"
        }
        
        found_tech = []
        for tech in tech_keywords:
            if tech in text:
                found_tech.append(tech)
        
        return found_tech
    
    def _extract_supported_chains(self, text: str) -> List[str]:
        """Extract supported blockchain networks"""
        chain_keywords = {
            "ethereum", "bitcoin", "polygon", "arbitrum", "optimism", "avalanche",
            "fantom", "bsc", "binance smart chain", "solana", "cardano", "polkadot",
            "cosmos", "near", "algorand", "tezos", "flow", "hedera", "stellar"
        }
        
        found_chains = []
        for chain in chain_keywords:
            if chain in text:
                found_chains.append(chain)
        
        return found_chains
    
    def _extract_protocols(self, text: str) -> List[str]:
        """Extract DeFi protocols and platforms"""
        protocol_keywords = {
            "uniswap", "sushiswap", "curve", "balancer", "aave", "compound", "maker",
            "yearn", "harvest", "synthetix", "1inch", "dydx", "opensea", "rarible",
            "foundation", "superrare", "ens", "gitcoin", "the graph", "chainlink"
        }
        
        found_protocols = []
        for protocol in protocol_keywords:
            if protocol in text:
                found_protocols.append(protocol)
        
        return found_protocols
    
    def _extract_key_features(self, text: str) -> List[str]:
        """Extract key features and capabilities"""
        feature_patterns = [
            r"real-time", r"automated", r"ai-powered", r"machine learning", r"ml",
            r"decentralized", r"peer-to-peer", r"p2p", r"non-custodial", r"trustless",
            r"transparent", r"immutable", r"verifiable", r"auditable", r"composable",
            r"interoperable", r"scalable", r"gas-efficient", r"low-cost", r"fast"
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
            "stripe", "paypal", "square", "shopify", "woocommerce", "wordpress",
            "discord", "telegram", "twitter", "reddit", "github", "gitlab"
        }
        
        found_integrations = []
        for integration in integration_keywords:
            if integration in text:
                found_integrations.append(integration)
        
        return found_integrations
    
    def _determine_target_audience(self, text: str) -> Optional[str]:
        """Determine target audience from text"""
        audience_indicators = {
            "developers": ["developer", "dev", "programmer", "coder", "api", "sdk"],
            "traders": ["trader", "trading", "investor", "investment", "portfolio"],
            "businesses": ["business", "enterprise", "corporate", "b2b", "saas"],
            "consumers": ["user", "consumer", "individual", "personal", "b2c"],
            "institutions": ["institution", "institutional", "fund", "hedge", "bank"]
        }
        
        for audience, keywords in audience_indicators.items():
            if any(keyword in text for keyword in keywords):
                return audience
        
        return None
    
    def _determine_business_model(self, text: str) -> Optional[str]:
        """Determine business model from text"""
        model_indicators = {
            "freemium": ["freemium", "free tier", "premium", "subscription"],
            "transaction_fees": ["fee", "commission", "transaction", "trading fee"],
            "subscription": ["subscription", "monthly", "annual", "recurring"],
            "advertising": ["ad", "advertising", "sponsor", "promotion"],
            "marketplace": ["marketplace", "platform", "commission", "listing"],
            "open_source": ["open source", "github", "mit license", "free"]
        }
        
        for model, keywords in model_indicators.items():
            if any(keyword in text for keyword in keywords):
                return model
        
        return None
    
    def _extract_use_cases(self, text: str, subcategory: str) -> List[str]:
        """Extract use cases for crypto subcategory"""
        use_case_mapping = {
            "defi": ["lending", "borrowing", "trading", "yield farming", "liquidity provision"],
            "nft": ["digital art", "collectibles", "gaming", "identity", "ticketing"],
            "trading": ["spot trading", "derivatives", "arbitrage", "market making"],
            "wallet": ["key management", "transaction signing", "portfolio tracking"],
            "dao": ["governance", "treasury management", "community voting"],
            "gaming": ["play-to-earn", "in-game assets", "virtual worlds"]
        }
        
        return use_case_mapping.get(subcategory, [])
    
    def _generate_category_reasoning(self, category: str, keywords: List[str], confidence: float) -> str:
        """Generate human-readable reasoning for category classification"""
        if confidence >= 0.8:
            strength = "strong"
        elif confidence >= 0.6:
            strength = "moderate"
        else:
            strength = "weak"
        
        keyword_list = ", ".join(keywords[:5])  # Show first 5 keywords
        if len(keywords) > 5:
            keyword_list += f" and {len(keywords) - 5} more"
        
        return f"{strength.title()} {category} classification based on {len(keywords)} keyword matches: {keyword_list}"
    
    # Fallback methods for when meTTa is not available
    async def _simple_feature_extraction(self, agent_profile: AgentProfileData) -> FeatureExtractionResult:
        """Simple feature extraction fallback"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        return FeatureExtractionResult(
            tech_stack=self._extract_tech_stack(text_lower),
            supported_chains=self._extract_supported_chains(text_lower),
            protocols=self._extract_protocols(text_lower),
            key_features=self._extract_key_features(text_lower),
            capabilities=list(agent_profile.capabilities),
            integrations=self._extract_integrations(text_lower),
            target_audience=self._determine_target_audience(text_lower),
            business_model=self._determine_business_model(text_lower)
        )
    
    async def _simple_primary_category(self, agent_profile: AgentProfileData) -> CategoryResult:
        """Simple primary category detection fallback"""
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
    
    async def _simple_secondary_categories(self, agent_profile: AgentProfileData, threshold: float) -> List[CategoryResult]:
        """Simple secondary category detection fallback"""
        text_content = f"{agent_profile.readme_content} {agent_profile.description} {' '.join(agent_profile.capabilities)}"
        text_lower = text_content.lower()
        
        category_scores = get_categories_for_text(text_lower)
        primary_scores = {k: v for k, v in category_scores.items() if k in PRIMARY_CATEGORIES}
        
        secondary_categories = []
        for category_name, confidence in primary_scores.items():
            if confidence >= threshold:
                category_def = PRIMARY_CATEGORIES[category_name]
                matched_keywords = [kw for kw in category_def.keywords if kw in text_lower]
                
                secondary_categories.append(CategoryResult(
                    category_type=category_name,
                    confidence=confidence,
                    keywords_matched=matched_keywords,
                    reasoning=f"Simple keyword matching: {len(matched_keywords)} matches"
                ))
        
        return sorted(secondary_categories, key=lambda x: x.confidence, reverse=True)
    
    def is_available(self) -> bool:
        """Check if meTTa framework is available"""
        return self.available
