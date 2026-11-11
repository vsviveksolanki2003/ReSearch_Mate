"""Hybrid Retrieval service combining dense semantic search and lexical matching."""
import time
import re
from typing import List, Dict, Any, Optional
from backend.app.schemas.paper import ChunkSchema
from backend.app.services.embeddings import EmbeddingService
from backend.app.services.reranker import CrossEncoderReranker

class HybridRetriever:
    def __init__(self, embedding_service: Optional[EmbeddingService] = None, reranker: Optional[CrossEncoderReranker] = None):
        self.embedding_service = embedding_service or EmbeddingService()
        self.reranker = reranker or CrossEncoderReranker()
        self._chunks: Dict[str, ChunkSchema] = {}
        self._vectors: Dict[str, List[float]] = {}

    def index_chunks(self, chunks: List[ChunkSchema]):
        """Index chunks with dense embeddings."""
        for chunk in chunks:
            self._chunks[chunk.id] = chunk
            vec = self.embedding_service.embed_query(chunk.content)
            self._vectors[chunk.id] = vec

    def clear(self):
        self._chunks.clear()
        self._vectors.clear()

    def _lexical_score(self, query: str, content: str) -> float:
        """Token-overlap lexical score."""
        q_tokens = set(re.findall(r"\w+", query.lower()))
        if not q_tokens:
            return 0.0
        doc_tokens = set(re.findall(r"\w+", content.lower()))
        matches = q_tokens.intersection(doc_tokens)
        return len(matches) / len(q_tokens)

    def retrieve(
        self,
        query: str,
        paper_ids: Optional[List[str]] = None,
        top_k: int = 5,
        dense_weight: float = 0.7,
        lexical_weight: float = 0.3
    ) -> List[Dict[str, Any]]:
        """Retrieve top_k chunks scored by hybrid combination of dense and lexical search."""
        if not self._chunks:
            return []

        query_vec = self.embedding_service.embed_query(query)
        scored_results: List[Dict[str, Any]] = []

        for chunk_id, chunk in self._chunks.items():
            # Paper ID filter
            if paper_ids and chunk.paper_id not in paper_ids:
                continue

            # Dense similarity
            chunk_vec = self._vectors.get(chunk_id)
            if chunk_vec:
                dense_score = self.embedding_service.cosine_similarity(query_vec, chunk_vec)
            else:
                dense_score = 0.0

            # Lexical score
            lexical_score = self._lexical_score(query, chunk.content)

            combined_score = (dense_weight * dense_score) + (lexical_weight * lexical_score)
            scored_results.append({
                "chunk": chunk,
                "score": combined_score,
                "dense_score": dense_score,
                "lexical_score": lexical_score
            })

        # Rank by initial hybrid score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        candidates = [item["chunk"] for item in scored_results[:top_k * 3]]
        
        # 2nd stage Cross-Encoder Reranking
        if candidates and self.reranker:
            reranked_chunks = self.reranker.rerank(query=query, candidates=candidates, top_k=top_k)
            # Map back to result structure
            final_results = []
            chunk_map = {item["chunk"].id: item for item in scored_results}
            for c in reranked_chunks:
                if c.id in chunk_map:
                    final_results.append(chunk_map[c.id])
            return final_results

        return scored_results[:top_k]

    def benchmark(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """Benchmark retrieval latency and return metrics."""
        start = time.perf_counter()
        results = self.retrieve(query=query, top_k=top_k)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        return {
            "query": query,
            "top_k": top_k,
            "retrieved_count": len(results),
            "latency_ms": round(elapsed_ms, 3),
            "top_score": results[0]["score"] if results else 0.0
        }

