"""API route contracts for research paper ingestion and listing."""
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from backend.app.schemas.paper import PaperUploadResponse, PaperListItem

router = APIRouter(prefix="/papers", tags=["Papers"])

# In-memory mock storage for initial contract verification
_PAPERS_REGISTRY: List[PaperListItem] = []

@router.get("", response_model=List[PaperListItem])
async def list_papers():
    """List all processed papers stored in the system."""
    return _PAPERS_REGISTRY

@router.post("/upload", response_model=PaperUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_paper(file: UploadFile = File(...)):
    """Upload research paper PDF for parsing, chunking, and indexing."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported."
        )
    
    paper_id = f"paper-{len(_PAPERS_REGISTRY) + 1}"
    item = PaperListItem(
        id=paper_id,
        title=file.filename.replace(".pdf", ""),
        filename=file.filename,
        total_pages=1,
        chunk_count=0
    )
    _PAPERS_REGISTRY.append(item)
    
    return PaperUploadResponse(
        id=paper_id,
        filename=file.filename,
        status="processed",
        message="Paper received and queued for indexing",
        total_pages=1
    )
