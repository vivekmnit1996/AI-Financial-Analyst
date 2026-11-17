import re
from typing import List, Dict, Any

class CrossEncoderReranker:
    """
    Reranks candidate chunks using cross-attention relevance / query-context scoring.
    Combines neural cross-encoder with exact term proximity and financial section weighting.
    """

    _neural_reranker = None
    _tried_loading = False

    @classmethod
    def get_neural_reranker(cls):
        if not cls._tried_loading:
            cls._tried_loading = True
            try:
                from fastembed.rerank.cross_encoder import TextCrossEncoder
                cls._neural_reranker = TextCrossEncoder(model_name="BAAI/bge-reranker-base")
            except Exception as e:
                print(f"[Reranker] Neural Cross-Encoder not active: {e}. Using deterministic feature reranker.")
                cls._neural_reranker = None
        return cls._neural_reranker

    @classmethod
    def rerank(
        cls,
        query: str,
        candidates: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Reranks retrieved candidate chunks based on query-content relevance.
        """
        if not candidates:
            return []

        neural = cls.get_neural_reranker()
        if neural is not None:
            try:
                passages = [c["content"] for c in candidates]
                scores_gen = neural.rerank(query, passages)
                for c, score in zip(candidates, scores_gen):
                    c["rerank_score"] = round(float(score), 4)
                candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
                return candidates[:top_k]
            except Exception as e:
                print(f"[Reranker] Error in neural reranking: {e}. Falling back to analytical reranker.")

        # Analytical Reranker: Entity Density, Term Proximity, and Section Alignment
        query_terms = re.findall(r"\b[A-Za-z0-9_-]+\b", query.lower())
        q_text = " ".join(query_terms)

        for chunk in candidates:
            content = chunk.get("content", "").lower()
            section = chunk.get("section", "").lower()
            rrf_score = chunk.get("rrf_score", 0.0)

            score = rrf_score * 10.0  # base from hybrid retrieval

            # 1. Exact phrase match boost
            if q_text and q_text in content:
                score += 5.0

            # 2. Term coverage & density
            matched_terms = sum(1 for term in query_terms if term in content)
            term_ratio = matched_terms / max(len(query_terms), 1)
            score += term_ratio * 4.0

            # 3. Section alignment boost
            if "margin" in query.lower() or "profit" in query.lower():
                if "management discussion" in section or "profit & loss" in section:
                    score += 2.0
            if "esg" in query.lower() or "emission" in query.lower() or "water" in query.lower():
                if "sustainability" in section or "esg" in section or "governance" in section:
                    score += 2.5
            if "risk" in query.lower():
                if "risk management" in section:
                    score += 2.5

            chunk["rerank_score"] = round(float(score), 4)

        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        return candidates[:top_k]
