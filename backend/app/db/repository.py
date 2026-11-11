"""Repository for papers, chunks, and vector store operations."""
import uuid
from typing import List, Optional, Dict, Any
from backend.app.schemas.paper import PaperMetadata, ChunkSchema, PaperListItem

class PaperRepository:
    def __init__(self):
        self._papers: Dict[str, Dict[str, Any]] = {}
        self._chunks: Dict[str, List[Dict[str, Any]]] = {}

    def save_paper(self, metadata: PaperMetadata) -> str:
        """Persist paper metadata and return generated unique paper_id."""
        paper_id = f"paper-{uuid.uuid4().hex[:8]}"
        self._papers[paper_id] = {
            "id": paper_id,
            "title": metadata.title,
            "authors": metadata.authors,
            "year": metadata.year,
            "abstract": metadata.abstract,
            "total_pages": metadata.total_pages,
            "file_name": metadata.file_name,
            "file_hash": metadata.file_hash,
            "chunk_count": 0
        }
        self._chunks[paper_id] = []
        return paper_id

    def get_paper(self, paper_id: str) -> Optional[PaperMetadata]:
        """Retrieve paper metadata by ID."""
        data = self._papers.get(paper_id)
        if not data:
            return None
        return PaperMetadata(
            title=data["title"],
            authors=data["authors"],
            year=data["year"],
            abstract=data["abstract"],
            total_pages=data["total_pages"],
            file_name=data["file_name"],
            file_hash=data["file_hash"]
        )

    def list_papers(self) -> List[PaperListItem]:
        """List all indexed papers."""
        results: List[PaperListItem] = []
        for p in self._papers.values():
            results.append(
                PaperListItem(
                    id=p["id"],
                    title=p["title"],
                    filename=p["file_name"],
                    total_pages=p["total_pages"],
                    chunk_count=p["chunk_count"]
                )
            )
        return results

    def save_chunks(self, paper_id: str, chunks: List[ChunkSchema], embeddings: Optional[List[List[float]]] = None):
        """Save chunk text and vector embeddings."""
        if paper_id not in self._papers:
            raise ValueError(f"Paper {paper_id} does not exist.")

        stored = []
        for idx, c in enumerate(chunks):
            emb = embeddings[idx] if (embeddings and idx < len(embeddings)) else None
            stored.append({
                "chunk": c,
                "embedding": emb
            })
        self._chunks[paper_id] = stored
        self._papers[paper_id]["chunk_count"] = len(chunks)

    def get_chunks_for_paper(self, paper_id: str) -> List[ChunkSchema]:
        """Get all chunks for a given paper."""
        items = self._chunks.get(paper_id, [])
        return [item["chunk"] for item in items]

    def get_all_chunks(self, paper_ids: Optional[List[str]] = None) -> List[ChunkSchema]:
        """Retrieve all chunks optionally filtered by paper IDs."""
        all_chunks: List[ChunkSchema] = []
        target_ids = paper_ids if paper_ids else list(self._chunks.keys())
        for pid in target_ids:
            for item in self._chunks.get(pid, []):
                all_chunks.append(item["chunk"])
        return all_chunks
