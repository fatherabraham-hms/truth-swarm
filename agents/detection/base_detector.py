"""Base detector class for multi-category agent detection"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from models.data_models import AgentProfileData, CategoryResult, FeatureExtractionResult


class BaseDetector(ABC):
    """Abstract base class for multi-category agent detectors"""
    
    @abstractmethod
    async def detect_crypto_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """
        Detect if an agent is a crypto agent (backward compatibility)
        
        Args:
            agent_profile: Agent profile data to analyze
            
        Returns:
            Dictionary containing detection results
        """
        pass
    
    @abstractmethod
    async def categorize_agent(self, agent_profile: AgentProfileData) -> Dict[str, Any]:
        """
        Categorize an agent into primary and secondary categories
        
        Args:
            agent_profile: Agent profile data to analyze
            
        Returns:
            Dictionary containing categorization results
        """
        pass
    
    @abstractmethod
    async def extract_features(self, agent_profile: AgentProfileData) -> FeatureExtractionResult:
        """
        Extract features from agent profile
        
        Args:
            agent_profile: Agent profile data to analyze
            
        Returns:
            FeatureExtractionResult containing extracted features
        """
        pass
    
    @abstractmethod
    async def get_primary_category(self, agent_profile: AgentProfileData) -> CategoryResult:
        """
        Get the primary category for an agent
        
        Args:
            agent_profile: Agent profile data to analyze
            
        Returns:
            CategoryResult for the primary category
        """
        pass
    
    @abstractmethod
    async def get_secondary_categories(self, agent_profile: AgentProfileData, threshold: float = 0.4) -> List[CategoryResult]:
        """
        Get secondary categories for an agent above confidence threshold
        
        Args:
            agent_profile: Agent profile data to analyze
            threshold: Minimum confidence threshold for secondary categories
            
        Returns:
            List of CategoryResult for secondary categories
        """
        pass
