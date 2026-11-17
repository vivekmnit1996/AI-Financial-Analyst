import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.rag.sample_document_generator import SampleDocumentGenerator
from backend.app.models.schema_models import Company

client = TestClient(app)

def test_complete_end_to_end_flow():
    """
    Full End-to-End Functional Test:
    1. Create Company
    2. Upload Financial Data
    3. Generate & Ingest Multi-Page Report PDF
    4. Compute Financial Ratios
    5. Evaluate ESG Disclosures
    6. Run Hybrid RAG Chat Query with Evidence Citations
    7. Generate Institutional PDF & HTML Report
    8. Verify Output Integrity
    """
    # 0. Clean up any existing E2ETEST company
    existing = client.get("/api/v1/companies").json()
    for c in existing:
        if c["ticker"] == "E2ETEST":
            client.delete(f"/api/v1/companies/{c['id']}")

    # 1. Create a company
    comp_payload = {
        "ticker": "E2ETEST",
        "name": "E2E Global Technologies Corp",
        "sector": "Information Technology",
        "industry": "Enterprise Software",
        "currency": "USD",
        "units": "Millions",
        "exchange": "NASDAQ"
    }
    create_resp = client.post("/api/v1/companies", json=comp_payload)
    assert create_resp.status_code == 200, create_resp.text
    company_id = create_resp.json()["id"]

    # 2. Add two years of financial data
    fin_y1 = {
        "company_id": company_id,
        "fiscal_year": 2023,
        "period": "FY",
        "currency": "USD",
        "units": "Millions",
        "source": "Audited 10-K",
        "revenue": 5000.0,
        "cost_of_revenue": 3000.0,
        "gross_profit": 2000.0,
        "operating_profit": 1200.0,
        "net_profit": 900.0,
        "total_assets": 6000.0,
        "current_assets": 3500.0,
        "total_liabilities": 2500.0,
        "current_liabilities": 1800.0,
        "shareholders_equity": 3500.0,
        "debt": 500.0,
        "cash": 800.0,
        "operating_cash_flow": 1100.0,
        "capital_expenditures": 200.0,
        "free_cash_flow": 900.0,
        "eps": 4.50
    }
    fin_y2 = {
        "company_id": company_id,
        "fiscal_year": 2024,
        "period": "FY",
        "currency": "USD",
        "units": "Millions",
        "source": "Audited 10-K",
        "revenue": 5750.0,
        "cost_of_revenue": 3400.0,
        "gross_profit": 2350.0,
        "operating_profit": 1450.0,
        "net_profit": 1100.0,
        "total_assets": 7000.0,
        "current_assets": 4200.0,
        "total_liabilities": 2800.0,
        "current_liabilities": 2000.0,
        "shareholders_equity": 4200.0,
        "debt": 400.0,
        "cash": 1200.0,
        "operating_cash_flow": 1350.0,
        "capital_expenditures": 250.0,
        "free_cash_flow": 1100.0,
        "eps": 5.50
    }
    assert client.post("/api/v1/financials", json=fin_y1).status_code == 200
    assert client.post("/api/v1/financials", json=fin_y2).status_code == 200

    # 3. Add ESG Disclosures
    esg_payload = {
        "company_id": company_id,
        "fiscal_year": 2024,
        "reporting_period": "FY",
        "renewable_energy_pct": 52.0,
        "water_recycled_pct": 38.0,
        "waste_recycled_pct": 82.0,
        "carbon_emissions_scope1": 45000.0,
        "carbon_emissions_scope2": 85000.0,
        "female_workforce_pct": 34.0,
        "training_hours_per_employee": 42.0,
        "lost_time_injury_rate": 0.05,
        "human_rights_policy": True,
        "csr_spending_amount": 25.0,
        "board_size": 8,
        "independent_directors_pct": 62.5,
        "women_on_board_pct": 37.5,
        "ceo_chair_separation": True,
        "ethics_code_established": True,
        "whistleblower_mechanism": True,
        "anti_corruption_policy": True,
        "data_privacy_policy": True
    }
    assert client.post("/api/v1/esg", json=esg_payload).status_code == 200

    # 4. Generate & Ingest Report PDF
    temp_comp = Company(id=company_id, ticker="E2ETEST", name="E2E Global Technologies Corp", sector="Tech", currency="USD", units="Millions")
    pdf_path = SampleDocumentGenerator.generate_or_get_report_for_company(temp_comp)
    assert os.path.exists(pdf_path)

    with open(pdf_path, "rb") as f:
        upload_resp = client.post(
            "/api/v1/documents/upload",
            data={"company_id": company_id, "document_type": "Annual Report", "fiscal_year": 2024},
            files={"file": (os.path.basename(pdf_path), f, "application/pdf")}
        )
    assert upload_resp.status_code == 200, upload_resp.text
    doc_id = upload_resp.json()["id"]
    assert upload_resp.json()["status"] == "INDEXED"

    # 5. Deterministic Financial Analysis
    analysis_resp = client.get(f"/api/v1/financials/analysis/{company_id}")
    assert analysis_resp.status_code == 200
    a_data = analysis_resp.json()
    assert len(a_data["ratios"]) == 2
    # Revenue growth: (5750 - 5000)/5000 * 100 = 15.0%
    assert a_data["ratios"][1]["revenue_growth_pct"] == 15.0
    assert a_data["ratios"][1]["operating_profit_margin_pct"] == round((1450.0 / 5750.0) * 100, 2)

    # 6. ESG Score Verification
    esg_resp = client.get(f"/api/v1/esg/score/{company_id}")
    assert esg_resp.status_code == 200
    esg_data = esg_resp.json()
    assert esg_data["is_sufficient_data"] is True
    assert esg_data["overall_esg_score"] is not None

    # 7. AI Hybrid Chat Query with Citations
    query_resp = client.post("/api/v1/chat/query", json={
        "query": "What are the primary risk factors and operating margin drivers?",
        "company_id": company_id,
        "fiscal_year": 2024,
        "top_k": 3
    })
    assert query_resp.status_code == 200
    q_data = query_resp.json()
    assert q_data["grounded"] is True
    assert len(q_data["citations"]) > 0
    assert any("Page" in c["document_title"] or c["page_number"] > 0 for c in q_data["citations"])

    # 8. Report Generation & Download
    rep_resp = client.post("/api/v1/reports/generate", json={
        "company_id": company_id,
        "fiscal_year": 2024,
        "title": "E2E Verified Institutional Report FY2024"
    })
    assert rep_resp.status_code == 200
    rep_id = rep_resp.json()["id"]

    pdf_dl = client.get(f"/api/v1/reports/{rep_id}/pdf")
    assert pdf_dl.status_code == 200
    assert len(pdf_dl.content) > 1000

    html_dl = client.get(f"/api/v1/reports/{rep_id}/html")
    assert html_dl.status_code == 200
    assert "E2E Global Technologies Corp" in html_dl.text

    # Cleanup test company
    client.delete(f"/api/v1/companies/{company_id}")
