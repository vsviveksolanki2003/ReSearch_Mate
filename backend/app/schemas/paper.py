"""Pydantic schemas for research papers and document ingestion."""
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field

class PaperMetadata(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the research paper")
    authors: List[str] = Field(default_factory=list, description="Authors of the paper")
    year: Optional[int] = Field(default=None, description="Publication year")
    abstract: Optional[str] = Field(default=None, description="Abstract summary")
    total_pages: int = Field(..., ge=1, description="Total number of pages in the PDF")
    file_name: str = Field(..., min_length=1, description="Original filename")
    file_hash: str = Field(..., min_length=1, description="SHA-256 hash for deduplication")

class ChunkSchema(BaseModel):
    id: str
    paper_id: str
    chunk_index: int
    page_number: int
    section_title: str
    content: str
    token_count: Optional[int] = None

class PaperUploadResponse(BaseModel):
    id: str
    filename: str
    status: str
    message: str
    total_pages: int
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaperListItem(BaseModel):
    id: str
    title: str
    filename: str
    total_pages: int
    chunk_count: int = 0
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
