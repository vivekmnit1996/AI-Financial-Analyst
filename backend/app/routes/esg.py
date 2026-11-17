import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.schema_models import Company, ESGData
from backend.app.schemas.pydantic_schemas import (
    ESGDataCreate, ESGDataResponse, ESGScoreBreakdown
)
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.collectors.data_validator import FinancialDataValidator

router = APIRouter(prefix="/esg", tags=["ESG Analysis & Scoring"])

@router.get("/company/{company_id}", response_model=List[ESGDataResponse])
def get_company_esg(company_id: int, db: Session = Depends(get_db)):
    return db.query(ESGData).filter(ESGData.company_id == company_id).order_by(ESGData.fiscal_year.desc()).all()

@router.post("", response_model=ESGDataResponse)
def create_or_update_esg(payload: ESGDataCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == payload.company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    rec_dict = payload.model_dump()
    val_status, warnings = FinancialDataValidator.validate_esg_record(rec_dict)

    # Compute transparent ESG scores
    dummy_obj = ESGData(**rec_dict)
    score_res = TransparentESGScorer.evaluate_esg(dummy_obj)

    rec_dict["environmental_score"] = score_res["environmental_score"]
    rec_dict["social_score"] = score_res["social_score"]
    rec_dict["governance_score"] = score_res["governance_score"]
    rec_dict["overall_esg_score"] = score_res["overall_esg_score"]
    rec_dict["data_coverage_pct"] = score_res["data_coverage_pct"]
    rec_dict["score_breakdown_json"] = json.dumps(score_res)

    existing = db.query(ESGData).filter(
        ESGData.company_id == payload.company_id,
        ESGData.fiscal_year == payload.fiscal_year,
        ESGData.reporting_period == payload.reporting_period
    ).first()

    if not existing:
        esg_obj = ESGData(**rec_dict)
        db.add(esg_obj)
    else:
        for k, v in rec_dict.items():
            setattr(existing, k, v)
        esg_obj = existing

    db.commit()
    db.refresh(esg_obj)
    return esg_obj

@router.get("/score/{company_id}", response_model=ESGScoreBreakdown)
def get_esg_score_breakdown(
    company_id: int,
    fiscal_year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns full transparent ESG scoring breakdown, normalized indicators,
    weights, formula explanation, and methodology limitations.
    """
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    query = db.query(ESGData).filter(ESGData.company_id == company_id)
    if fiscal_year:
        query = query.filter(ESGData.fiscal_year == fiscal_year)
    esg_rec = query.order_by(ESGData.fiscal_year.desc()).first()

    if not esg_rec:
        raise HTTPException(status_code=404, detail="No ESG disclosure data found for this company.")

    score_res = TransparentESGScorer.evaluate_esg(esg_rec)
    return ESGScoreBreakdown(**score_res)
