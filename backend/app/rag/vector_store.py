import os
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from backend.app.config import settings

class VectorStoreManager:
    """
    Manages Qdrant vector database interactions, collection lifecycles,
    dense embedding generation, and vector retrieval.
    """

    _instance = None
    _client = None
    _embedder = None
    VECTOR_DIM = 384  # Default for bge-small / all-MiniLM

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._client is None:
            if settings.QDRANT_MODE == "server":
                try:
                    cls._client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
                    cls._client.get_collections()
                except Exception:
                    try:
                        cls._client = QdrantClient(path=settings.QDRANT_PATH)
                    except Exception:
                        cls._client = QdrantClient(location=":memory:")
            else:
                try:
                    cls._client = QdrantClient(path=settings.QDRANT_PATH)
                except Exception as e:
                    print(f"[VectorStore] Storage path locked or inaccessible ({e}). Falling back to in-memory Qdrant instance.")
                    cls._client = QdrantClient(location=":memory:")
        return cls._client

    @classmethod
    def get_embedder(cls):
        """
        Initializes fastembed ONNX embedding model.
        Falls back to deterministic normalized pseudo-embeddings if offline/download restricted.
        """
        if cls._embedder is None:
            try:
                from fastembed import TextEmbedding
                cls._embedder = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            except Exception as e:
                print(f"[VectorStore] Notice: Fastembed download failed or offline ({e}). Using deterministic embedding fallback.")
                cls._embedder = "FALLBACK"
        return cls._embedder

    @classmethod
    def generate_embeddings(cls, texts: List[str]) -> List[List[float]]:
        embedder = cls.get_embedder()
        if embedder != "FALLBACK":
            try:
                embeddings_gen = embedder.embed(texts)
                return [emb.tolist() for emb in embeddings_gen]
            except Exception as e:
                print(f"[VectorStore] Embedding generation error: {e}. Falling back.")
        
        # Deterministic semantic hash projection (384-dimensional normalized vector)
        results = []
        for text in texts:
            words = text.lower().split()
            vec = np.zeros(cls.VECTOR_DIM, dtype=np.float32)
            for w in words:
                h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
                idx = h % cls.VECTOR_DIM
                sign = 1.0 if (h >> 1) % 2 == 0 else -1.0
                vec[idx] += sign
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            results.append(vec.tolist())
        return results

    @classmethod
    def ensure_collection(cls):
        client = cls.get_client()
        collections = [col.name for col in client.get_collections().collections]
        if settings.QDRANT_COLLECTION not in collections:
            client.create_collection(
                collection_name=settings.QDRANT_COLLECTION,
                vectors_config=qmodels.VectorParams(
                    size=cls.VECTOR_DIM,
                    distance=qmodels.Distance.COSINE
                )
            )

    @classmethod
    def upsert_chunks(cls, chunks: List[Dict[str, Any]]) -> int:
        if not chunks:
            return 0

        cls.ensure_collection()
        client = cls.get_client()

        texts = [chunk["content"] for chunk in chunks]
        embeddings = cls.generate_embeddings(texts)

        points = []
        for idx, (chunk, vector) in enumerate(zip(chunks, embeddings)):
            point_id = int(hashlib.md5(chunk["chunk_id"].encode("utf-8")).hexdigest()[:15], 16)
            payload = {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "company_id": chunk["company_id"],
                "company_name": chunk.get("company_name", ""),
                "fiscal_year": chunk.get("fiscal_year"),
                "document_title": chunk.get("document_title", ""),
                "document_type": chunk.get("document_type", ""),
                "page_number": chunk["page_number"],
                "section": chunk["section"],
                "content": chunk["content"],
                "is_table": chunk.get("is_table", False),
            }
            points.append(
                qmodels.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            )

        client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points
        )
        return len(points)

    @classmethod
    def dense_search(
        cls,
        query: str,
        company_id: Optional[int] = None,
        fiscal_year: Optional[int] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Executes dense cosine similarity search in Qdrant with optional metadata filtering.
        """
        cls.ensure_collection()
        client = cls.get_client()

        query_vectors = cls.generate_embeddings([query])
        query_vector = query_vectors[0]

        # Build filter conditions
        must_conditions = []
        if company_id is not None:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="company_id",
                    match=qmodels.MatchValue(value=company_id)
                )
            )
        if fiscal_year is not None:
            must_conditions.append(
                qmodels.FieldCondition(
                    key="fiscal_year",
                    match=qmodels.MatchValue(value=fiscal_year)
                )
            )

        query_filter = qmodels.Filter(must=must_conditions) if must_conditions else None

        results = client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k
        )

        hits = []
        for point in results.points:
            hits.append({
                "chunk_id": point.payload.get("chunk_id"),
                "document_id": point.payload.get("document_id"),
                "company_id": point.payload.get("company_id"),
                "company_name": point.payload.get("company_name"),
                "fiscal_year": point.payload.get("fiscal_year"),
                "document_title": point.payload.get("document_title"),
                "document_type": point.payload.get("document_type"),
                "page_number": point.payload.get("page_number"),
                "section": point.payload.get("section"),
                "content": point.payload.get("content"),
                "is_table": point.payload.get("is_table"),
                "dense_score": float(point.score)
            })

        return hits
