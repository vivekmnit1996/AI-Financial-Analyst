import io
from typing import List, Optional
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.schema_models import Company, FinancialData
from backend.app.schemas.pydantic_schemas import (
    FinancialDataCreate, FinancialDataUpdate, FinancialDataResponse,
    FinancialAnalysisResponse, FinancialRatioSet
)
from backend.app.engine.financial_calculator import FinancialCalculatorEngine
from backend.app.collectors.data_validator import FinancialDataValidator

router = APIRouter(prefix="/financials", tags=["Financial Data & Analysis"])

@router.get("/company/{company_id}", response_model=List[FinancialDataResponse])
def get_company_financials(company_id: int, db: Session = Depends(get_db)):
    return db.query(FinancialData).filter(
        FinancialData.company_id == company_id
    ).order_by(FinancialData.fiscal_year.asc(), FinancialData.period.asc()).all()

@router.post("", response_model=FinancialDataResponse)
def create_financial_data(payload: FinancialDataCreate, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == payload.company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    rec_dict = payload.model_dump()
    val_status, warnings = FinancialDataValidator.validate_financial_record(rec_dict)

    existing = db.query(FinancialData).filter(
        FinancialData.company_id == payload.company_id,
        FinancialData.fiscal_year == payload.fiscal_year,
        FinancialData.period == payload.period
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Financial record for {comp.name} FY{payload.fiscal_year} ({payload.period}) already exists. Use PUT to update."
        )

    fin_obj = FinancialData(**rec_dict, validation_status=val_status, validation_notes="; ".join(warnings))
    db.add(fin_obj)
    db.commit()
    db.refresh(fin_obj)
    return fin_obj

@router.put("/{record_id}", response_model=FinancialDataResponse)
def update_financial_data(record_id: int, payload: FinancialDataUpdate, db: Session = Depends(get_db)):
    fin = db.query(FinancialData).filter(FinancialData.id == record_id).first()
    if not fin:
        raise HTTPException(status_code=404, detail="Financial record not found")

    update_dict = payload.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(fin, k, v)

    val_status, warnings = FinancialDataValidator.validate_financial_record(fin.__dict__)
    fin.validation_status = val_status
    fin.validation_notes = "; ".join(warnings)

    db.commit()
    db.refresh(fin)
    return fin

@router.delete("/{record_id}")
def delete_financial_data(record_id: int, db: Session = Depends(get_db)):
    fin = db.query(FinancialData).filter(FinancialData.id == record_id).first()
    if not fin:
        raise HTTPException(status_code=404, detail="Financial record not found")
    db.delete(fin)
    db.commit()
    return {"message": "Financial record deleted successfully"}

@router.post("/upload-csv")
async def upload_financial_csv(
    company_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload CSV or XLSX file containing financial records."""
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    filename = file.filename.lower()
    content = await file.read()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Only CSV and XLSX files are supported.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    # Clean column headers: lowercase, strip, replace spaces/dashes with underscores
    df.columns = [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]

    if "fiscal_year" not in df.columns:
        raise HTTPException(status_code=400, detail="Uploaded file must contain 'fiscal_year' column.")

    imported_count = 0
    warnings_list = []

    for _, row in df.iterrows():
        try:
            fy = int(row["fiscal_year"])
            period = str(row.get("period", "FY")).strip().upper()

            def get_f(col):
                val = row.get(col)
                if pd.isna(val) or val is None or str(val).strip() == "":
                    return None
                try:
                    return float(val)
                except Exception:
                    return None

            rec_data = {
                "fiscal_year": fy,
                "period": period,
                "currency": str(row.get("currency", comp.currency)),
                "units": str(row.get("units", comp.units)),
                "source": f"Uploaded File: {file.filename}",
                "revenue": get_f("revenue"),
                "cost_of_revenue": get_f("cost_of_revenue"),
                "gross_profit": get_f("gross_profit"),
                "operating_profit": get_f("operating_profit"),
                "net_profit": get_f("net_profit"),
                "eps": get_f("eps"),
                "shares_outstanding": get_f("shares_outstanding"),
                "total_assets": get_f("total_assets"),
                "current_assets": get_f("current_assets"),
                "total_liabilities": get_f("total_liabilities"),
                "current_liabilities": get_f("current_liabilities"),
                "shareholders_equity": get_f("shareholders_equity"),
                "debt": get_f("debt"),
                "cash": get_f("cash"),
                "operating_cash_flow": get_f("operating_cash_flow"),
                "capital_expenditures": get_f("capital_expenditures"),
                "free_cash_flow": get_f("free_cash_flow"),
            }

            val_status, w_items = FinancialDataValidator.validate_financial_record(rec_data)
            if w_items:
                warnings_list.extend([f"FY{fy}: {w}" for w in w_items])

            existing = db.query(FinancialData).filter(
                FinancialData.company_id == comp.id,
                FinancialData.fiscal_year == fy,
                FinancialData.period == period
            ).first()

            if not existing:
                fin_obj = FinancialData(company_id=comp.id, **rec_data, validation_status=val_status)
                db.add(fin_obj)
            else:
                for k, v in rec_data.items():
                    setattr(existing, k, v)
                existing.validation_status = val_status

            imported_count += 1
        except Exception as row_err:
            warnings_list.append(f"Row error: {str(row_err)}")

    db.commit()
    return {
        "status": "SUCCESS",
        "imported_records": imported_count,
        "company": comp.name,
        "warnings": warnings_list
    }

@router.get("/analysis/{company_id}", response_model=FinancialAnalysisResponse)
def get_financial_analysis(company_id: int, db: Session = Depends(get_db)):
    """
    Deterministically computes financial ratios, YoY growth rates, capital efficiency,
    cash flow conversions, and data completeness warnings using Python / Pandas.
    """
    comp = db.query(Company).filter(Company.id == company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    records = db.query(FinancialData).filter(
        FinancialData.company_id == company_id
    ).order_by(FinancialData.fiscal_year.asc(), FinancialData.period.asc()).all()

    if not records:
        return FinancialAnalysisResponse(
            company_id=comp.id,
            company_name=comp.name,
            ticker=comp.ticker,
            currency=comp.currency,
            units=comp.units,
            years_available=[],
            ratios=[],
            summary_insights=["No financial data available. Upload data or trigger automated collection."],
            missing_data_warnings=["No records in database."]
        )

    ratio_dicts = FinancialCalculatorEngine.compute_ratios_for_records(records)
    insights = FinancialCalculatorEngine.generate_analytical_insights(ratio_dicts)

    all_warnings = []
    for r in ratio_dicts:
        all_warnings.extend(r.get("warnings", []))

    ratio_objs = [FinancialRatioSet(**r) for r in ratio_dicts]
    years = [r.fiscal_year for r in records]

    return FinancialAnalysisResponse(
        company_id=comp.id,
        company_name=comp.name,
        ticker=comp.ticker,
        currency=comp.currency,
        units=comp.units,
        years_available=sorted(list(set(years))),
        ratios=ratio_objs,
        summary_insights=insights,
        missing_data_warnings=list(set(all_warnings))
    )

@router.get("/comparison")
def compare_companies(company_ids: str = Query(..., description="Comma-separated company IDs"), db: Session = Depends(get_db)):
    """Compare multiple companies across key financial metrics and ratios."""
    ids = [int(i.strip()) for i in company_ids.split(",") if i.strip().isdigit()]
    if not ids:
        raise HTTPException(status_code=400, detail="Invalid company_ids provided.")

    comparison_results = []
    for cid in ids:
        comp = db.query(Company).filter(Company.id == cid).first()
        if not comp:
            continue
        records = db.query(FinancialData).filter(FinancialData.company_id == cid).all()
        ratios = FinancialCalculatorEngine.compute_ratios_for_records(records) if records else []
        latest_ratio = ratios[-1] if ratios else {}

        comparison_results.append({
            "company_id": comp.id,
            "company_name": comp.name,
            "ticker": comp.ticker,
            "sector": comp.sector,
            "currency": comp.currency,
            "units": comp.units,
            "latest_fiscal_year": latest_ratio.get("fiscal_year"),
            "revenue": latest_ratio.get("revenue"),
            "revenue_growth_pct": latest_ratio.get("revenue_growth_pct"),
            "operating_profit_margin_pct": latest_ratio.get("operating_profit_margin_pct"),
            "net_profit_margin_pct": latest_ratio.get("net_profit_margin_pct"),
            "return_on_equity_pct": latest_ratio.get("return_on_equity_pct"),
            "debt_to_equity": latest_ratio.get("debt_to_equity"),
            "operating_cash_flow": latest_ratio.get("operating_cash_flow"),
        })

    return comparison_results
