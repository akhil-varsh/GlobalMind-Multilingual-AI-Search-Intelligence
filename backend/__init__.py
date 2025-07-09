"""
GlobalMind FL: Core Package
Federated Learning for Multilingual AI Search Intelligence
"""

__version__ = "1.0.0"
__author__ = "GlobalMind FL Team"
__description__ = "Privacy-preserving multilingual AI search for Indian languages"

from .core.federated_coordinator import FederatedCoordinator
from .language_nodes.base_node import BaseLanguageNode
from .cultural_context.context_engine import CulturalContextEngine

__all__ = [
    "FederatedCoordinator",
    "BaseLanguageNode", 
    "CulturalContextEngine"
]
