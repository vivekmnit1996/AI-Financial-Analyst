import pytest
from backend.app.engine.financial_calculator import (
    safe_divide, calculate_growth_rate, FinancialCalculatorEngine
)
from backend.app.models.schema_models import FinancialData

def test_safe_divide():
    assert safe_divide(100, 20) == 5.0
    assert safe_divide(100, 0) is None
    assert safe_divide(None, 20) is None
    assert safe_divide(100, None) is None
    assert safe_divide(25, 100, multiplier=100.0) == 25.0

def test_calculate_growth_rate():
    # Regular positive growth
    assert calculate_growth_rate(120, 100) == 20.0
    # Contraction
    assert calculate_growth_rate(80, 100) == -20.0
    # Zero denominator
    assert calculate_growth_rate(100, 0) is None
    # None values
    assert calculate_growth_rate(None, 100) is None
    # Turnaround from negative base
    assert calculate_growth_rate(50, -50) == 200.0

def test_financial_calculator_engine():
    rec1 = FinancialData(
        id=1, company_id=1, fiscal_year=2023, period="FY",
        currency="INR", units="Crores", source="Test",
        revenue=1000.0, cost_of_revenue=600.0, gross_profit=400.0,
        operating_profit=250.0, net_profit=180.0,
        total_assets=1200.0, current_assets=700.0,
        total_liabilities=400.0, current_liabilities=300.0,
        shareholders_equity=800.0, debt=100.0, cash=150.0,
        operating_cash_flow=220.0, capital_expenditures=40.0, free_cash_flow=180.0,
        eps=18.0
    )

    rec2 = FinancialData(
        id=2, company_id=1, fiscal_year=2024, period="FY",
        currency="INR", units="Crores", source="Test",
        revenue=1200.0, cost_of_revenue=700.0, gross_profit=500.0,
        operating_profit=300.0, net_profit=210.0,
        total_assets=1400.0, current_assets=850.0,
        total_liabilities=450.0, current_liabilities=350.0,
        shareholders_equity=950.0, debt=80.0, cash=200.0,
        operating_cash_flow=260.0, capital_expenditures=50.0, free_cash_flow=210.0,
        eps=21.0
    )

    ratios = FinancialCalculatorEngine.compute_ratios_for_records([rec1, rec2])
    assert len(ratios) == 2

    # Year 1 checks
    r1 = ratios[0]
    assert r1["fiscal_year"] == 2023
    assert r1["operating_profit_margin_pct"] == 25.0
    assert r1["net_profit_margin_pct"] == 18.0
    assert r1["gross_profit_margin_pct"] == 40.0
    assert r1["revenue_growth_pct"] is None  # base period
    assert r1["debt_to_equity"] == 0.125 or r1["debt_to_equity"] == 0.12 or round(r1["debt_to_equity"], 2) == 0.12

    # Year 2 checks
    r2 = ratios[1]
    assert r2["fiscal_year"] == 2024
    assert r2["revenue_growth_pct"] == 20.0
    assert r2["net_profit_growth_pct"] == round(((210 - 180) / 180) * 100, 2)
    assert r2["operating_profit_margin_pct"] == 25.0
    assert r2["net_profit_margin_pct"] == 17.5
    # Average equity = (800 + 950) / 2 = 875 -> ROE = (210 / 875) * 100 = 24.0%
    assert r2["return_on_equity_pct"] == 24.0
    # Current ratio = 850 / 350 = 2.43
    assert r2["current_ratio"] == 2.43

    # Insights generation
    insights = FinancialCalculatorEngine.generate_analytical_insights(ratios)
    assert len(insights) > 0
    assert any("Revenue" in i for i in insights)
