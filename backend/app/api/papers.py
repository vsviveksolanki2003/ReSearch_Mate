"""API routes for research paper ingestion and document management."""
import uuid
from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from backend.app.schemas.paper import PaperUploadResponse, PaperListItem, ChunkSchema
from backend.app.services.pdf_processor import PDFProcessor
from backend.app.services.retriever import HybridRetriever

router = APIRouter(prefix="/papers", tags=["Papers"])

pdf_processor = PDFProcessor()
retriever_instance = HybridRetriever()

_PAPERS_STORE: List[PaperListItem] = []

def get_retriever() -> HybridRetriever:
    return retriever_instance

@router.get("", response_model=List[PaperListItem])
async def list_papers():
    """List all processed papers stored in the system."""
    return _PAPERS_STORE

@router.post("/upload", response_model=PaperUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_paper(file: UploadFile = File(...)):
    """Upload research paper PDF, extract sections, chunk text, and index in vector store."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF documents are supported."
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    paper_id = f"paper-{uuid.uuid4().hex[:8]}"

    try:
        extracted = pdf_processor.extract_document(file_bytes, file.filename)
        chunks = pdf_processor.chunk_sections(
            paper_id=paper_id,
            sections=extracted["sections"]
        )
        # Index in hybrid retriever
        retriever_instance.index_chunks(chunks)

        item = PaperListItem(
            id=paper_id,
            title=extracted["metadata"].title,
            filename=file.filename,
            total_pages=extracted["metadata"].total_pages,
            chunk_count=len(chunks)
        )
        _PAPERS_STORE.append(item)

        return PaperUploadResponse(
            id=paper_id,
            filename=file.filename,
            status="processed",
            message=f"Paper processed: {len(chunks)} chunks indexed across {extracted['metadata'].total_pages} pages.",
            total_pages=extracted["metadata"].total_pages
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process PDF: {str(e)}"
        )
