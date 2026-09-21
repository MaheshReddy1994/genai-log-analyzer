from pydantic import BaseModel

class LogAnalysis(BaseModel):
    root_cause: str
    category: str
    confidence_level: str
    evidence: str