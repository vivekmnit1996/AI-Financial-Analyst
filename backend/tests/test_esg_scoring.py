import pytest
from backend.app.engine.esg_scorer import TransparentESGScorer
from backend.app.models.schema_models import ESGData

def test_esg_sufficient_data_scoring():
    esg = ESGData(
        company_id=1,
        fiscal_year=2024,
        reporting_period="FY",
        renewable_energy_pct=60.0,
        water_recycled_pct=40.0,
        waste_recycled_pct=80.0,
        carbon_emissions_scope1=1000.0,
        carbon_emissions_scope2=2000.0,
        female_workforce_pct=36.0,
        training_hours_per_employee=40.0,
        lost_time_injury_rate=0.05,
        human_rights_policy=True,
        csr_spending_amount=100.0,
        independent_directors_pct=60.0,
        women_on_board_pct=30.0,
        ceo_chair_separation=True,
        ethics_code_established=True,
        whistleblower_mechanism=True,
        anti_corruption_policy=True,
        data_privacy_policy=True
    )

    result = TransparentESGScorer.evaluate_esg(esg)
    assert result["is_sufficient_data"] is True
    assert result["data_coverage_pct"] >= 90.0
    assert result["overall_esg_score"] is not None
    assert 50.0 <= result["overall_esg_score"] <= 100.0
    assert result["environmental_score"] is not None
    assert result["social_score"] is not None
    assert result["governance_score"] is not None
    assert "Academic / Project-Specific Rating" in result["methodology_limitations"][0]

def test_esg_insufficient_data():
    # Only 1 indicator disclosed out of 16 (< 30% coverage)
    sparse_esg = ESGData(
        company_id=1,
        fiscal_year=2024,
        reporting_period="FY",
        renewable_energy_pct=50.0
    )

    result = TransparentESGScorer.evaluate_esg(sparse_esg)
    assert result["is_sufficient_data"] is False
    assert result["overall_esg_score"] is None
    assert any("Insufficient data coverage" in lim for lim in result["methodology_limitations"])
