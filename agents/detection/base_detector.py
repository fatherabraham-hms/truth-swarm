"""Base detector class for crypto agent detection"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from models.data_models import AgentProfileData


class BaseDetector(ABC):
    """Abstract base class for crypto agent detectors"""
    
    @abstractmethod
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """
        Detect if an agent is a crypto agent
        
        Args:
            agent_profile: Agent profile data to analyze
            
        Returns:
            Dictionary containing detection results
        """
        pass
