from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# ==========================================
# Company Schemas
# ==========================================
class CompanyBase(BaseModel):
    ticker: str = Field(..., description="Unique ticker symbol e.g. TCS")
    name: str = Field(..., description="Full legal company name")
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    currency: str = Field("INR", description="Financial currency code")
    units: str = Field("Crores", description="Units e.g. Crores, Millions")
    exchange: Optional[str] = "NSE"
    cik: Optional[str] = None
    isin: Optional[str] = None
    nse_symbol: Optional[str] = None
    bse_code: Optional[str] = None
    ir_url: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    units: Optional[str] = None
    exchange: Optional[str] = None
    cik: Optional[str] = None
    isin: Optional[str] = None
    nse_symbol: Optional[str] = None
    bse_code: Optional[str] = None
    ir_url: Optional[str] = None

class CompanyResponse(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Financial Data Schemas
# ==========================================
class FinancialDataBase(BaseModel):
    fiscal_year: int = Field(..., description="Reporting financial year e.g. 2024")
    period: str = Field("FY", description="FY, Q1, Q2, Q3, Q4")
    reporting_period_end: Optional[str] = None
    currency: str = "INR"
    units: str = "Crores"
    source: str = "Manual Entry"

    # Income Statement
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_profit: Optional[float] = None
    net_profit: Optional[float] = None
    eps: Optional[float] = None
    shares_outstanding: Optional[float] = None

    # Balance Sheet
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    shareholders_equity: Optional[float] = None
    debt: Optional[float] = None
    cash: Optional[float] = None

    # Cash Flow
    operating_cash_flow: Optional[float] = None
    capital_expenditures: Optional[float] = None
    free_cash_flow: Optional[float] = None

    is_audited: bool = True
    notes: Optional[str] = None

class FinancialDataCreate(FinancialDataBase):
    company_id: int

class FinancialDataUpdate(BaseModel):
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_profit: Optional[float] = None
    net_profit: Optional[float] = None
    eps: Optional[float] = None
    shares_outstanding: Optional[float] = None
    total_assets: Optional[float] = None
    current_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    current_liabilities: Optional[float] = None
    shareholders_equity: Optional[float] = None
    debt: Optional[float] = None
    cash: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capital_expenditures: Optional[float] = None
    free_cash_flow: Optional[float] = None
    source: Optional[str] = None
    is_audited: Optional[bool] = None
    notes: Optional[str] = None

class FinancialDataResponse(FinancialDataBase):
    id: int
    company_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class FinancialRatioSet(BaseModel):
    fiscal_year: int
    period: str
    revenue: Optional[float] = None
    net_profit: Optional[float] = None
    operating_profit: Optional[float] = None
    gross_profit: Optional[float] = None
    
    # Growth Ratios (%)
    revenue_growth_pct: Optional[float] = None
    net_profit_growth_pct: Optional[float] = None
    operating_profit_growth_pct: Optional[float] = None
    
    # Profitability Ratios (%)
    gross_profit_margin_pct: Optional[float] = None
    operating_profit_margin_pct: Optional[float] = None
    net_profit_margin_pct: Optional[float] = None
    return_on_assets_pct: Optional[float] = None
    return_on_equity_pct: Optional[float] = None

    # Solvency & Liquidity Ratios
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None

    # Cash Flow & Valuation
    operating_cash_flow: Optional[float] = None
    free_cash_flow: Optional[float] = None
    eps: Optional[float] = None
    ocf_to_net_income: Optional[float] = None

    # Metadata & Warnings
    missing_fields: List[str] = []
    warnings: List[str] = []
    units: str
    currency: str

class FinancialAnalysisResponse(BaseModel):
    company_id: int
    company_name: str
    ticker: str
    currency: str
    units: str
    years_available: List[int]
    ratios: List[FinancialRatioSet]
    summary_insights: List[str]
    missing_data_warnings: List[str]


# ==========================================
# ESG Data Schemas
# ==========================================
class ESGDataBase(BaseModel):
    fiscal_year: int
    reporting_period: str = "FY"
    source_document: Optional[str] = None

    # Environmental
    carbon_emissions_scope1: Optional[float] = None
    carbon_emissions_scope2: Optional[float] = None
    carbon_emissions_scope3: Optional[float] = None
    energy_consumption_gj: Optional[float] = None
    renewable_energy_pct: Optional[float] = None
    water_consumption_kl: Optional[float] = None
    water_recycled_pct: Optional[float] = None
    waste_generated_mt: Optional[float] = None
    waste_recycled_pct: Optional[float] = None

    # Social
    employee_count: Optional[int] = None
    female_workforce_pct: Optional[float] = None
    employee_turnover_pct: Optional[float] = None
    lost_time_injury_rate: Optional[float] = None
    training_hours_per_employee: Optional[float] = None
    csr_spending_amount: Optional[float] = None
    human_rights_policy: Optional[bool] = None

    # Governance
    board_size: Optional[int] = None
    independent_directors_pct: Optional[float] = None
    women_on_board_pct: Optional[float] = None
    ceo_chair_separation: Optional[bool] = None
    ethics_code_established: Optional[bool] = None
    whistleblower_mechanism: Optional[bool] = None
    anti_corruption_policy: Optional[bool] = None
    data_privacy_policy: Optional[bool] = None

    notes: Optional[str] = None

class ESGDataCreate(ESGDataBase):
    company_id: int

class ESGScoreBreakdown(BaseModel):
    environmental_score: Optional[float] = None
    social_score: Optional[float] = None
    governance_score: Optional[float] = None
    overall_esg_score: Optional[float] = None
    data_coverage_pct: float
    weights: Dict[str, float]
    indicator_scores: Dict[str, Any]
    formula_explanation: str
    methodology_limitations: List[str]
    is_sufficient_data: bool

class ESGDataResponse(ESGDataBase):
    id: int
    company_id: int
    environmental_score: Optional[float] = None
    social_score: Optional[float] = None
    governance_score: Optional[float] = None
    overall_esg_score: Optional[float] = None
    data_coverage_pct: Optional[float] = None
    score_breakdown_json: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Document & Chunk Schemas
# ==========================================
class DocumentResponse(BaseModel):
    id: int
    company_id: int
    title: str
    file_name: str
    file_size_bytes: int
    document_type: str
    fiscal_year: Optional[int] = None
    total_pages: int
    total_chunks: int
    status: str
    error_message: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DocumentChunkResponse(BaseModel):
    id: int
    document_id: int
    company_id: int
    fiscal_year: Optional[int]
    page_number: int
    section: str
    chunk_index: int
    chunk_id: str
    content: str
    token_count: int
    is_table: bool
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Query & RAG Schemas
# ==========================================
class CitationItem(BaseModel):
    document_title: str
    document_type: str
    fiscal_year: Optional[int] = None
    page_number: int
    section: str
    chunk_id: str
    relevance_score: Optional[float] = None
    snippet: str

class QueryRequest(BaseModel):
    query: str = Field(..., description="Financial or ESG question")
    company_id: Optional[int] = Field(None, description="Scope query to specific company")
    fiscal_year: Optional[int] = Field(None, description="Scope to specific year")
    top_k: int = Field(5, ge=1, le=20)
    enable_reranking: bool = True

class QueryResponse(BaseModel):
    query: str
    query_type: str  # FINANCIAL_CALCULATION, FINANCIAL_EXPLANATION, ESG, DOCUMENT, COMPARISON, COMBINED
    answer: str
    citations: List[CitationItem]
    deterministic_metrics: Optional[Dict[str, Any]] = None
    esg_summary: Optional[Dict[str, Any]] = None
    llm_provider: str
    grounded: bool
    warnings: List[str] = []


# ==========================================
# Report Generation Schemas
# ==========================================
class ReportGenerateRequest(BaseModel):
    company_id: int
    fiscal_year: int
    report_type: str = "Comprehensive Financial & ESG"
    title: Optional[str] = None
    include_ai_insights: bool = True

class GeneratedReportResponse(BaseModel):
    id: int
    company_id: int
    company_name: str
    fiscal_year: int
    title: str
    report_type: str
    pdf_url: Optional[str] = None
    html_url: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Automated Collection Schemas
# ==========================================
class CompanyDiscoveryItem(BaseModel):
    ticker: str
    name: str
    exchange: str
    sector: Optional[str] = None
    cik: Optional[str] = None
    isin: Optional[str] = None
    nse_symbol: Optional[str] = None
    bse_code: Optional[str] = None
    ir_url: Optional[str] = None
    currency: str
    units: str

class TriggerCollectionRequest(BaseModel):
    company_id: int
    sources: List[str] = Field(default=["SEC EDGAR", "NSE/BSE Filings", "Company IR"])
    fiscal_years: List[int] = Field(default=[2023, 2024, 2025])
    document_categories: List[str] = Field(default=["Annual Report", "Quarterly Report", "Sustainability Report / BRSR"])

class DataCollectionJobResponse(BaseModel):
    id: int
    company_id: int
    status: str
    sources_searched: str
    documents_discovered: int
    documents_downloaded: int
    financial_records_extracted: int
    esg_records_extracted: int
    successful_operations: int
    failed_operations: int
    validation_warnings_json: str
    logs: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class DiscoveredDocumentResponse(BaseModel):
    id: int
    company_id: int
    collection_job_id: Optional[int] = None
    title: str
    document_type: str
    fiscal_year: Optional[int] = None
    source_url: str
    source_name: str
    download_status: str
    file_size_bytes: int
    error_message: Optional[str] = None
    discovered_at: datetime
    model_config = ConfigDict(from_attributes=True)
