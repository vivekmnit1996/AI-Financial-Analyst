import pytest
from backend.app.collectors.company_catalog import CompanyCatalogService
from backend.app.collectors.sec_edgar_connector import SecEdgarConnector
from backend.app.collectors.exchange_connector import ExchangeConnector
from backend.app.collectors.data_validator import FinancialDataValidator
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.models.schema_models import ESGData, Company
from backend.app.rag.sample_document_generator import SampleDocumentGenerator
import os

def test_company_catalog_search_dynamic():
    """Verify that catalog search handles arbitrary searches and returns standardized discovery items."""
    # Test query for US equity
    tesla_results = CompanyCatalogService.search("Tesla")
    assert len(tesla_results) >= 1
    tickers = [r["ticker"].upper() for r in tesla_results]
    assert "TSLA" in tickers
    tsla_item = next(r for r in tesla_results if r["ticker"].upper() == "TSLA")
    assert tsla_item["currency"] == "USD"
    assert tsla_item["exchange"] in ["NASDAQ", "NASDAQ/NYSE", "SEC / US Markets"]

    # Test query for Indian equity
    tata_results = CompanyCatalogService.search("Tata")
    assert len(tata_results) >= 1
    assert any("TCS" in r["ticker"].upper() or "TATA" in r["ticker"].upper() for r in tata_results)

    # Test empty query returns default bluechips
    all_default = CompanyCatalogService.search("")
    assert len(all_default) >= 15

def test_company_catalog_get_by_ticker():
    """Verify dynamic resolution of company metadata for known and novel tickers."""
    # Benchmark Indian
    tcs = CompanyCatalogService.get_by_ticker("TCS")
    assert tcs is not None
    assert tcs["ticker"] == "TCS"
    assert tcs["currency"] == "INR"

    # US Mega-cap
    nvda = CompanyCatalogService.get_by_ticker("NVDA")
    assert nvda is not None
    assert nvda["ticker"] == "NVDA"
    assert nvda["cik"] == "0001045810"

    # Dynamic / Novel ticker
    arbitrary = CompanyCatalogService.get_by_ticker("GLOBALTECH")
    assert arbitrary is not None
    assert arbitrary["ticker"] == "GLOBALTECH"
    assert arbitrary["name"] is not None

def test_sec_edgar_cik_resolution():
    """Verify that SEC EDGAR dynamic directory resolves 10-digit CIK codes."""
    assert SecEdgarConnector.resolve_ticker_to_cik("AAPL") == "0000320193"
    assert SecEdgarConnector.resolve_ticker_to_cik("MSFT") == "0000789019"
    assert SecEdgarConnector.resolve_ticker_to_cik("TSLA") == "0001318605"
    assert SecEdgarConnector.resolve_ticker_to_cik("NVDA") == "0001045810"
    assert SecEdgarConnector.resolve_ticker_to_cik("INFY") == "0001067491"

def test_exchange_connector_verified_and_dynamic():
    """Verify financial extraction and accounting equation for verified and dynamic companies."""
    # 1. Verified benchmark: RELIANCE
    ril_filings = ExchangeConnector.get_company_filings("RELIANCE", target_years=[2023, 2024])
    assert len(ril_filings) == 2
    for f in ril_filings:
        status, warnings = FinancialDataValidator.validate_financial_record(f)
        assert status == "VALIDATED"
        assert len(warnings) == 0
        assert f["total_assets"] == pytest.approx(f["total_liabilities"] + f["shareholders_equity"], rel=1e-3)

    # 2. Dynamic ticker: SBIN
    sbin_filings = ExchangeConnector.get_company_filings("SBIN", target_years=[2023, 2024, 2025])
    assert len(sbin_filings) == 3
    for f in sbin_filings:
        status, warnings = FinancialDataValidator.validate_financial_record(f)
        assert status == "VALIDATED"
        assert len(warnings) == 0
        assert f["total_assets"] == pytest.approx(f["total_liabilities"] + f["shareholders_equity"], rel=1e-3)

def test_exchange_connector_esg_scoring():
    """Verify ESG disclosures pass validation and score with high data coverage."""
    for sym in ["RELIANCE", "WIPRO", "TATAMOTORS", "SBIN"]:
        esg_dict = ExchangeConnector.get_esg_disclosures(sym)
        assert esg_dict is not None
        status, warnings = FinancialDataValidator.validate_esg_record(esg_dict)
        assert status == "VALIDATED"
        assert len(warnings) == 0

        # Score ESG
        esg_obj = ESGData(**esg_dict)
        score_res = TransparentESGScorer.evaluate_esg(esg_obj)
        assert score_res["is_sufficient_data"] is True
        assert score_res["data_coverage_pct"] >= 75.0
        assert 0.0 <= score_res["overall_esg_score"] <= 100.0

def test_sample_document_generator_dynamic():
    """Verify that multi-page report PDF is generated without error."""
    mock_company = Company(
        id=999,
        ticker="TESTCOMP",
        name="Test Corporation",
        sector="Technology",
        industry="Enterprise Software",
        currency="USD",
        units="Millions",
        exchange="NASDAQ"
    )
    pdf_path = SampleDocumentGenerator.generate_or_get_report_for_company(mock_company, recreate=True)
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 1000
