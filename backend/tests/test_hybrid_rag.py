import pytest
from backend.app.rag.bm25_search import BM25SearchEngine
from backend.app.rag.reranker import CrossEncoderReranker
from backend.app.rag.hybrid_retriever import HybridRetriever

def test_bm25_search():
    engine = BM25SearchEngine()
    chunks = [
        {"chunk_id": "c1", "content": "Operating margin declined due to wage hikes in Europe.", "company_id": 1, "fiscal_year": 2024, "page_number": 12, "section": "MD&A"},
        {"chunk_id": "c2", "content": "Renewable energy reached fifty percent of total consumption.", "company_id": 1, "fiscal_year": 2024, "page_number": 45, "section": "ESG"},
        {"chunk_id": "c3", "content": "The company completed acquisitions in cloud data engineering.", "company_id": 2, "fiscal_year": 2024, "page_number": 8, "section": "Strategy"}
    ]
    engine.index_chunks(chunks)

    results = engine.search(query="wage hikes operating margin", company_id=1, top_k=2)
    assert len(results) > 0
    assert results[0]["chunk_id"] == "c1"

def test_cross_encoder_reranker():
    candidates = [
        {"chunk_id": "c1", "content": "General corporate overview and history of the group.", "section": "General", "rrf_score": 0.015},
        {"chunk_id": "c2", "content": "Why did operating margin decline? Compensation revisions and talent costs compressed margins by 50 basis points.", "section": "Management Discussion & Analysis", "rrf_score": 0.012}
    ]

    reranked = CrossEncoderReranker.rerank(
        query="operating margin decline reason",
        candidates=candidates,
        top_k=2
    )
    assert len(reranked) == 2
    # c2 contains exact query terms and matching section, so it should rank first
    assert reranked[0]["chunk_id"] == "c2"
    assert reranked[0]["rerank_score"] > reranked[1]["rerank_score"]
