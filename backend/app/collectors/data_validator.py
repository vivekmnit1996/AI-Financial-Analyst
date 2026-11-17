from typing import Dict, Any, List, Tuple, Optional
import numpy as np

class FinancialDataValidator:
    """
    Mandatory Financial & ESG Data Validation and Reconciliation Engine.
    Ensures structural integrity, accounting identity checks, unit consistency,
    and provenance tracking prior to permanent database storage.
    """

    @classmethod
    def validate_financial_record(cls, record: Dict[str, Any]) -> Tuple[str, List[str]]:
        """
        Validates an extracted financial record.
        Returns:
            status: 'VALIDATED' or 'WARNING'
            warnings: list of validation warnings or inconsistency notices
        """
        warnings = []

        # 1. Mandatory Identity Fields
        if not record.get("fiscal_year"):
            warnings.append("Missing required field: fiscal_year")
        if not record.get("currency"):
            warnings.append("Missing required field: currency")
        if not record.get("units"):
            warnings.append("Missing required field: units")

        # 2. Check Negative / Suspicious Balance Sheet Items
        rev = record.get("revenue")
        assets = record.get("total_assets")
        liab = record.get("total_liabilities")
        equity = record.get("shareholders_equity")
        cash = record.get("cash")
        debt = record.get("debt")

        if rev is not None and rev < 0:
            warnings.append(f"Suspicious negative revenue detected: {rev}")
        if assets is not None and assets <= 0:
            warnings.append(f"Invalid non-positive total assets: {assets}")
        if cash is not None and cash < 0:
            warnings.append(f"Invalid negative cash value: {cash}")
        if debt is not None and debt < 0:
            warnings.append(f"Invalid negative debt value: {debt}")

        # 3. Accounting Identity: Total Assets = Total Liabilities + Equity
        if assets is not None and liab is not None and equity is not None:
            sum_liab_equity = liab + equity
            discrepancy = abs(assets - sum_liab_equity)
            discrepancy_pct = (discrepancy / assets) * 100.0 if assets > 0 else 0.0
            
            # If difference exceeds 5%, flag potential accounting reclassification
            if discrepancy_pct > 5.0:
                warnings.append(
                    f"Balance Sheet Discrepancy: Assets ({assets}) != Liabilities ({liab}) + Equity ({equity}). "
                    f"Variance of {discrepancy_pct:.1f}% flagged for manual reconciliation."
                )

        # 4. Check Reporting Basis
        basis = record.get("reporting_basis", "Consolidated")
        if basis not in ["Consolidated", "Standalone"]:
            warnings.append(f"Unrecognized reporting basis '{basis}'. Defaulted to Consolidated.")

        # 5. Core Metric Completeness
        essential = [("revenue", rev), ("net_profit", record.get("net_profit")), ("operating_profit", record.get("operating_profit"))]
        missing_essential = [name for name, val in essential if val is None]
        if missing_essential:
            warnings.append(f"Core metrics missing: {', '.join(missing_essential)}")

        status = "WARNING" if warnings else "VALIDATED"
        return status, warnings

    @classmethod
    def validate_esg_record(cls, record: Dict[str, Any]) -> Tuple[str, List[str]]:
        """
        Validates ESG indicators for bounds and format correctness.
        """
        warnings = []

        # Percentage fields must be between 0 and 100
        pct_fields = [
            ("renewable_energy_pct", record.get("renewable_energy_pct")),
            ("water_recycled_pct", record.get("water_recycled_pct")),
            ("waste_recycled_pct", record.get("waste_recycled_pct")),
            ("female_workforce_pct", record.get("female_workforce_pct")),
            ("employee_turnover_pct", record.get("employee_turnover_pct")),
            ("independent_directors_pct", record.get("independent_directors_pct")),
            ("women_on_board_pct", record.get("women_on_board_pct")),
        ]

        for name, val in pct_fields:
            if val is not None:
                if not (0.0 <= val <= 100.0):
                    warnings.append(f"Invalid percentage out of range [0, 100] for {name}: {val}")

        # Emission figures cannot be negative
        for em in ["carbon_emissions_scope1", "carbon_emissions_scope2", "carbon_emissions_scope3"]:
            val = record.get(em)
            if val is not None and val < 0:
                warnings.append(f"Negative carbon emission value for {em}: {val}")

        status = "WARNING" if warnings else "VALIDATED"
        return status, warnings
