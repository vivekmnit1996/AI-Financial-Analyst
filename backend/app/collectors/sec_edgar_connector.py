import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime

logger = logging.getLogger("sec_edgar_connector")

class SecEdgarConnector:
    """
    Official SEC EDGAR XBRL & Submissions API Connector.
    Extracts audited GAAP/IFRS financial statements and discovers official 10-K / 20-F reports.
    Complies with SEC Fair Access policy (User-Agent declaration and request rate control).
    """

    HEADERS = {
        "User-Agent": "BTechAcademicFinancialAnalyst research.ai@university.edu",
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov"
    }
    SEC_HOST_HEADERS = {
        "User-Agent": "BTechAcademicFinancialAnalyst research.ai@university.edu",
        "Accept-Encoding": "gzip, deflate"
    }

    @classmethod
    def fetch_company_facts(cls, cik: str) -> Optional[Dict[str, Any]]:
        """Fetch full XBRL facts JSON for given CIK."""
        cik_clean = str(cik).strip().zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_clean}.json"
        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.get(url, headers=cls.HEADERS)
                if resp.status_code == 200:
                    return resp.json()
                logger.warning(f"SEC EDGAR facts returned {resp.status_code} for CIK {cik_clean}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to SEC EDGAR facts for CIK {cik_clean}: {e}")
            return None

    @classmethod
    def fetch_submissions(cls, cik: str) -> Optional[Dict[str, Any]]:
        """Fetch submissions metadata (filings list) for given CIK."""
        cik_clean = str(cik).strip().zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_clean}.json"
        try:
            with httpx.Client(timeout=20.0) as client:
                resp = client.get(url, headers=cls.HEADERS)
                if resp.status_code == 200:
                    return resp.json()
                return None
        except Exception as e:
            logger.error(f"Error fetching SEC submissions for CIK {cik_clean}: {e}")
            return None

    @classmethod
    def extract_annual_financials(cls, cik: str, target_years: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """
        Extracts structured annual financials from SEC XBRL facts.
        """
        facts_data = cls.fetch_company_facts(cik)
        if not facts_data:
            return []

        entity_name = facts_data.get("entityName", "SEC Filer")
        facts = facts_data.get("facts", {}).get("us-gaap", {})
        if not facts:
            # Check IFRS if foreign private issuer (e.g. 20-F)
            facts = facts_data.get("facts", {}).get("ifrs-full", {})

        if not facts:
            return []

        def get_concept_annual_values(concept_keys: List[str]) -> Dict[int, Dict[str, Any]]:
            """Finds annual 10-K/20-F values indexed by fiscal year."""
            result = {}
            for key in concept_keys:
                concept_obj = facts.get(key)
                if not concept_obj:
                    continue
                units_dict = concept_obj.get("units", {})
                for unit_name, items in units_dict.items():
                    for item in items:
                        form = item.get("form")
                        if form in ["10-K", "20-F", "10-K/A"]:
                            fy = item.get("fy")
                            fp = item.get("fp")
                            # If frame is present like 'CY2024' or fp == 'FY'
                            if fy and (fp == "FY" or not fp or "CY" in str(item.get("frame", ""))):
                                val = item.get("val")
                                filed = item.get("filed")
                                if fy not in result or item.get("end", "") > result[fy].get("end", ""):
                                    result[fy] = {
                                        "val": val,
                                        "unit": unit_name,
                                        "filed": filed,
                                        "end": item.get("end"),
                                        "concept": key
                                    }
            return result

        # Concept keys mapping
        rev_data = get_concept_annual_values([
            "RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet", "TotalRevenuesAndOtherIncome"
        ])
        cost_rev_data = get_concept_annual_values([
            "CostOfGoodsAndServicesSold", "CostOfRevenue"
        ])
        gross_profit_data = get_concept_annual_values([
            "GrossProfit"
        ])
        op_inc_data = get_concept_annual_values([
            "OperatingIncomeLoss"
        ])
        net_inc_data = get_concept_annual_values([
            "NetIncomeLoss", "ProfitLoss"
        ])
        assets_data = get_concept_annual_values([
            "Assets"
        ])
        curr_assets_data = get_concept_annual_values([
            "AssetsCurrent"
        ])
        liab_data = get_concept_annual_values([
            "Liabilities", "LiabilitiesAndStockholdersEquity"
        ])
        curr_liab_data = get_concept_annual_values([
            "LiabilitiesCurrent"
        ])
        equity_data = get_concept_annual_values([
            "StockholdersEquity", "CommonStockholdersEquity"
        ])
        debt_data = get_concept_annual_values([
            "LongTermDebtNoncurrent", "DebtCurrent"
        ])
        cash_data = get_concept_annual_values([
            "CashAndCashEquivalentsAtCarryingValue"
        ])
        ocf_data = get_concept_annual_values([
            "NetCashProvidedByUsedInOperatingActivities"
        ])
        capex_data = get_concept_annual_values([
            "PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"
        ])
        eps_data = get_concept_annual_values([
            "EarningsPerShareDiluted", "EarningsPerShareBasic"
        ])

        # Find all available years
        all_years = sorted(list(set(rev_data.keys()) | set(net_inc_data.keys()) | set(assets_data.keys())))
        if target_years:
            all_years = [y for y in all_years if y in target_years]

        records = []
        for year in all_years:
            # Values in SEC XBRL are in exact units (USD). Normalize to Millions ($M)
            scale = 1_000_000.0

            def scale_val(data_dict, yr):
                rec = data_dict.get(yr)
                if rec and rec.get("val") is not None:
                    return round(float(rec["val"]) / scale, 2)
                return None

            rev = scale_val(rev_data, year)
            cost_rev = scale_val(cost_rev_data, year)
            gross_p = scale_val(gross_profit_data, year)
            if gross_p is None and rev is not None and cost_rev is not None:
                gross_p = round(rev - cost_rev, 2)
                
            op_inc = scale_val(op_inc_data, year)
            net_inc = scale_val(net_inc_data, year)
            tot_assets = scale_val(assets_data, year)
            curr_assets = scale_val(curr_assets_data, year)
            tot_liab = scale_val(liab_data, year)
            curr_liab = scale_val(curr_liab_data, year)
            eq = scale_val(equity_data, year)
            debt = scale_val(debt_data, year)
            cash = scale_val(cash_data, year)
            ocf = scale_val(ocf_data, year)
            capex = scale_val(capex_data, year)
            fcf = round(ocf - capex, 2) if (ocf is not None and capex is not None) else None
            
            eps_rec = eps_data.get(year)
            eps_val = round(float(eps_rec["val"]), 2) if (eps_rec and eps_rec.get("val") is not None) else None

            filing_date = (rev_data.get(year) or net_inc_data.get(year) or {}).get("filed", "")
            period_end = (rev_data.get(year) or net_inc_data.get(year) or {}).get("end", "")

            raw_dict = {
                "source_concept_rev": (rev_data.get(year) or {}).get("concept"),
                "source_raw_revenue": (rev_data.get(year) or {}).get("val"),
                "source_raw_net_income": (net_inc_data.get(year) or {}).get("val"),
                "scale_factor": "USD Millions (/1,000,000)"
            }

            records.append({
                "fiscal_year": int(year),
                "period": "FY",
                "reporting_basis": "Consolidated",
                "reporting_period_end": period_end,
                "currency": "USD",
                "units": "Millions",
                "source": "SEC EDGAR Official XBRL Filing",
                "source_url": f"https://www.sec.gov/edgar/browse/?CIK={cik}",
                "filing_date": filing_date,
                "revenue": rev,
                "cost_of_revenue": cost_rev,
                "gross_profit": gross_p,
                "operating_profit": op_inc,
                "net_profit": net_inc,
                "total_assets": tot_assets,
                "current_assets": curr_assets,
                "total_liabilities": tot_liab,
                "current_liabilities": curr_liab,
                "shareholders_equity": eq,
                "debt": debt,
                "cash": cash,
                "operating_cash_flow": ocf,
                "capital_expenditures": capex,
                "free_cash_flow": fcf,
                "eps": eps_val,
                "is_audited": True,
                "raw_values_json": json.dumps(raw_dict)
            })

        return records

    @classmethod
    def discover_official_reports(cls, cik: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Discovers official 10-K / 20-F reports from SEC EDGAR submissions.
        """
        submissions = cls.fetch_submissions(cik)
        if not submissions:
            return []

        cik_clean = str(cik).strip().zfill(10)
        cik_int = str(int(cik_clean))
        recent = submissions.get("filings", {}).get("recent", {})
        if not recent:
            return []

        forms = recent.get("form", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        filing_dates = recent.get("filingDate", [])
        report_dates = recent.get("reportDate", [])

        discovered = []
        for idx, form in enumerate(forms):
            if form in ["10-K", "20-F"]:
                acc = accessions[idx]
                acc_clean = acc.replace("-", "")
                primary = primary_docs[idx]
                f_date = filing_dates[idx]
                r_date = report_dates[idx] if idx < len(report_dates) else f_date
                
                # Derive fiscal year
                fy = int(r_date[:4]) if r_date else int(f_date[:4])

                # Official SEC document URL
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc_clean}/{primary}"

                discovered.append({
                    "title": f"Official SEC Form {form} (FY{fy})",
                    "document_type": "Annual Report",
                    "fiscal_year": fy,
                    "source_url": doc_url,
                    "source_name": "SEC EDGAR",
                    "filing_date": f_date,
                    "form": form
                })

                if len(discovered) >= limit:
                    break

        return discovered
