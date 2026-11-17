from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from backend.app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(32), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    sector = Column(String(128), nullable=True)
    industry = Column(String(128), nullable=True)
    description = Column(Text, nullable=True)
    currency = Column(String(10), default="INR", nullable=False)
    units = Column(String(32), default="Crores", nullable=False)
    
    # Identification & Exchange metadata
    exchange = Column(String(32), default="NSE", nullable=True)  # NSE, BSE, NASDAQ, NYSE
    cik = Column(String(16), nullable=True, index=True)          # SEC CIK e.g. 0000320193
    isin = Column(String(32), nullable=True)                     # ISIN code
    nse_symbol = Column(String(32), nullable=True)               # e.g. TCS
    bse_code = Column(String(32), nullable=True)                 # e.g. 532540
    ir_url = Column(String(512), nullable=True)                  # Investor relations portal

    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Relationships
    financials = relationship("FinancialData", back_populates="company", cascade="all, delete-orphan")
    esg_records = relationship("ESGData", back_populates="company", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="company", cascade="all, delete-orphan")
    reports = relationship("GeneratedReport", back_populates="company", cascade="all, delete-orphan")
    collection_jobs = relationship("DataCollectionJob", back_populates="company", cascade="all, delete-orphan")
    discovered_docs = relationship("DiscoveredDocument", back_populates="company", cascade="all, delete-orphan")


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=False, index=True)
    period = Column(String(16), default="FY", nullable=False)  # FY, Q1, Q2, Q3, Q4
    reporting_period_end = Column(String(32), nullable=True)  # e.g. 2024-03-31
    reporting_basis = Column(String(32), default="Consolidated", nullable=False)  # Consolidated / Standalone
    currency = Column(String(10), default="INR", nullable=False)
    units = Column(String(32), default="Crores", nullable=False)
    source = Column(String(128), default="Manual Entry", nullable=False)
    source_url = Column(String(512), nullable=True)
    filing_date = Column(String(32), nullable=True)
    extraction_timestamp = Column(DateTime, default=utcnow)

    # Income Statement
    revenue = Column(Float, nullable=True)
    cost_of_revenue = Column(Float, nullable=True)
    gross_profit = Column(Float, nullable=True)
    operating_profit = Column(Float, nullable=True)
    net_profit = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)
    shares_outstanding = Column(Float, nullable=True)

    # Balance Sheet
    total_assets = Column(Float, nullable=True)
    current_assets = Column(Float, nullable=True)
    total_liabilities = Column(Float, nullable=True)
    current_liabilities = Column(Float, nullable=True)
    shareholders_equity = Column(Float, nullable=True)
    debt = Column(Float, nullable=True)
    cash = Column(Float, nullable=True)

    # Cash Flow
    operating_cash_flow = Column(Float, nullable=True)
    capital_expenditures = Column(Float, nullable=True)
    free_cash_flow = Column(Float, nullable=True)

    # Validation & Provenance
    is_audited = Column(Boolean, default=True)
    validation_status = Column(String(32), default="VALIDATED")  # VALIDATED, WARNING, RECONCILED
    validation_notes = Column(Text, nullable=True)
    raw_values_json = Column(Text, nullable=True)  # Stores original unnormalized values and units
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint("company_id", "fiscal_year", "period", "reporting_basis", name="uq_company_year_period_basis"),
    )

    company = relationship("Company", back_populates="financials")


class ESGData(Base):
    __tablename__ = "esg_data"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=False, index=True)
    reporting_period = Column(String(16), default="FY", nullable=False)
    source_document = Column(String(255), nullable=True)
    source_url = Column(String(512), nullable=True)
    extraction_timestamp = Column(DateTime, default=utcnow)

    # Environmental Indicators
    carbon_emissions_scope1 = Column(Float, nullable=True)  # MT CO2e
    carbon_emissions_scope2 = Column(Float, nullable=True)  # MT CO2e
    carbon_emissions_scope3 = Column(Float, nullable=True)  # MT CO2e
    energy_consumption_gj = Column(Float, nullable=True)    # Gigajoules
    renewable_energy_pct = Column(Float, nullable=True)     # 0 - 100%
    water_consumption_kl = Column(Float, nullable=True)     # Kiloliters
    water_recycled_pct = Column(Float, nullable=True)       # 0 - 100%
    waste_generated_mt = Column(Float, nullable=True)       # Metric Tonnes
    waste_recycled_pct = Column(Float, nullable=True)       # 0 - 100%

    # Social Indicators
    employee_count = Column(Integer, nullable=True)
    female_workforce_pct = Column(Float, nullable=True)     # 0 - 100%
    employee_turnover_pct = Column(Float, nullable=True)    # 0 - 100%
    lost_time_injury_rate = Column(Float, nullable=True)    # per million hours
    training_hours_per_employee = Column(Float, nullable=True)
    csr_spending_amount = Column(Float, nullable=True)
    human_rights_policy = Column(Boolean, nullable=True)

    # Governance Indicators
    board_size = Column(Integer, nullable=True)
    independent_directors_pct = Column(Float, nullable=True) # 0 - 100%
    women_on_board_pct = Column(Float, nullable=True)        # 0 - 100%
    ceo_chair_separation = Column(Boolean, nullable=True)
    ethics_code_established = Column(Boolean, nullable=True)
    whistleblower_mechanism = Column(Boolean, nullable=True)
    anti_corruption_policy = Column(Boolean, nullable=True)
    data_privacy_policy = Column(Boolean, nullable=True)

    # Project-Specific Computed Scores
    environmental_score = Column(Float, nullable=True)
    social_score = Column(Float, nullable=True)
    governance_score = Column(Float, nullable=True)
    overall_esg_score = Column(Float, nullable=True)
    data_coverage_pct = Column(Float, nullable=True)
    score_breakdown_json = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    __table_args__ = (
        UniqueConstraint("company_id", "fiscal_year", "reporting_period", name="uq_company_esg_year_period"),
    )

    company = relationship("Company", back_populates="esg_records")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_hash = Column(String(64), unique=True, index=True, nullable=False)  # SHA256
    file_size_bytes = Column(Integer, nullable=False)
    document_type = Column(String(64), default="Annual Report", nullable=False)
    fiscal_year = Column(Integer, nullable=True, index=True)
    total_pages = Column(Integer, default=0)
    total_chunks = Column(Integer, default=0)
    status = Column(String(32), default="PENDING", index=True)  # PENDING, PROCESSING, INDEXED, FAILED
    source_url = Column(String(512), nullable=True)
    error_message = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    company = relationship("Company", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=True, index=True)
    page_number = Column(Integer, nullable=False, index=True)
    section = Column(String(128), default="General", nullable=False)
    chunk_index = Column(Integer, nullable=False)
    chunk_id = Column(String(128), unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    token_count = Column(Integer, default=0)
    is_table = Column(Boolean, default=False)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    document = relationship("Document", back_populates="chunks")


class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    fiscal_year = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    report_type = Column(String(64), default="Comprehensive Financial & ESG", nullable=False)
    pdf_path = Column(String(512), nullable=True)
    html_path = Column(String(512), nullable=True)
    summary = Column(Text, nullable=True)
    metrics_json = Column(Text, nullable=True)
    citations_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    company = relationship("Company", back_populates="reports")


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True, index=True)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(64), default="GENERAL", nullable=False)
    response_text = Column(Text, nullable=False)
    calculated_metrics_json = Column(Text, nullable=True)
    citations_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)


# ==========================================
# Automated Collection Models
# ==========================================
class DataCollectionJob(Base):
    __tablename__ = "data_collection_jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(32), default="PENDING", index=True)  # PENDING, RUNNING, COMPLETED, FAILED, PARTIAL
    sources_searched = Column(Text, default="[]")               # JSON list of sources queried
    documents_discovered = Column(Integer, default=0)
    documents_downloaded = Column(Integer, default=0)
    financial_records_extracted = Column(Integer, default=0)
    esg_records_extracted = Column(Integer, default=0)
    successful_operations = Column(Integer, default=0)
    failed_operations = Column(Integer, default=0)
    validation_warnings_json = Column(Text, default="[]")       # JSON list of warnings/inconsistencies
    logs = Column(Text, default="")
    started_at = Column(DateTime, default=utcnow)
    completed_at = Column(DateTime, nullable=True)

    company = relationship("Company", back_populates="collection_jobs")


class DiscoveredDocument(Base):
    __tablename__ = "discovered_documents"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    collection_job_id = Column(Integer, ForeignKey("data_collection_jobs.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(64), default="Annual Report", nullable=False)
    fiscal_year = Column(Integer, nullable=True)
    source_url = Column(String(512), nullable=False)
    source_name = Column(String(64), default="SEC EDGAR", nullable=False)  # SEC EDGAR, NSE, BSE, Company IR
    download_status = Column(String(32), default="DISCOVERED")  # DISCOVERED, DOWNLOADED, INDEXED, FAILED, SKIPPED
    local_file_path = Column(String(512), nullable=True)
    file_hash = Column(String(64), nullable=True)
    file_size_bytes = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    discovered_at = Column(DateTime, default=utcnow)

    company = relationship("Company", back_populates="discovered_docs")
