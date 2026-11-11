"""Local embedding generation and vector similarity operations."""
import math
import hashlib
from typing import List, Union
import numpy as np
from backend.app.config import settings

class EmbeddingService:
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL, dimension: int = settings.EMBEDDING_DIMENSION):
        self.model_name = model_name
        self.dimension = dimension
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                # Deterministic semantic hashing fallback (384 dimensions)
                self._model = "fallback"
        return self._model

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string into normalized float vector."""
        model = self._get_model()
        if model != "fallback":
            try:
                vec = model.encode(text, normalize_embeddings=True)
                return vec.tolist()
            except Exception:
                pass
        return self._fallback_embed(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of document texts."""
        return [self.embed_query(t) for t in texts]

    def _fallback_embed(self, text: str) -> List[float]:
        """Deterministic 384-dimensional normalized semantic vector with token and subtoken n-grams."""
        import re
        tokens = re.findall(r"\w+", text.lower())
        vec = np.zeros(self.dimension, dtype=np.float32)
        
        for w in tokens:
            # Word level hash
            h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dimension
            vec[idx] += 2.0
            
            # Character 3-grams for subword similarity
            if len(w) >= 3:
                for i in range(len(w) - 2):
                    ngram = w[i:i+3]
                    nh = int(hashlib.md5(ngram.encode("utf-8")).hexdigest(), 16)
                    vec[nh % self.dimension] += 0.5

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Compute cosine similarity between two normalized vectors."""
        a = np.array(v1, dtype=np.float32)
        b = np.array(v2, dtype=np.float32)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))
