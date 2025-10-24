"""Detection modules for crypto agent analysis"""

from .metta_detector import MeTTaDetector
from .simple_detector import SimpleDetector
from .base_detector import BaseDetector

__all__ = ['MeTTaDetector', 'SimpleDetector', 'BaseDetector']
