export interface Company {
  id: number;
  ticker: string;
  name: string;
  sector?: string;
  industry?: string;
  description?: string;
  currency: string;
  units: string;
  exchange?: string;
  cik?: string;
  isin?: string;
  nse_symbol?: string;
  bse_code?: string;
  ir_url?: string;
  created_at: string;
  updated_at: string;
}

export interface CompanyCatalogItem {
  ticker: string;
  name: string;
  exchange: string;
  sector?: string;
  cik?: string;
  isin?: string;
  nse_symbol?: string;
  bse_code?: string;
  ir_url?: string;
  currency: string;
  units: string;
}

export interface FinancialRecord {
  id: number;
  company_id: number;
  fiscal_year: number;
  period: string;
  reporting_basis?: string;
  reporting_period_end?: string;
  currency: string;
  units: string;
  source: string;
  source_url?: string;
  filing_date?: string;
  revenue?: number | null;
  cost_of_revenue?: number | null;
  gross_profit?: number | null;
  operating_profit?: number | null;
  net_profit?: number | null;
  eps?: number | null;
  total_assets?: number | null;
  current_assets?: number | null;
  total_liabilities?: number | null;
  current_liabilities?: number | null;
  shareholders_equity?: number | null;
  debt?: number | null;
  cash?: number | null;
  operating_cash_flow?: number | null;
  capital_expenditures?: number | null;
  free_cash_flow?: number | null;
  is_audited?: boolean;
  validation_status?: string;
  validation_notes?: string;
}

export interface FinancialRatioSet {
  fiscal_year: number;
  period: string;
  revenue?: number | null;
  gross_profit?: number | null;
  operating_profit?: number | null;
  net_profit?: number | null;
  revenue_growth_pct?: number | null;
  net_profit_growth_pct?: number | null;
  operating_profit_margin_pct?: number | null;
  net_profit_margin_pct?: number | null;
  gross_profit_margin_pct?: number | null;
  return_on_assets_pct?: number | null;
  return_on_equity_pct?: number | null;
  debt_to_equity?: number | null;
  current_ratio?: number | null;
  operating_cash_flow?: number | null;
  free_cash_flow?: number | null;
  ocf_to_net_income?: number | null;
  eps?: number | null;
  warnings?: string[];
  missing_fields?: string[];
  units: string;
  currency: string;
}

export interface FinancialAnalysis {
  company_id: number;
  company_name: string;
  ticker: string;
  currency: string;
  units: string;
  years_available: number[];
  ratios: FinancialRatioSet[];
  summary_insights: string[];
  missing_data_warnings: string[];
}

export interface ESGRecord {
  id: number;
  company_id: number;
  fiscal_year: number;
  reporting_period: string;
  source_document?: string;
  carbon_emissions_scope1?: number | null;
  carbon_emissions_scope2?: number | null;
  carbon_emissions_scope3?: number | null;
  energy_consumption_gj?: number | null;
  renewable_energy_pct?: number | null;
  water_consumption_kl?: number | null;
  water_recycled_pct?: number | null;
  waste_generated_mt?: number | null;
  waste_recycled_pct?: number | null;
  female_workforce_pct?: number | null;
  employee_turnover_pct?: number | null;
  lost_time_injury_rate?: number | null;
  training_hours_per_employee?: number | null;
  csr_spending_amount?: number | null;
  human_rights_policy?: boolean | null;
  board_size?: number | null;
  independent_directors_pct?: number | null;
  women_on_board_pct?: number | null;
  ceo_chair_separation?: boolean | null;
  ethics_code_established?: boolean | null;
  whistleblower_mechanism?: boolean | null;
  anti_corruption_policy?: boolean | null;
  data_privacy_policy?: boolean | null;
  environmental_score?: number | null;
  social_score?: number | null;
  governance_score?: number | null;
  overall_esg_score?: number | null;
  data_coverage_pct?: number | null;
}

export interface ESGScoreBreakdown {
  environmental_score?: number | null;
  social_score?: number | null;
  governance_score?: number | null;
  overall_esg_score?: number | null;
  data_coverage_pct: number;
  weights: {
    environmental: number;
    social: number;
    governance: number;
  };
  indicator_scores: {
    environmental: Record<string, any>;
    social: Record<string, any>;
    governance: Record<string, any>;
  };
  formula_explanation: string;
  methodology_limitations: string[];
  is_sufficient_data: boolean;
}

export interface DocumentItem {
  id: number;
  company_id: number;
  title: string;
  file_name: string;
  file_size_bytes: number;
  document_type: string;
  fiscal_year?: number | null;
  total_pages: number;
  total_chunks: number;
  status: string;
  error_message?: string | null;
  created_at: string;
}

export interface CitationItem {
  document_title: string;
  document_type: string;
  fiscal_year?: number | null;
  page_number: number;
  section: string;
  chunk_id: string;
  relevance_score?: number | null;
  snippet: string;
}

export interface QueryResponse {
  query: string;
  query_type: string;
  answer: string;
  citations: CitationItem[];
  deterministic_metrics?: any;
  esg_summary?: any;
  llm_provider: string;
  grounded: boolean;
  warnings?: string[];
}

export interface GeneratedReport {
  id: number;
  company_id: number;
  company_name: string;
  fiscal_year: number;
  title: string;
  report_type: string;
  pdf_url?: string;
  html_url?: string;
  summary?: string;
  created_at: string;
}

export interface CollectionJob {
  id: number;
  company_id: number;
  status: string;
  sources_searched: string;
  documents_discovered: number;
  documents_downloaded: number;
  financial_records_extracted: number;
  esg_records_extracted: number;
  successful_operations: number;
  failed_operations: number;
  validation_warnings_json: string;
  logs?: string;
  started_at: string;
  completed_at?: string;
}

export interface DiscoveredDocument {
  id: number;
  company_id: number;
  collection_job_id?: number;
  title: string;
  document_type: string;
  fiscal_year?: number;
  source_url: string;
  source_name: string;
  download_status: string;
  file_size_bytes: number;
  error_message?: string;
  discovered_at: string;
}

export interface SystemSettings {
  project_name: string;
  version: string;
  database_url: string;
  qdrant_mode: string;
  qdrant_path: string;
  qdrant_collection: string;
  embedding_model: string;
  reranker_enabled: boolean;
  llm_provider: string;
  gemini_configured: boolean;
  openai_configured: boolean;
  groq_configured: boolean;
  ollama_url: string;
}
