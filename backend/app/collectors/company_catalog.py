from typing import List, Dict, Any, Optional

DEFAULT_COMPANY_CATALOG = [
    {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics & Software",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0000320193",
        "isin": "US0378331005",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://investor.apple.com",
        "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories, and sells a variety of related services."
    },
    {
        "ticker": "MSFT",
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software & Cloud Infrastructure",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0000789019",
        "isin": "US5949181045",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://www.microsoft.com/en-us/investor",
        "description": "Microsoft Corporation develops and supports software, services, devices and solutions worldwide, including Azure cloud, Office 365, and Windows."
    },
    {
        "ticker": "INFY",
        "name": "Infosys Limited",
        "sector": "Information Technology",
        "industry": "IT Consulting & Software Services",
        "exchange": "NSE / NYSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001067491",  # SEC EDGAR registered 20-F Filer!
        "isin": "INE009A01021",
        "nse_symbol": "INFY",
        "bse_code": "500209",
        "ir_url": "https://www.infosys.com/investors.html",
        "description": "Infosys Limited is an Indian multinational information technology company that provides business consulting, information technology and outsourcing services."
    },
    {
        "ticker": "TCS",
        "name": "Tata Consultancy Services Limited",
        "sector": "Information Technology",
        "industry": "IT Services & Consulting",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE467B01029",
        "nse_symbol": "TCS",
        "bse_code": "532540",
        "ir_url": "https://www.tcs.com/investor-relations",
        "description": "Tata Consultancy Services is an Indian multinational IT services and consulting company, flagship subsidiary of the Tata Group."
    },
    {
        "ticker": "RELIANCE",
        "name": "Reliance Industries Limited",
        "sector": "Energy & Telecommunications",
        "industry": "Oil to Chemicals, Retail & Digital Services",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE002A01018",
        "nse_symbol": "RELIANCE",
        "bse_code": "500325",
        "ir_url": "https://www.ril.com/investor-relations",
        "description": "Reliance Industries Limited is an Indian multinational conglomerate headquartered in Mumbai, with businesses spanning energy, petrochemicals, natural gas, retail, and telecommunications."
    },
    {
        "ticker": "HDFCBANK",
        "name": "HDFC Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001144967",  # SEC 20-F Filer
        "isin": "INE040A01034",
        "nse_symbol": "HDFCBANK",
        "bse_code": "500180",
        "ir_url": "https://www.hdfcbank.com/personal/about-us/investor-relations",
        "description": "HDFC Bank Limited is India's largest private sector bank by assets and market capitalization."
    }
]

class CompanyCatalogService:
    """
    Search and discovery service for public companies.
    """

    @classmethod
    def search(cls, query: str = "", exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        results = []
        for comp in DEFAULT_COMPANY_CATALOG:
            if exchange and exchange.upper() not in comp["exchange"].upper():
                continue
            if not q:
                results.append(comp)
                continue
            if (q in comp["ticker"].lower() or
                q in comp["name"].lower() or
                (comp.get("nse_symbol") and q in comp["nse_symbol"].lower()) or
                (comp.get("cik") and q in comp["cik"].lower()) or
                (comp.get("sector") and q in comp["sector"].lower())):
                results.append(comp)
        return results

    @classmethod
    def get_by_ticker(cls, ticker: str) -> Optional[Dict[str, Any]]:
        for comp in DEFAULT_COMPANY_CATALOG:
            if comp["ticker"].upper() == ticker.upper():
                return comp
        return None
