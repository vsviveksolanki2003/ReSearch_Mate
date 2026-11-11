"""Pydantic schemas for citation grounding and verification."""
from typing import Optional
from pydantic import BaseModel, Field

class Citation(BaseModel):
    paper_id: str
    paper_title: str
    page_number: int = Field(..., ge=1)
    quote: str = Field(..., min_length=1)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    verified: bool = True

class CitationVerificationResult(BaseModel):
    claim: str
    is_grounded: bool
    citation: Optional[Citation] = None
    rejection_reason: Optional[str] = None
