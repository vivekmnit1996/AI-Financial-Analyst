import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from backend.app.models.schema_models import FinancialData

def safe_divide(numerator: Optional[float], denominator: Optional[float], multiplier: float = 1.0) -> Optional[float]:
    """
    Safely divide two numbers handling None, NaN, and zero denominators.
    Does NOT silently convert missing values into zero.
    """
    if numerator is None or denominator is None:
        return None
    try:
        num = float(numerator)
        denom = float(denominator)
    except (ValueError, TypeError):
        return None
        
    if np.isnan(num) or np.isnan(denom):
        return None
    if denom == 0.0:
        return None
        
    result = (num / denom) * multiplier
    return round(float(result), 2)

def calculate_growth_rate(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    """
    Calculate percentage growth rate: ((Current - Previous) / abs(Previous)) * 100
    Properly handles negative base values and zero denominators.
    """
    if current is None or previous is None:
        return None
    try:
        curr = float(current)
        prev = float(previous)
    except (ValueError, TypeError):
        return None
        
    if np.isnan(curr) or np.isnan(prev):
        return None
    if prev == 0.0:
        return None
        
    growth = ((curr - prev) / abs(prev)) * 100.0
    return round(float(growth), 2)


class FinancialCalculatorEngine:
    """
    Deterministic Python / Pandas engine for financial ratio and trend calculations.
    Ensures zero reliance on LLMs for quantitative metrics.
    """

    @classmethod
    def compute_ratios_for_records(cls, records: List[FinancialData]) -> List[Dict[str, Any]]:
        """
        Takes raw financial records sorted by fiscal_year ascending and computes
        all financial ratios, historical comparisons, and data completeness warnings.
        """
        if not records:
            return []

        # Sort by fiscal_year ascending
        sorted_records = sorted(records, key=lambda x: (x.fiscal_year, x.period))
        
        ratio_results = []
        prev_record = None

        for idx, rec in enumerate(sorted_records):
            warnings = []
            missing_fields = []

            # Check core field availability
            core_fields = [
                ("revenue", rec.revenue),
                ("cost_of_revenue", rec.cost_of_revenue),
                ("gross_profit", rec.gross_profit),
                ("operating_profit", rec.operating_profit),
                ("net_profit", rec.net_profit),
                ("total_assets", rec.total_assets),
                ("shareholders_equity", rec.shareholders_equity),
                ("debt", rec.debt),
                ("cash", rec.cash),
                ("operating_cash_flow", rec.operating_cash_flow),
                ("eps", rec.eps)
            ]
            for name, val in core_fields:
                if val is None:
                    missing_fields.append(name)

            # Gross profit margin: (Gross Profit / Revenue) * 100
            # If gross profit not directly provided, check if revenue and cost_of_revenue are present
            effective_gross_profit = rec.gross_profit
            if effective_gross_profit is None and rec.revenue is not None and rec.cost_of_revenue is not None:
                effective_gross_profit = rec.revenue - rec.cost_of_revenue

            gross_margin = safe_divide(effective_gross_profit, rec.revenue, multiplier=100.0)
            if rec.revenue == 0.0:
                warnings.append("Revenue is zero; gross margin undefined.")

            # Operating profit margin: (Operating Profit / Revenue) * 100
            op_margin = safe_divide(rec.operating_profit, rec.revenue, multiplier=100.0)

            # Net profit margin: (Net Profit / Revenue) * 100
            net_margin = safe_divide(rec.net_profit, rec.revenue, multiplier=100.0)

            # ROA: (Net Profit / Total Assets) * 100
            # If previous assets available, use average total assets
            avg_assets = rec.total_assets
            if prev_record and prev_record.total_assets is not None and rec.total_assets is not None:
                avg_assets = (rec.total_assets + prev_record.total_assets) / 2.0
            roa = safe_divide(rec.net_profit, avg_assets, multiplier=100.0)

            # ROE: (Net Profit / Average Shareholders' Equity) * 100
            avg_equity = rec.shareholders_equity
            if prev_record and prev_record.shareholders_equity is not None and rec.shareholders_equity is not None:
                avg_equity = (rec.shareholders_equity + prev_record.shareholders_equity) / 2.0
            
            roe = None
            if avg_equity is not None:
                if avg_equity <= 0:
                    warnings.append("Negative or zero shareholders' equity; ROE distorted or negative.")
                roe = safe_divide(rec.net_profit, avg_equity, multiplier=100.0)

            # Debt-to-Equity: Total Debt / Shareholders' Equity
            dte = None
            if rec.shareholders_equity is not None and rec.debt is not None:
                if rec.shareholders_equity <= 0:
                    warnings.append("Negative shareholders equity encountered; Debt/Equity ratio not meaningful.")
                else:
                    dte = safe_divide(rec.debt, rec.shareholders_equity)

            # Current Ratio: Current Assets / Current Liabilities
            curr_ratio = None
            if rec.current_assets is not None and rec.current_liabilities is not None:
                curr_ratio = safe_divide(rec.current_assets, rec.current_liabilities)
            elif rec.current_assets is None or rec.current_liabilities is None:
                missing_fields.append("current_ratio (current assets/liabilities missing)")

            # Free Cash Flow: Operating Cash Flow - Capital Expenditures
            fcf = rec.free_cash_flow
            if fcf is None and rec.operating_cash_flow is not None and rec.capital_expenditures is not None:
                fcf = round(rec.operating_cash_flow - rec.capital_expenditures, 2)

            # Quality of Earnings: OCF / Net Profit
            ocf_to_ni = None
            if rec.operating_cash_flow is not None and rec.net_profit is not None:
                if rec.net_profit != 0:
                    ocf_to_ni = safe_divide(rec.operating_cash_flow, rec.net_profit)

            # Growth Rates (YoY)
            rev_growth = None
            pat_growth = None
            op_growth = None

            if prev_record is not None:
                rev_growth = calculate_growth_rate(rec.revenue, prev_record.revenue)
                pat_growth = calculate_growth_rate(rec.net_profit, prev_record.net_profit)
                op_growth = calculate_growth_rate(rec.operating_profit, prev_record.operating_profit)
            else:
                warnings.append(f"Base period FY{rec.fiscal_year}: YoY growth rates require a preceding fiscal year.")

            ratio_dict = {
                "fiscal_year": rec.fiscal_year,
                "period": rec.period,
                "revenue": rec.revenue,
                "gross_profit": effective_gross_profit,
                "operating_profit": rec.operating_profit,
                "net_profit": rec.net_profit,
                "total_assets": rec.total_assets,
                "shareholders_equity": rec.shareholders_equity,
                "debt": rec.debt,
                "cash": rec.cash,
                "operating_cash_flow": rec.operating_cash_flow,
                "free_cash_flow": fcf,
                "eps": rec.eps,
                # Computed ratios
                "revenue_growth_pct": rev_growth,
                "net_profit_growth_pct": pat_growth,
                "operating_profit_growth_pct": op_growth,
                "gross_profit_margin_pct": gross_margin,
                "operating_profit_margin_pct": op_margin,
                "net_profit_margin_pct": net_margin,
                "return_on_assets_pct": roa,
                "return_on_equity_pct": roe,
                "debt_to_equity": dte,
                "current_ratio": curr_ratio,
                "ocf_to_net_income": ocf_to_ni,
                # Metadata
                "missing_fields": missing_fields,
                "warnings": warnings,
                "units": rec.units,
                "currency": rec.currency,
                "source": rec.source
            }

            ratio_results.append(ratio_dict)
            prev_record = rec

        return ratio_results

    @classmethod
    def generate_analytical_insights(cls, ratios: List[Dict[str, Any]]) -> List[str]:
        """
        Generate deterministic analytical bullet points highlighting notable financial changes,
        margin expansions/contractions, leverage, and cash flow trends.
        """
        insights = []
        if not ratios:
            return ["No financial data available for analysis."]

        latest = ratios[-1]
        fy = latest["fiscal_year"]
        u = latest.get("units", "")
        c = latest.get("currency", "")

        # 1. Revenue & Growth
        if latest.get("revenue") is not None:
            rev_str = f"FY{fy} Revenue reached {c} {latest['revenue']:,.2f} {u}"
            if latest.get("revenue_growth_pct") is not None:
                direction = "grew by" if latest["revenue_growth_pct"] >= 0 else "declined by"
                rev_str += f" ({direction} {abs(latest['revenue_growth_pct']):.2f}% YoY)."
            else:
                rev_str += "."
            insights.append(rev_str)

        # 2. Operating & Net Margins
        if latest.get("operating_profit_margin_pct") is not None:
            insights.append(
                f"Operating Profit Margin stood at {latest['operating_profit_margin_pct']:.2f}% in FY{fy} "
                f"(Operating Profit: {c} {latest.get('operating_profit', 0):,.2f} {u})."
            )
        if latest.get("net_profit_margin_pct") is not None:
            insights.append(
                f"Net Profit Margin recorded at {latest['net_profit_margin_pct']:.2f}% (Net Profit: {c} {latest.get('net_profit', 0):,.2f} {u})."
            )

        # 3. Capital Efficiency (ROE & ROA)
        if latest.get("return_on_equity_pct") is not None:
            insights.append(f"Return on Equity (ROE) achieved {latest['return_on_equity_pct']:.2f}%.")
        if latest.get("return_on_assets_pct") is not None:
            insights.append(f"Return on Assets (ROA) was {latest['return_on_assets_pct']:.2f}%.")

        # 4. Solvency & Balance Sheet
        if latest.get("debt_to_equity") is not None:
            leverage_comment = "healthy/conservative" if latest["debt_to_equity"] < 1.0 else "elevated"
            insights.append(
                f"Debt-to-Equity ratio of {latest['debt_to_equity']:.2f} reflects {leverage_comment} financial leverage "
                f"(Total Debt: {c} {latest.get('debt', 0):,.2f} {u}, Equity: {c} {latest.get('shareholders_equity', 0):,.2f} {u})."
            )

        # 5. Cash Flow Quality
        if latest.get("operating_cash_flow") is not None:
            ocf_msg = f"Operating Cash Flow generated: {c} {latest['operating_cash_flow']:,.2f} {u}."
            if latest.get("free_cash_flow") is not None:
                ocf_msg += f" Free Cash Flow: {c} {latest['free_cash_flow']:,.2f} {u}."
            if latest.get("ocf_to_net_income") is not None:
                ocf_msg += f" OCF-to-Net-Income conversion ratio is {latest['ocf_to_net_income']:.2f}x."
            insights.append(ocf_msg)

        # 6. Multi-year trend (if >= 2 years)
        if len(ratios) >= 2:
            prev = ratios[-2]
            if latest.get("operating_profit_margin_pct") is not None and prev.get("operating_profit_margin_pct") is not None:
                delta_margin = round(latest["operating_profit_margin_pct"] - prev["operating_profit_margin_pct"], 2)
                verb = "expanded by" if delta_margin >= 0 else "contracted by"
                insights.append(
                    f"Operating margin {verb} {abs(delta_margin):.2f} percentage points compared to FY{prev['fiscal_year']} "
                    f"({prev['operating_profit_margin_pct']:.2f}% to {latest['operating_profit_margin_pct']:.2f}%)."
                )

        return insights
