import re
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi

class BM25SearchEngine:
    """
    Keyword-based BM25 retrieval engine for exact financial terms, metrics, and entity queries.
    """

    def __init__(self):
        self.corpus_chunks: List[Dict[str, Any]] = []
        self.tokenized_corpus: List[List[str]] = []
        self.bm25_model: Optional[BM25Okapi] = None

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple tokenizer that handles lowercase, alphanumeric tokens, and financial acronyms."""
        tokens = re.findall(r"\b[A-Za-z0-9_-]+\b", text.lower())
        return tokens

    def index_chunks(self, chunks: List[Dict[str, Any]]):
        """Build or update the BM25 index with candidate chunks."""
        self.corpus_chunks = chunks
        self.tokenized_corpus = [self.tokenize(c["content"]) for c in chunks]
        if self.tokenized_corpus:
            self.bm25_model = BM25Okapi(self.tokenized_corpus)
        else:
            self.bm25_model = None

    def search(
        self,
        query: str,
        company_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Execute BM25 keyword search with metadata filtering.
        """
        if not self.bm25_model or not self.corpus_chunks:
            return []

        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        doc_scores = self.bm25_model.get_scores(query_tokens)
        
        candidates = []
        for idx, score in enumerate(doc_scores):
            if score <= 0.0:
                continue
            chunk = self.corpus_chunks[idx]

            # Metadata filtering
            if company_id is not None and chunk.get("company_id") != company_id:
                continue
            if fiscal_year is not None and chunk.get("fiscal_year") != fiscal_year:
                continue

            candidates.append({
                "chunk_id": chunk.get("chunk_id"),
                "document_id": chunk.get("document_id"),
                "company_id": chunk.get("company_id"),
                "company_name": chunk.get("company_name"),
                "fiscal_year": chunk.get("fiscal_year"),
                "document_title": chunk.get("document_title"),
                "document_type": chunk.get("document_type"),
                "page_number": chunk.get("page_number"),
                "section": chunk.get("section"),
                "content": chunk.get("content"),
                "is_table": chunk.get("is_table"),
                "bm25_score": float(score)
            })

        # Sort descending by bm25_score
        candidates.sort(key=lambda x: x["bm25_score"], reverse=True)
        return candidates[:top_k]
