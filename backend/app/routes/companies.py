from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.schema_models import Company
from backend.app.schemas.pydantic_schemas import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyDiscoveryItem
)
from backend.app.collectors.company_catalog import CompanyCatalogService

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("", response_model=List[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return db.query(Company).order_by(Company.name.asc()).all()

@router.get("/discover/search", response_model=List[CompanyDiscoveryItem])
def search_catalog(
    query: str = Query("", description="Ticker or company name"),
    exchange: Optional[str] = Query(None, description="Filter by exchange e.g. NSE, NASDAQ")
):
    """Search public companies available for automated financial and document collection."""
    results = CompanyCatalogService.search(query=query, exchange=exchange)
    return [CompanyDiscoveryItem(**r) for r in results]

@router.post("/discover/import", response_model=CompanyResponse)
def import_from_catalog(ticker: str = Query(..., description="Ticker from catalog"), db: Session = Depends(get_db)):
    """Import a company from the public catalog into the working database."""
    comp_meta = CompanyCatalogService.get_by_ticker(ticker)
    if not comp_meta:
        raise HTTPException(status_code=404, detail=f"Company with ticker '{ticker}' not found in public catalog.")
    
    existing = db.query(Company).filter(Company.ticker == comp_meta["ticker"]).first()
    if existing:
        return existing

    new_comp = Company(
        ticker=comp_meta["ticker"],
        name=comp_meta["name"],
        sector=comp_meta.get("sector"),
        industry=comp_meta.get("industry"),
        description=comp_meta.get("description"),
        currency=comp_meta.get("currency", "INR"),
        units=comp_meta.get("units", "Crores"),
        exchange=comp_meta.get("exchange"),
        cik=comp_meta.get("cik"),
        isin=comp_meta.get("isin"),
        nse_symbol=comp_meta.get("nse_symbol"),
        bse_code=comp_meta.get("bse_code"),
        ir_url=comp_meta.get("ir_url")
    )
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return new_comp

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    return comp

@router.post("", response_model=CompanyResponse)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.query(Company).filter(Company.ticker == payload.ticker.upper()).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Company with ticker '{payload.ticker}' already exists.")
    
    comp = Company(
        ticker=payload.ticker.upper(),
        name=payload.name,
        sector=payload.sector,
        industry=payload.industry,
        description=payload.description,
        currency=payload.currency,
        units=payload.units,
        exchange=payload.exchange,
        cik=payload.cik,
        isin=payload.isin,
        nse_symbol=payload.nse_symbol,
        bse_code=payload.bse_code,
        ir_url=payload.ir_url
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return comp

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(comp, k, v)
    
    db.commit()
    db.refresh(comp)
    return comp

@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(comp)
    db.commit()
    return {"message": f"Company {comp.name} deleted successfully"}
