import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.schema_models import (
    Company, FinancialData, ESGData, Document, DocumentChunk, GeneratedReport
)
from backend.app.collectors.exchange_connector import VERIFIED_EXCHANGE_DATA
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.rag.document_parser import DocumentParser
from backend.app.rag.chunker import StructureAwareChunker
from backend.app.rag.vector_store import VectorStoreManager
from backend.app.rag.sample_document_generator import SampleDocumentGenerator
from backend.app.collectors.sec_edgar_connector import SecEdgarConnector
from backend.app.collectors.company_catalog import DEFAULT_COMPANY_CATALOG

def seed():
    print("[Seed] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        print("[Seed] Populating company catalog entries...")
        for c in DEFAULT_COMPANY_CATALOG:
            existing = db.query(Company).filter(Company.ticker == c["ticker"]).first()
            if not existing:
                comp = Company(
                    ticker=c["ticker"],
                    name=c["name"],
                    sector=c["sector"],
                    industry=c["industry"],
                    description=c["description"],
                    currency=c["currency"],
                    units=c["units"],
                    exchange=c["exchange"],
                    cik=c.get("cik"),
                    isin=c.get("isin"),
                    nse_symbol=c.get("nse_symbol"),
                    bse_code=c.get("bse_code"),
                    ir_url=c.get("ir_url")
                )
                db.add(comp)
        db.commit()

        # Seed TCS Financials & ESG
        tcs = db.query(Company).filter(Company.ticker == "TCS").first()
        if tcs and "TCS" in VERIFIED_EXCHANGE_DATA:
            print(f"[Seed] Seeding audited financials for {tcs.name}...")
            tcs_data = VERIFIED_EXCHANGE_DATA["TCS"]
            for rec in tcs_data["financials"]:
                existing_fin = db.query(FinancialData).filter(
                    FinancialData.company_id == tcs.id,
                    FinancialData.fiscal_year == rec["fiscal_year"],
                    FinancialData.period == rec["period"]
                ).first()
                if not existing_fin:
                    fin_obj = FinancialData(company_id=tcs.id, **rec, validation_status="VALIDATED")
                    db.add(fin_obj)

            # Seed ESG
            esg_dict = tcs_data["esg"]
            dummy = ESGData(**esg_dict)
            sc = TransparentESGScorer.evaluate_esg(dummy)
            esg_dict["environmental_score"] = sc["environmental_score"]
            esg_dict["social_score"] = sc["social_score"]
            esg_dict["governance_score"] = sc["governance_score"]
            esg_dict["overall_esg_score"] = sc["overall_esg_score"]
            esg_dict["data_coverage_pct"] = sc["data_coverage_pct"]
            esg_dict["score_breakdown_json"] = json.dumps(sc)

            existing_esg = db.query(ESGData).filter(
                ESGData.company_id == tcs.id,
                ESGData.fiscal_year == esg_dict["fiscal_year"]
            ).first()
            if not existing_esg:
                db.add(ESGData(company_id=tcs.id, **esg_dict))
            db.commit()

            # Generate & Ingest Multi-Page PDF Annual Report
            print(f"[Seed] Generating and indexing integrated annual report for {tcs.name}...")
            pdf_path = SampleDocumentGenerator.generate_or_get_report_for_company(tcs)
            existing_doc = db.query(Document).filter(Document.company_id == tcs.id).first()
            if not existing_doc:
                pages_data, meta = DocumentParser.parse_pdf(pdf_path)
                doc_obj = Document(
                    company_id=tcs.id,
                    title=f"{tcs.name} Integrated Annual Report FY2024",
                    file_name=os.path.basename(pdf_path),
                    file_path=pdf_path,
                    file_hash=meta["file_hash"],
                    file_size_bytes=meta["file_size_bytes"],
                    document_type="Annual Report",
                    fiscal_year=2024,
                    total_pages=meta["total_pages"],
                    status="PROCESSING",
                    source_url=tcs.ir_url
                )
                db.add(doc_obj)
                db.commit()
                db.refresh(doc_obj)

                chunks = StructureAwareChunker.chunk_pages(pages_data, {
                    "document_id": doc_obj.id,
                    "company_id": tcs.id,
                    "company_name": tcs.name,
                    "fiscal_year": 2024,
                    "title": doc_obj.title,
                    "document_type": doc_obj.document_type
                })

                VectorStoreManager.upsert_chunks(chunks)

                for chk in chunks:
                    chunk_rec = DocumentChunk(
                        document_id=doc_obj.id,
                        company_id=tcs.id,
                        fiscal_year=2024,
                        page_number=chk["page_number"],
                        section=chk["section"],
                        chunk_index=chk["chunk_index"],
                        chunk_id=chk["chunk_id"],
                        content=chk["content"],
                        token_count=chk["token_count"],
                        is_table=chk["is_table"]
                    )
                    db.add(chunk_rec)

                doc_obj.status = "INDEXED"
                doc_obj.total_chunks = len(chunks)
                db.commit()
                print(f"[Seed] Successfully indexed {len(chunks)} chunks into Qdrant for {tcs.name}!")

        # Seed Apple (AAPL) from real SEC EDGAR facts
        aapl = db.query(Company).filter(Company.ticker == "AAPL").first()
        if aapl and aapl.cik:
            print(f"[Seed] Querying live SEC EDGAR data for {aapl.name} (CIK: {aapl.cik})...")
            try:
                aapl_financials = SecEdgarConnector.extract_annual_financials(aapl.cik, target_years=[2024, 2025, 2026])
                for rec in aapl_financials:
                    existing = db.query(FinancialData).filter(
                        FinancialData.company_id == aapl.id,
                        FinancialData.fiscal_year == rec["fiscal_year"],
                        FinancialData.period == rec["period"]
                    ).first()
                    if not existing:
                        db.add(FinancialData(company_id=aapl.id, **rec, validation_status="VALIDATED"))
                db.commit()
                print(f"[Seed] Seeded {len(aapl_financials)} SEC EDGAR periods for Apple Inc.")
            except Exception as e:
                print(f"[Seed] Note: SEC EDGAR call skipped ({e}).")

        print("[Seed] Seed completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
