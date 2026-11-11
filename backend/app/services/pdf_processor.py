"""PyMuPDF extraction and section- and page-aware chunking."""
import re
import hashlib
from typing import List, Dict, Any, Optional
import fitz  # PyMuPDF
from backend.app.schemas.paper import ChunkSchema, PaperMetadata

class PDFProcessor:
    def __init__(self):
        self.section_patterns = [
            r"^(?:[0-9IVX]+\.?\s*)?(abstract|introduction|related work|background|methodology|methods|system architecture|model architecture|experiments|experimental setup|results|discussion|conclusion|limitations|future work|references)",
        ]

    def extract_document(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Extract text blocks, font sizes, headings, and page mapping from PDF bytes."""
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        total_pages = len(doc)
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        extracted_sections: List[Dict[str, Any]] = []
        current_section = "Abstract"
        
        for page_idx in range(total_pages):
            page_num = page_idx + 1
            page = doc[page_idx]
            blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type)
            
            for b in blocks:
                if b[6] == 0:  # Text block
                    text = b[4].strip()
                    if not text:
                        continue
                    
                    # Detect section heading
                    lines = text.split("\n")
                    first_line = lines[0].strip().lower()
                    for pattern in self.section_patterns:
                        match = re.search(pattern, first_line, re.IGNORECASE)
                        if match:
                            current_section = match.group(1).title()
                            break
                    
                    extracted_sections.append({
                        "section": current_section,
                        "page": page_num,
                        "text": text
                    })
                    
        metadata = PaperMetadata(
            title=doc.metadata.get("title") or filename.replace(".pdf", ""),
            authors=[doc.metadata.get("author")] if doc.metadata.get("author") else [],
            year=None,
            abstract="",
            total_pages=total_pages,
            file_name=filename,
            file_hash=file_hash
        )
        return {"metadata": metadata, "sections": extracted_sections}

    def chunk_sections(
        self,
        paper_id: str,
        sections: List[Dict[str, Any]],
        chunk_size: int = 600,
        chunk_overlap: int = 100
    ) -> List[ChunkSchema]:
        """Split text within section boundaries while preserving page numbers."""
        chunks: List[ChunkSchema] = []
        chunk_idx = 0
        
        for sec in sections:
            section_title = sec["section"]
            page_num = sec["page"]
            text = sec["text"]
            
            # Simple word-based chunking with overlap
            words = text.split()
            if not words:
                continue
            
            start = 0
            while start < len(words):
                end = min(start + chunk_size, len(words))
                chunk_words = words[start:end]
                chunk_content = " ".join(chunk_words)
                
                chunks.append(
                    ChunkSchema(
                        id=f"{paper_id}-c{chunk_idx}",
                        paper_id=paper_id,
                        chunk_index=chunk_idx,
                        page_number=page_num,
                        section_title=section_title,
                        content=chunk_content,
                        token_count=len(chunk_words)
                    )
                )
                chunk_idx += 1
                if end == len(words):
                    break
                start += max(1, chunk_size - chunk_overlap)
                
        return chunks
