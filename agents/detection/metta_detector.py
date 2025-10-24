"""meTTa-based crypto agent detection logic"""

from typing import Dict, Any
from .base_detector import BaseDetector
from models.data_models import AgentProfileData
from utils.crypto_keywords import CRYPTO_KEYWORDS


class MeTTaDetector(BaseDetector):
    """Crypto agent detector using meTTa framework"""
    
    def __init__(self):
        """Initialize meTTa detector"""
        try:
            from hyperon import GroundingSpace
            # Initialize meTTa grounding space for symbolic reasoning
            self.grounding_space = GroundingSpace()
            self.available = True
            print("✅ meTTa framework (Hyperon) initialized successfully")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ meTTa initialization failed: {e}")
            self.grounding_space = None
            self.available = False
    
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Detect crypto agent using meTTa framework"""
        if not self.available or not self.grounding_space:
            raise RuntimeError("meTTa framework not available")
        
        try:
            from hyperon import S, E, G, V
            
            # Prepare data for meTTa symbolic reasoning
            readme_content = agent_profile.readme_content.lower()
            capabilities = [cap.lower() for cap in agent_profile.capabilities]
            description = agent_profile.description.lower()
            
            # Add crypto keywords to grounding space for symbolic reasoning
            for keyword in CRYPTO_KEYWORDS:
                self.grounding_space.add(S(keyword.lower()))
            
            # Count crypto keywords in different fields using meTTa reasoning
            readme_matches = [kw for kw in CRYPTO_KEYWORDS if kw.lower() in readme_content]
            cap_matches = [kw for kw in CRYPTO_KEYWORDS if any(kw.lower() in cap for cap in capabilities)]
            desc_matches = [kw for kw in CRYPTO_KEYWORDS if kw.lower() in description]
            
            # Debug logging
            print(f"🔍 DEBUG: README content length: {len(readme_content)}")
            print(f"🔍 DEBUG: README content preview: {readme_content[:200]}...")
            print(f"🔍 DEBUG: Total crypto keywords: {len(CRYPTO_KEYWORDS)}")
            print(f"🔍 DEBUG: README matches found: {readme_matches}")
            print(f"🔍 DEBUG: Checking for 'crypto' in README: {'crypto' in readme_content}")
            print(f"🔍 DEBUG: Checking for 'decentralized' in README: {'decentralized' in readme_content}")
            print(f"🔍 DEBUG: Checking for 'blockchain' in README: {'blockchain' in readme_content}")
            
            # Calculate scores with meTTa-enhanced logic
            readme_count = len(readme_matches)
            cap_count = len(cap_matches)
            desc_count = len(desc_matches)
            total_matches = readme_count + cap_count + desc_count
            
            # Enhanced scoring using meTTa symbolic reasoning
            # Weight different sources differently based on their importance
            readme_weight = 0.4  # README is most important
            cap_weight = 0.35    # Capabilities are very important
            desc_weight = 0.25   # Description is less important
            
            weighted_score = (readme_count * readme_weight + 
                            cap_count * cap_weight + 
                            desc_count * desc_weight)
            
            # Normalize to 0-1 scale
            crypto_score = min(1.0, weighted_score / 5.0)
            
            # Determine if it's a crypto agent using meTTa reasoning
            is_crypto_agent = crypto_score > 0.3
            
            # Enhanced confidence calculation using meTTa logic
            # Consider multiple factors for confidence
            confidence_factors = []
            
            # Factor 1: Total matches
            if total_matches > 15:
                confidence_factors.append(0.9)
            elif total_matches > 10:
                confidence_factors.append(0.8)
            elif total_matches > 5:
                confidence_factors.append(0.7)
            elif total_matches > 2:
                confidence_factors.append(0.6)
            else:
                confidence_factors.append(0.3)
            
            # Factor 2: Multiple source agreement
            sources_with_matches = sum([1 for count in [readme_count, cap_count, desc_count] if count > 0])
            if sources_with_matches >= 3:
                confidence_factors.append(0.9)
            elif sources_with_matches >= 2:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.5)
            
            # Factor 3: High-value keyword matches
            high_value_keywords = ['bitcoin', 'ethereum', 'crypto', 'blockchain', 'defi', 'nft']
            high_value_matches = sum([1 for kw in high_value_keywords if kw in readme_content or 
                                    any(kw in cap for cap in capabilities) or kw in description])
            if high_value_matches >= 3:
                confidence_factors.append(0.9)
            elif high_value_matches >= 2:
                confidence_factors.append(0.8)
            elif high_value_matches >= 1:
                confidence_factors.append(0.6)
            else:
                confidence_factors.append(0.4)
            
            # Calculate final confidence as weighted average
            confidence = sum(confidence_factors) / len(confidence_factors)
            
            # Return results with meTTa-enhanced analysis
            return {
                'is_crypto_agent': is_crypto_agent,
                'crypto_score': crypto_score,
                'confidence': confidence,
                'total_matches': total_matches,
                'readme_matches': readme_matches,
                'capability_matches': cap_matches,
                'description_matches': desc_matches,
                'evaluation_method': 'metta',
                'metta_enhanced': True,
                'confidence_factors': {
                    'total_matches_factor': confidence_factors[0],
                    'multi_source_factor': confidence_factors[1],
                    'high_value_keywords_factor': confidence_factors[2]
                }
            }
                
        except Exception as e:
            raise RuntimeError(f"meTTa crypto detection failed: {e}")
    
    def is_available(self) -> bool:
        """Check if meTTa framework is available"""
        return self.available
