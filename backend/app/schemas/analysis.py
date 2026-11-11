"""Pydantic schemas for paper comparison and research gaps."""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PaperAspect(BaseModel):
    paper_id: str
    paper_title: str
    methodology: str = ""
    datasets: str = ""
    metrics: str = ""
    findings: str = ""
    limitations: str = ""

class ComparisonMatrix(BaseModel):
    aspects: List[str] = ["Methodology", "Datasets and metrics", "Findings", "Limitations"]
    papers: List[PaperAspect] = Field(default_factory=list)

class ResearchGap(BaseModel):
    area: str = Field(..., description="Topical or methodological area")
    description: str = Field(..., description="Explanation of the gap or unresolved issue")
    potential_direction: str = Field(..., description="Suggested future work or experiment")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    supporting_citations: List[str] = Field(default_factory=list)
