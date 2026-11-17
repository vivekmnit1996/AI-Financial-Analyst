import logging
from typing import List, Dict, Any, Optional
import httpx

from backend.app.collectors.sec_edgar_connector import SecEdgarConnector

logger = logging.getLogger("company_catalog")

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
        "ticker": "NVDA",
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors & Accelerated Computing",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0001045810",
        "isin": "US67066G1040",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://investor.nvidia.com",
        "description": "NVIDIA Corporation pioneers GPU-accelerated computing and full-stack artificial intelligence computing infrastructure."
    },
    {
        "ticker": "TSLA",
        "name": "Tesla, Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Auto Manufacturers & Clean Energy",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0001318605",
        "isin": "US88160R1014",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://ir.tesla.com",
        "description": "Tesla, Inc. designs, manufactures, and sells electric vehicles, energy storage systems, and solar products."
    },
    {
        "ticker": "GOOGL",
        "name": "Alphabet Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0001652044",
        "isin": "US02079K3059",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://abc.xyz/investor",
        "description": "Alphabet Inc. is a multinational technology conglomerate holding company and the parent company of Google."
    },
    {
        "ticker": "AMZN",
        "name": "Amazon.com, Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Internet Retail & Cloud Infrastructure",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0001018724",
        "isin": "US0231351067",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://ir.aboutamazon.com",
        "description": "Amazon.com, Inc. focuses on e-commerce, cloud computing (AWS), online advertising, digital streaming, and artificial intelligence."
    },
    {
        "ticker": "META",
        "name": "Meta Platforms, Inc.",
        "sector": "Communication Services",
        "industry": "Social Media & Metaverse Technologies",
        "exchange": "NASDAQ",
        "currency": "USD",
        "units": "Millions",
        "cik": "0001326801",
        "isin": "US30303M1027",
        "nse_symbol": None,
        "bse_code": None,
        "ir_url": "https://investor.atmeta.com",
        "description": "Meta Platforms builds technologies that help people connect, find communities, and grow businesses across apps and mixed reality."
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
        "ticker": "INFY",
        "name": "Infosys Limited",
        "sector": "Information Technology",
        "industry": "IT Consulting & Software Services",
        "exchange": "NSE / NYSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001067491",  # SEC EDGAR registered 20-F Filer
        "isin": "INE009A01021",
        "nse_symbol": "INFY",
        "bse_code": "500209",
        "ir_url": "https://www.infosys.com/investors.html",
        "description": "Infosys Limited is an Indian multinational information technology company providing digital consulting, IT engineering and enterprise platforms."
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
        "description": "Reliance Industries Limited is an Indian conglomerate spanning petrochemicals, refining, retail, and telecommunications (Jio)."
    },
    {
        "ticker": "HDFCBANK",
        "name": "HDFC Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "exchange": "NSE / NYSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001144967",  # SEC 20-F Filer (ADR: HDB)
        "isin": "INE040A01034",
        "nse_symbol": "HDFCBANK",
        "bse_code": "500180",
        "ir_url": "https://www.hdfcbank.com/personal/about-us/investor-relations",
        "description": "HDFC Bank Limited is India's largest private sector banking and financial services institution by market capitalization."
    },
    {
        "ticker": "WIPRO",
        "name": "Wipro Limited",
        "sector": "Information Technology",
        "industry": "IT Services & Business Process",
        "exchange": "NSE / NYSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001123799",  # SEC 20-F Filer (ADR: WIT)
        "isin": "INE075A01022",
        "nse_symbol": "WIPRO",
        "bse_code": "507685",
        "ir_url": "https://www.wipro.com/investors",
        "description": "Wipro Limited is a global provider of information technology, consulting, and business process services."
    },
    {
        "ticker": "TATAMOTORS",
        "name": "Tata Motors Limited",
        "sector": "Automotive",
        "industry": "Commercial & Passenger Vehicles",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0000926042",
        "isin": "INE155A01022",
        "nse_symbol": "TATAMOTORS",
        "bse_code": "500570",
        "ir_url": "https://www.tatamotors.com/investors",
        "description": "Tata Motors Limited is a leading multinational automotive manufacturer and owner of Jaguar Land Rover (JLR)."
    },
    {
        "ticker": "ICICIBANK",
        "name": "ICICI Bank Limited",
        "sector": "Financial Services",
        "industry": "Private Sector Banking",
        "exchange": "NSE / NYSE",
        "currency": "INR",
        "units": "Crores",
        "cik": "0001103838",
        "isin": "INE090A01021",
        "nse_symbol": "ICICIBANK",
        "bse_code": "532174",
        "ir_url": "https://www.icicibank.com/about-us/investor-relations",
        "description": "ICICI Bank is a prominent Indian multinational bank and financial services company."
    },
    {
        "ticker": "SBIN",
        "name": "State Bank of India",
        "sector": "Financial Services",
        "industry": "Public Sector Banking",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE062A01020",
        "nse_symbol": "SBIN",
        "bse_code": "500112",
        "ir_url": "https://sbi.co.in/web/investor-relations",
        "description": "State Bank of India is a Fortune 500 public sector bank and the largest commercial banking enterprise in India."
    },
    {
        "ticker": "BHARTIARTL",
        "name": "Bharti Airtel Limited",
        "sector": "Telecommunications",
        "industry": "Wireless & Digital Telecom Services",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE397D01024",
        "nse_symbol": "BHARTIARTL",
        "bse_code": "532454",
        "ir_url": "https://www.airtel.in/about-bharti/equity",
        "description": "Bharti Airtel Limited is a leading global telecommunications company operating across 18 countries in South Asia and Africa."
    },
    {
        "ticker": "ITC",
        "name": "ITC Limited",
        "sector": "Consumer Goods",
        "industry": "FMCG, Hotels & Paperboards",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE154A01025",
        "nse_symbol": "ITC",
        "bse_code": "500875",
        "ir_url": "https://www.itcportal.com/investor",
        "description": "ITC Limited is a diversified Indian conglomerate with businesses in FMCG, Hotels, Packaging, Agri-Business, and IT."
    },
    {
        "ticker": "LT",
        "name": "Larsen & Toubro Limited",
        "sector": "Industrials",
        "industry": "Engineering & Infrastructure",
        "exchange": "NSE",
        "currency": "INR",
        "units": "Crores",
        "cik": None,
        "isin": "INE018A01030",
        "nse_symbol": "LT",
        "bse_code": "500510",
        "ir_url": "https://www.larsentoubro.com/investors",
        "description": "Larsen & Toubro is an Indian multinational engaged in engineering, procurement, construction projects, and manufacturing."
    }
]

class CompanyCatalogService:
    """
    Automated company discovery and catalog service.
    Integrates live external discovery from Yahoo Finance Search API,
    SEC EDGAR 10,400+ registrant directory, and benchmark exchange catalogs.
    """

    @classmethod
    def search(cls, query: str = "", exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        results_map: Dict[str, Dict[str, Any]] = {}

        # 1. Match from Curated Benchmark Catalog
        for comp in DEFAULT_COMPANY_CATALOG:
            if exchange and exchange.upper() not in comp["exchange"].upper():
                continue
            if not q:
                results_map[comp["ticker"].upper()] = comp
                continue
            if (q in comp["ticker"].lower() or
                q in comp["name"].lower() or
                (comp.get("nse_symbol") and q in comp["nse_symbol"].lower()) or
                (comp.get("cik") and q in comp["cik"].lower()) or
                (comp.get("sector") and q in comp["sector"].lower())):
                results_map[comp["ticker"].upper()] = comp

        # If query is empty, return curated results
        if not q:
            return list(results_map.values())

        # 2. Dynamic Discovery via Yahoo Finance Search API
        try:
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=12&newsCount=0"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(url, headers=headers)
                if resp.status_code == 200:
                    quotes = resp.json().get("quotes", [])
                    for quote in quotes:
                        symbol = quote.get("symbol", "").strip()
                        quote_type = quote.get("quoteType", "")
                        if not symbol or quote_type not in ["EQUITY", ""]:
                            continue

                        # Check Indian market listing
                        is_indian = (
                            symbol.endswith(".NS") or
                            symbol.endswith(".BO") or
                            quote.get("exchDisp") in ["NSE", "BSE", "Bombay"]
                        )

                        if is_indian:
                            clean_ticker = symbol.replace(".NS", "").replace(".BO", "")
                            exch = "NSE" if (".NS" in symbol or "NSE" in quote.get("exchDisp", "")) else "BSE"
                            curr = "INR"
                            unit = "Crores"
                            nse_s = clean_ticker if exch == "NSE" else None
                            bse_c = None
                        else:
                            clean_ticker = symbol
                            exch = quote.get("exchDisp") or quote.get("exchange") or "NASDAQ/NYSE"
                            curr = "USD"
                            unit = "Millions"
                            nse_s = None
                            bse_c = None

                        if clean_ticker.upper() in results_map:
                            continue

                        # Check exchange filter if requested
                        if exchange and exchange.upper() not in exch.upper():
                            continue

                        cik = SecEdgarConnector.resolve_ticker_to_cik(clean_ticker)

                        name = quote.get("longname") or quote.get("shortname") or clean_ticker
                        sector = quote.get("sector") or "Diversified"
                        industry = quote.get("industry") or "General Industry"

                        results_map[clean_ticker.upper()] = {
                            "ticker": clean_ticker,
                            "name": name,
                            "sector": sector,
                            "industry": industry,
                            "exchange": exch,
                            "currency": curr,
                            "units": unit,
                            "cik": cik,
                            "isin": None,
                            "nse_symbol": nse_s,
                            "bse_code": bse_c,
                            "ir_url": f"https://finance.yahoo.com/quote/{symbol}",
                            "description": f"{name} is a publicly traded corporation listed on {exch}."
                        }
        except Exception as e:
            logger.warning(f"Live Yahoo search query failed for '{query}': {e}")

        # 3. Dynamic Discovery via SEC EDGAR Registrants Directory
        try:
            if SecEdgarConnector._CIK_CACHE:
                q_up = q.upper()
                sec_matches = 0
                for sec_ticker, cik_val in SecEdgarConnector._CIK_CACHE.items():
                    if q_up in sec_ticker and sec_ticker not in results_map:
                        if exchange and "SEC" not in exchange.upper() and "NASDAQ" not in exchange.upper() and "NYSE" not in exchange.upper():
                            continue
                        results_map[sec_ticker] = {
                            "ticker": sec_ticker,
                            "name": f"{sec_ticker} Inc. / SEC Registrant",
                            "sector": "Public Corporate Filer",
                            "industry": "Commercial & Industrial",
                            "exchange": "SEC / US Markets",
                            "currency": "USD",
                            "units": "Millions",
                            "cik": cik_val,
                            "isin": None,
                            "nse_symbol": None,
                            "bse_code": None,
                            "ir_url": f"https://www.sec.gov/edgar/browse/?CIK={cik_val}",
                            "description": f"{sec_ticker} is an SEC EDGAR registered reporting issuer."
                        }
                        sec_matches += 1
                        if sec_matches >= 5:
                            break
        except Exception as e:
            logger.warning(f"SEC directory lookup error: {e}")

        return list(results_map.values())

    @classmethod
    def get_by_ticker(cls, ticker: str) -> Optional[Dict[str, Any]]:
        clean = ticker.strip().upper().replace(".NS", "").replace(".BO", "")
        
        # 1. Curated benchmark check
        for comp in DEFAULT_COMPANY_CATALOG:
            if comp["ticker"].upper() == clean:
                return comp

        # 2. Query SEC CIK mapping
        cik = SecEdgarConnector.resolve_ticker_to_cik(clean)

        # 3. Query Yahoo Finance search for metadata
        try:
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={clean}&quotesCount=5&newsCount=0"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            with httpx.Client(timeout=5.0) as client:
                resp = client.get(url, headers=headers)
                if resp.status_code == 200:
                    quotes = resp.json().get("quotes", [])
                    for q in quotes:
                        sym = q.get("symbol", "").upper()
                        if sym == clean or sym == f"{clean}.NS" or sym == f"{clean}.BO":
                            is_indian = sym.endswith(".NS") or sym.endswith(".BO") or q.get("exchDisp") in ["NSE", "BSE"]
                            exch = "NSE" if is_indian else (q.get("exchDisp") or "NASDAQ/NYSE")
                            curr = "INR" if is_indian else "USD"
                            unit = "Crores" if is_indian else "Millions"
                            name = q.get("longname") or q.get("shortname") or clean
                            return {
                                "ticker": clean,
                                "name": name,
                                "sector": q.get("sector") or "Diversified",
                                "industry": q.get("industry") or "General Industry",
                                "exchange": exch,
                                "currency": curr,
                                "units": unit,
                                "cik": cik,
                                "isin": None,
                                "nse_symbol": clean if is_indian else None,
                                "bse_code": None,
                                "ir_url": f"https://finance.yahoo.com/quote/{q.get('symbol')}",
                                "description": f"{name} is a publicly traded corporation listed on {exch}."
                            }
        except Exception as e:
            logger.warning(f"Live lookup for ticker '{ticker}' failed: {e}")

        # 4. Fallback synthesis for searched ticker
        curr = "USD" if cik else "INR"
        unit = "Millions" if curr == "USD" else "Crores"
        exch = "NASDAQ/NYSE" if curr == "USD" else "NSE"

        return {
            "ticker": clean,
            "name": f"{clean} Corporation",
            "sector": "Diversified Commercial Enterprise",
            "industry": "Corporate Operations",
            "exchange": exch,
            "currency": curr,
            "units": unit,
            "cik": cik,
            "isin": None,
            "nse_symbol": clean if curr == "INR" else None,
            "bse_code": None,
            "ir_url": f"https://finance.yahoo.com/quote/{clean}",
            "description": f"{clean} Corporation is a publicly listed enterprise."
        }
