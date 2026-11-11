"""Pydantic schemas for chat queries, SSE streaming events, and responses."""
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from backend.app.schemas.citation import Citation
from backend.app.schemas.analysis import ComparisonMatrix, ResearchGap

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Researcher natural language query")
    paper_ids: List[str] = Field(default_factory=list, description="Target paper IDs to scope retrieval")
    stream: bool = Field(default=True, description="Whether to stream response tokens via SSE")
    top_k: int = Field(default=5, ge=1, le=20, description="Top evidence chunks to retrieve")

class StreamEvent(BaseModel):
    event: str = Field(..., description="Event type: token, agent_status, citation, gap, done, error")
    data: Any = Field(..., description="Payload associated with event")

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    research_gaps: List[ResearchGap] = Field(default_factory=list)
    comparison_matrix: Optional[ComparisonMatrix] = None
