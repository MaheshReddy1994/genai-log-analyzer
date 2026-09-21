from enum import Enum
from pydantic import BaseModel


class LogCategory(str, Enum):
    ACCOUNT = "ACCOUNT"
    PERMISSION = "PERMISSION"
    NETWORK = "NETWORK"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    OTHER = "OTHER"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class LogAnalysis(BaseModel):
    root_cause: str
    category: LogCategory
    confidence_level: ConfidenceLevel
    evidence: str