"""
Models module for ContractAI.

Import all models here to make them available from the models module.
"""

from ContractAI.app.models.user import User
from ContractAI.app.models.document import (
    Document,
    DocumentStatus,
    DocumentAnalysis,
    Clause,
    ClauseRisk,
    RiskLevel
)

# Add more model imports here as needed
