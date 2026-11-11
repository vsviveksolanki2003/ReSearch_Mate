"""Citation Verifier Agent: Validates claim grounding against source chunks and page numbers."""
import re
from typing import List, Dict, Any, Optional
from backend.app.schemas.paper import ChunkSchema
from backend.app.schemas.citation import Citation, CitationVerificationResult

class CitationVerifier:
    def __init__(self, min_quote_overlap: float = 0.75):
        self.min_quote_overlap = min_quote_overlap

    def verify_claim(self, claim: Dict[str, Any], source_chunks: List[ChunkSchema]) -> CitationVerificationResult:
        """
        Verify that a claim has supporting evidence in source chunks.
        claim dict expected keys:
          - text: the claim statement
          - quote: verbatim or near-verbatim quote from paper
          - page_number: cited page number
          - paper_id: cited paper ID
        """
        claim_text = claim.get("text", "")
        quote = claim.get("quote", "").strip()
        page_num = claim.get("page_number")
        paper_id = claim.get("paper_id")

        if not quote or not page_num or not paper_id:
            return CitationVerificationResult(
                claim=claim_text,
                is_grounded=False,
                rejection_reason="Missing quote, page number, or paper ID"
            )

        # Find matching chunk
        for chunk in source_chunks:
            if chunk.paper_id == paper_id and chunk.page_number == page_num:
                # Check quote overlap
                chunk_text_clean = chunk.content.lower()
                quote_clean = quote.lower()
                
                if quote_clean in chunk_text_clean:
                    citation = Citation(
                        paper_id=chunk.paper_id,
                        paper_title=getattr(chunk, "section_title", "Source Document"),
                        page_number=chunk.page_number,
                        quote=quote,
                        confidence=1.0,
                        verified=True
                    )
                    return CitationVerificationResult(
                        claim=claim_text,
                        is_grounded=True,
                        citation=citation
                    )
                
                # Check token set overlap
                quote_tokens = set(re.findall(r"\w+", quote_clean))
                chunk_tokens = set(re.findall(r"\w+", chunk_text_clean))
                if quote_tokens and (len(quote_tokens.intersection(chunk_tokens)) / len(quote_tokens)) >= self.min_quote_overlap:
                    citation = Citation(
                        paper_id=chunk.paper_id,
                        paper_title=getattr(chunk, "section_title", "Source Document"),
                        page_number=chunk.page_number,
                        quote=quote,
                        confidence=0.85,
                        verified=True
                    )
                    return CitationVerificationResult(
                        claim=claim_text,
                        is_grounded=True,
                        citation=citation
                    )

        return CitationVerificationResult(
            claim=claim_text,
            is_grounded=False,
            rejection_reason=f"Quote not substantiated on page {page_num} of paper {paper_id}"
        )

    def filter_and_ground_response(
        self,
        claims: List[Dict[str, Any]],
        source_chunks: List[ChunkSchema]
    ) -> List[Citation]:
        """Filter out hallucinated claims and return only verified citations."""
        verified_citations: List[Citation] = []
        for claim in claims:
            res = self.verify_claim(claim, source_chunks)
            if res.is_grounded and res.citation:
                verified_citations.append(res.citation)
        return verified_citations
