from typing import List, Dict, Any, Optional
from backend.app.config import settings
from backend.app.rag.vector_store import VectorStoreManager
from backend.app.rag.bm25_search import BM25SearchEngine
from backend.app.rag.reranker import CrossEncoderReranker

class HybridRetriever:
    """
    Hybrid Retrieval Engine combining Qdrant Dense Vector Search,
    BM25 Keyword Search, Reciprocal Rank Fusion (RRF), and Cross-Encoder Reranking.
    """

    def __init__(self, bm25_engine: BM25SearchEngine):
        self.bm25 = bm25_engine

    def retrieve(
        self,
        query: str,
        company_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        dense_top_k: int = 10,
        bm25_top_k: int = 10,
        final_top_k: int = 5,
        enable_reranking: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Executes the full Hybrid RAG retrieval pipeline:
        1. Dense Vector Search (Qdrant)
        2. BM25 Keyword Search
        3. Reciprocal Rank Fusion (RRF)
        4. Cross-Encoder Reranker
        """
        # 1. Dense retrieval
        dense_hits = []
        try:
            dense_hits = VectorStoreManager.dense_search(
                query=query,
                company_id=company_id,
                fiscal_year=fiscal_year,
                top_k=dense_top_k
            )
        except Exception as e:
            print(f"[HybridRetriever] Dense search error: {e}")

        # 2. BM25 retrieval
        bm25_hits = self.bm25.search(
            query=query,
            company_id=company_id,
            fiscal_year=fiscal_year,
            top_k=bm25_top_k
        )

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_k = settings.RRF_K  # 60
        fused_candidates: Dict[str, Dict[str, Any]] = {}

        # Process dense hits
        for rank, hit in enumerate(dense_hits):
            cid = hit["chunk_id"]
            rrf_score = 1.0 / (rrf_k + (rank + 1))
            if cid not in fused_candidates:
                fused_candidates[cid] = {**hit, "rrf_score": rrf_score, "dense_rank": rank + 1, "bm25_rank": None}
            else:
                fused_candidates[cid]["rrf_score"] += rrf_score
                fused_candidates[cid]["dense_rank"] = rank + 1

        # Process BM25 hits
        for rank, hit in enumerate(bm25_hits):
            cid = hit["chunk_id"]
            rrf_score = 1.0 / (rrf_k + (rank + 1))
            if cid not in fused_candidates:
                fused_candidates[cid] = {**hit, "rrf_score": rrf_score, "dense_rank": None, "bm25_rank": rank + 1}
            else:
                fused_candidates[cid]["rrf_score"] += rrf_score
                fused_candidates[cid]["bm25_rank"] = rank + 1

        candidate_list = list(fused_candidates.values())
        if not candidate_list:
            return []

        # Sort by RRF score descending
        candidate_list.sort(key=lambda x: x["rrf_score"], reverse=True)

        # 4. Cross-Encoder Reranking
        if enable_reranking:
            # Take top 10 candidates for reranking
            rerank_candidates = candidate_list[:10]
            final_hits = CrossEncoderReranker.rerank(
                query=query,
                candidates=rerank_candidates,
                top_k=final_top_k
            )
        else:
            final_hits = candidate_list[:final_top_k]

        return final_hits
