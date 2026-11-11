"""Cross-Encoder Reranker for fine-grained semantic relevance scoring."""
import re
from typing import List, Tuple
from backend.app.schemas.paper import ChunkSchema

class CrossEncoderReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
                self._model = CrossEncoder(self.model_name)
            except Exception:
                self._model = "fallback"
        return self._model

    def compute_pair_score(self, query: str, passage: str) -> float:
        """Compute relevance score between query and passage."""
        model = self._get_model()
        if model != "fallback":
            try:
                score = model.predict([(query, passage)])[0]
                return float(score)
            except Exception:
                pass
        return self._heuristic_cross_score(query, passage)

    def _heuristic_cross_score(self, query: str, passage: str) -> float:
        """Deterministic cross-attention heuristic scoring word co-occurrences, n-grams, and proximity."""
        q_words = re.findall(r"\w+", query.lower())
        p_words = re.findall(r"\w+", passage.lower())
        if not q_words or not p_words:
            return 0.0

        q_set = set(q_words)
        p_set = set(p_words)
        overlap = len(q_set.intersection(p_set))
        coverage = overlap / len(q_set)

        # Bigram match bonus
        q_bigrams = set(zip(q_words[:-1], q_words[1:]))
        p_bigrams = set(zip(p_words[:-1], p_words[1:]))
        bigram_overlap = len(q_bigrams.intersection(p_bigrams)) if q_bigrams else 0
        bigram_bonus = (bigram_overlap / len(q_bigrams)) if q_bigrams else 0.0

        # Exact phrase match bonus
        exact_bonus = 1.0 if query.lower() in passage.lower() else 0.0

        return (coverage * 0.6) + (bigram_bonus * 0.25) + (exact_bonus * 0.15)

    def rerank(self, query: str, candidates: List[ChunkSchema], top_k: int = 5) -> List[ChunkSchema]:
        """Rerank candidate chunks according to query-passage cross-attention scores."""
        if not candidates:
            return []

        scored_candidates: List[Tuple[float, ChunkSchema]] = []
        for c in candidates:
            score = self.compute_pair_score(query, c.content)
            scored_candidates.append((score, c))

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored_candidates[:top_k]]
