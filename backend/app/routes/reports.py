import os
import json
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models.schema_models import (
    Company, FinancialData, ESGData, GeneratedReport
)
from backend.app.schemas.pydantic_schemas import (
    ReportGenerateRequest, GeneratedReportResponse
)
from backend.app.engine.financial_calculator import FinancialCalculatorEngine
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.report_generator.pdf_generator import PDFReportGenerator
from backend.app.report_generator.html_generator import HTMLReportGenerator

router = APIRouter(prefix="/reports", tags=["Report Generation"])

@router.post("/generate", response_model=GeneratedReportResponse)
def generate_report(payload: ReportGenerateRequest, db: Session = Depends(get_db)):
    comp = db.query(Company).filter(Company.id == payload.company_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Company not found")

    # 1. Fetch financial records
    fin_records = db.query(FinancialData).filter(
        FinancialData.company_id == comp.id
    ).order_by(FinancialData.fiscal_year.asc()).all()

    ratios_data = FinancialCalculatorEngine.compute_ratios_for_records(fin_records) if fin_records else []
    insights = FinancialCalculatorEngine.generate_analytical_insights(ratios_data) if ratios_data else []

    # 2. Fetch ESG data
    esg_rec = db.query(ESGData).filter(
        ESGData.company_id == comp.id,
        ESGData.fiscal_year == payload.fiscal_year
    ).first()
    if not esg_rec:
        esg_rec = db.query(ESGData).filter(ESGData.company_id == comp.id).order_by(ESGData.fiscal_year.desc()).first()

    esg_breakdown = TransparentESGScorer.evaluate_esg(esg_rec) if esg_rec else {}

    # 3. Compile citations & qualitative highlights from uploaded documents
    citations = []
    for doc in comp.documents:
        for chk in doc.chunks[:2]:
            citations.append({
                "document_title": doc.title,
                "fiscal_year": doc.fiscal_year,
                "page_number": chk.page_number,
                "section": chk.section,
                "snippet": chk.content[:280]
            })

    # 4. Generate AI summary
    ai_summary = " ".join(insights[:3]) if insights else "Company exhibits stable operating fundamentals."

    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{comp.ticker}_FY{payload.fiscal_year}_Analysis_{timestamp_str}.pdf"
    html_filename = f"{comp.ticker}_FY{payload.fiscal_year}_Analysis_{timestamp_str}.html"

    # Generate PDF
    pdf_path = PDFReportGenerator.generate_report(
        company=comp,
        fiscal_year=payload.fiscal_year,
        ratios_data=ratios_data,
        insights=insights,
        esg_breakdown=esg_breakdown,
        citations=citations,
        ai_summary=ai_summary,
        output_filename=pdf_filename
    )

    # Generate HTML
    html_path = HTMLReportGenerator.generate_html_report(
        company=comp,
        fiscal_year=payload.fiscal_year,
        ratios_data=ratios_data,
        insights=insights,
        esg_breakdown=esg_breakdown,
        citations=citations,
        ai_summary=ai_summary,
        output_filename=html_filename
    )

    report_title = payload.title or f"{comp.name} Comprehensive Financial & ESG Report (FY{payload.fiscal_year})"

    rep_obj = GeneratedReport(
        company_id=comp.id,
        fiscal_year=payload.fiscal_year,
        title=report_title,
        report_type=payload.report_type,
        pdf_path=pdf_path,
        html_path=html_path,
        summary=ai_summary,
        metrics_json=json.dumps(ratios_data),
        citations_json=json.dumps(citations)
    )
    db.add(rep_obj)
    db.commit()
    db.refresh(rep_obj)

    return GeneratedReportResponse(
        id=rep_obj.id,
        company_id=comp.id,
        company_name=comp.name,
        fiscal_year=rep_obj.fiscal_year,
        title=rep_obj.title,
        report_type=rep_obj.report_type,
        pdf_url=f"/api/v1/reports/{rep_obj.id}/pdf",
        html_url=f"/api/v1/reports/{rep_obj.id}/html",
        summary=rep_obj.summary,
        created_at=rep_obj.created_at
    )

@router.get("", response_model=List[GeneratedReportResponse])
def list_reports(company_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    query = db.query(GeneratedReport)
    if company_id:
        query = query.filter(GeneratedReport.company_id == company_id)
    reps = query.order_by(GeneratedReport.created_at.desc()).all()

    return [
        GeneratedReportResponse(
            id=r.id,
            company_id=r.company_id,
            company_name=r.company.name if r.company else "Company",
            fiscal_year=r.fiscal_year,
            title=r.title,
            report_type=r.report_type,
            pdf_url=f"/api/v1/reports/{r.id}/pdf",
            html_url=f"/api/v1/reports/{r.id}/html",
            summary=r.summary,
            created_at=r.created_at
        )
        for r in reps
    ]

@router.get("/{report_id}/pdf")
def download_pdf_report(report_id: int, db: Session = Depends(get_db)):
    rep = db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()
    if not rep or not rep.pdf_path or not os.path.exists(rep.pdf_path):
        raise HTTPException(status_code=404, detail="PDF report not found on server.")
    return FileResponse(rep.pdf_path, filename=os.path.basename(rep.pdf_path), media_type="application/pdf")

@router.get("/{report_id}/html")
def view_html_report(report_id: int, db: Session = Depends(get_db)):
    rep = db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()
    if not rep or not rep.html_path or not os.path.exists(rep.html_path):
        raise HTTPException(status_code=404, detail="HTML report not found on server.")
    with open(rep.html_path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content)

@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    rep = db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Report not found")
    if rep.pdf_path and os.path.exists(rep.pdf_path):
        try: os.remove(rep.pdf_path)
        except Exception: pass
    if rep.html_path and os.path.exists(rep.html_path):
        try: os.remove(rep.html_path)
        except Exception: pass
    db.delete(rep)
    db.commit()
    return {"message": "Report deleted successfully"}
