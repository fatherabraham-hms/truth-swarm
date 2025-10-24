"""Simple fallback crypto agent detection logic"""

from typing import Dict, Any
from .base_detector import BaseDetector
from models.data_models import AgentProfileData
from utils.crypto_keywords import CRYPTO_KEYWORDS


class SimpleDetector(BaseDetector):
    """Simple crypto agent detector using keyword matching"""
    
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """Simple crypto detection fallback when meTTa is not available"""
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
