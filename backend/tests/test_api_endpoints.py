import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    # Test API status endpoint
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RUNNING"
    assert "version" in data

    # Test Web App SPA root
    spa_resp = client.get("/")
    assert spa_resp.status_code == 200

def test_list_companies():
    response = client.get("/api/v1/companies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_company_catalog_search():
    response = client.get("/api/v1/companies/discover/search?query=TCS")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["ticker"] == "TCS"

def test_financial_analysis_endpoint():
    # Find TCS id
    comp_resp = client.get("/api/v1/companies")
    companies = comp_resp.json()
    tcs = next((c for c in companies if c["ticker"] == "TCS"), None)
    assert tcs is not None

    response = client.get(f"/api/v1/financials/analysis/{tcs['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["company_id"] == tcs["id"]
    assert "ratios" in data
    assert len(data["ratios"]) >= 1

def test_esg_score_endpoint():
    comp_resp = client.get("/api/v1/companies")
    tcs = next((c for c in comp_resp.json() if c["ticker"] == "TCS"), None)
    assert tcs is not None

    response = client.get(f"/api/v1/esg/score/{tcs['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "environmental_score" in data
    assert "weights" in data

def test_chat_query_endpoint():
    comp_resp = client.get("/api/v1/companies")
    tcs = next((c for c in comp_resp.json() if c["ticker"] == "TCS"), None)
    assert tcs is not None

    payload = {
        "query": "Why did operating margin change in FY2024?",
        "company_id": tcs["id"],
        "fiscal_year": 2024,
        "top_k": 3
    }
    response = client.post("/api/v1/chat/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["grounded"] is True
    assert len(data["citations"]) > 0

def test_report_generation_endpoint():
    comp_resp = client.get("/api/v1/companies")
    tcs = next((c for c in comp_resp.json() if c["ticker"] == "TCS"), None)
    assert tcs is not None

    payload = {
        "company_id": tcs["id"],
        "fiscal_year": 2024,
        "title": "TCS Automated Test Report FY2024"
    }
    response = client.post("/api/v1/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "pdf_url" in data
    assert "html_url" in data
    report_id = data["id"]

    # Test PDF download
    pdf_resp = client.get(f"/api/v1/reports/{report_id}/pdf")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
