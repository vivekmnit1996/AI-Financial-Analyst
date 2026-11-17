import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from backend.app.database import get_db, SessionLocal
from backend.app.models.schema_models import Company, DataCollectionJob, DiscoveredDocument
from backend.app.schemas.pydantic_schemas import (
    TriggerCollectionRequest, DataCollectionJobResponse, DiscoveredDocumentResponse
)
from backend.app.collectors.collection_orchestrator import CollectionOrchestrator

router = APIRouter(prefix="/collection", tags=["Automated Data Collection & Pipeline"])

def run_collection_task(job_id: int, company_id: int, sources: List[str], fiscal_years: List[int], categories: List[str]):
    db = SessionLocal()
    try:
        CollectionOrchestrator.execute_collection_job(
            db=db,
            job_id=job_id,
            company_id=company_id,
            sources=sources,
            fiscal_years=fiscal_years,
            document_categories=categories
        )
    finally:
        db.close()

@router.post("/trigger", response_model=DataCollectionJobResponse)
def trigger_collection(
    payload: TriggerCollectionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Initiates automated financial and ESG data collection from SEC EDGAR,
    Indian Exchange Filings, and verified Company IR portals.
    """
    comp = db.query(Company).filter(Company.id == payload.company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    job = DataCollectionJob(
        company_id=comp.id,
        status="PENDING",
        sources_searched=json.dumps(payload.sources),
        logs=f"Job queued for {comp.name} ({comp.ticker})."
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Dispatch to background task or execute synchronously if requested
    background_tasks.add_task(
        run_collection_task,
        job.id,
        comp.id,
        payload.sources,
        payload.fiscal_years,
        payload.document_categories
    )

    return job

@router.get("/jobs", response_model=List[DataCollectionJobResponse])
def list_collection_jobs(company_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(DataCollectionJob)
    if company_id is not None:
        query = query.filter(DataCollectionJob.company_id == company_id)
    return query.order_by(DataCollectionJob.started_at.desc()).all()

@router.get("/jobs/{job_id}", response_model=DataCollectionJobResponse)
def get_collection_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(DataCollectionJob).filter(DataCollectionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/discovered-docs", response_model=List[DiscoveredDocumentResponse])
def list_discovered_documents(company_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(DiscoveredDocument)
    if company_id is not None:
        query = query.filter(DiscoveredDocument.company_id == company_id)
    return query.order_by(DiscoveredDocument.discovered_at.desc()).all()

@router.post("/retry/{job_id}", response_model=DataCollectionJobResponse)
def retry_failed_collection(job_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = db.query(DataCollectionJob).filter(DataCollectionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = "PENDING"
    job.failed_operations = 0
    db.commit()

    sources = json.loads(job.sources_searched) if job.sources_searched else ["SEC EDGAR", "NSE/BSE Filings"]
    background_tasks.add_task(
        run_collection_task,
        job.id,
        job.company_id,
        sources,
        [2023, 2024, 2025],
        ["Annual Report"]
    )
    return job
