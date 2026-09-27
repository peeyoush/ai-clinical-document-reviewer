from pydantic import BaseModel
from app.schemas.analysis import AnalyzeRequest, ClinicalReport


class HealthStatus(BaseModel):
    status: str


__all__ = ["HealthStatus", "AnalyzeRequest", "ClinicalReport"]
