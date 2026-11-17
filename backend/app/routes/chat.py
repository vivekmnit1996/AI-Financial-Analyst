import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.schema_models import (
    Company, FinancialData, ESGData, DocumentChunk, QueryHistory
)
from backend.app.schemas.pydantic_schemas import QueryRequest, QueryResponse
from backend.app.engine.financial_calculator import FinancialCalculatorEngine
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.rag.bm25_search import BM25SearchEngine
from backend.app.rag.hybrid_retriever import HybridRetriever
from backend.app.rag.llm_service import LLMService

router = APIRouter(prefix="/chat", tags=["AI Financial Analyst Chat & RAG"])

@router.post("/query", response_model=QueryResponse)
def query_ai_analyst(payload: QueryRequest, db: Session = Depends(get_db)):
    """
    Hybrid RAG + Deterministic Analysis Query Endpoint.
    Combines verified financial calculations, transparent ESG evaluations,
    and hybrid document retrieval with cross-encoder reranking and citations.
    """
    comp = None
    if payload.company_id:
        comp = db.query(Company).filter(Company.id == payload.company_id).first()

    # 1. Fetch and calculate deterministic financial metrics
    metrics_summary = None
    if comp:
        fin_records = db.query(FinancialData).filter(
            FinancialData.company_id == comp.id
        ).order_by(FinancialData.fiscal_year.asc()).all()

        if fin_records:
            ratios = FinancialCalculatorEngine.compute_ratios_for_records(fin_records)
            insights = FinancialCalculatorEngine.generate_analytical_insights(ratios)
            metrics_summary = {
                "company_id": comp.id,
                "company_name": comp.name,
                "ticker": comp.ticker,
                "currency": comp.currency,
                "units": comp.units,
                "ratios": ratios,
                "summary_insights": insights
            }

    # 2. Fetch ESG data and score
    esg_summary = None
    if comp:
        esg_query = db.query(ESGData).filter(ESGData.company_id == comp.id)
        if payload.fiscal_year:
            esg_query = esg_query.filter(ESGData.fiscal_year == payload.fiscal_year)
        esg_rec = esg_query.order_by(ESGData.fiscal_year.desc()).first()
        if esg_rec:
            esg_summary = TransparentESGScorer.evaluate_esg(esg_rec)

    # 3. Hybrid Retrieval: Dense + BM25 + RRF + Reranker
    # Fetch all chunks from DB for BM25 corpus matching company or global
    chunk_query = db.query(DocumentChunk)
    if comp:
        chunk_query = chunk_query.filter(DocumentChunk.company_id == comp.id)
    all_chunks = chunk_query.all()

    bm25_engine = BM25SearchEngine()
    if all_chunks:
        chunk_dicts = [{
            "chunk_id": c.chunk_id,
            "document_id": c.document_id,
            "company_id": c.company_id,
            "fiscal_year": c.fiscal_year,
            "page_number": c.page_number,
            "section": c.section,
            "content": c.content,
            "is_table": c.is_table,
            "document_title": c.document.title if c.document else "Annual Report",
            "document_type": c.document.document_type if c.document else "Annual Report",
            "company_name": comp.name if comp else "Company"
        } for c in all_chunks]
        bm25_engine.index_chunks(chunk_dicts)

    retriever = HybridRetriever(bm25_engine=bm25_engine)
    retrieved_evidence = retriever.retrieve(
        query=payload.query,
        company_id=comp.id if comp else None,
        fiscal_year=payload.fiscal_year,
        dense_top_k=10,
        bm25_top_k=10,
        final_top_k=payload.top_k,
        enable_reranking=payload.enable_reranking
    )

    # 4. Generate grounded answer
    response = LLMService.answer_query(
        query=payload.query,
        company_id=comp.id if comp else None,
        fiscal_year=payload.fiscal_year,
        metrics=metrics_summary,
        esg=esg_summary,
        evidence=retrieved_evidence
    )

    # 5. Persist Query History
    try:
        history_rec = QueryHistory(
            company_id=comp.id if comp else None,
            query_text=payload.query,
            query_type=response.query_type,
            response_text=response.answer,
            calculated_metrics_json=json.dumps(metrics_summary) if metrics_summary else None,
            citations_json=json.dumps([c.model_dump() for c in response.citations])
        )
        db.add(history_rec)
        db.commit()
    except Exception as e:
        db.rollback()

    return response

@router.get("/history")
def get_query_history(company_id: Optional[int] = Query(None), limit: int = 20, db: Session = Depends(get_db)):
    query = db.query(QueryHistory)
    if company_id:
        query = query.filter(QueryHistory.company_id == company_id)
    records = query.order_by(QueryHistory.created_at.desc()).limit(limit).all()
    return records
