# AI FINANCIAL ANALYST & REPORT GENERATOR

An institutional-grade, end-to-end B.Tech AI & Data Engineering project designed for deterministic financial ratio computation, automated public data acquisition (SEC EDGAR & Indian Stock Exchanges), transparent ESG disclosure scoring, and Hybrid Retrieval-Augmented Generation (Hybrid RAG) with cross-encoder reranking and source citations.

---

## 1. System Architecture

The application executes three parallel analytical pipelines before synthesizing answers through an evidence-grounded AI engine:

```mermaid
flowchart TD
    User([User / Financial Analyst]) --> Dashboard[React + Vite + Tailwind Dashboard]
    Dashboard --> API[FastAPI Backend /api/v1]
    
    API --> Router[Intelligent Query Router]
    
    subgraph PathA [Path A: Deterministic Financial Engine]
        Router --> FinDB[(PostgreSQL / SQLite Financial Data)]
        FinDB --> PandasEngine[Python / Pandas Numerical Engine]
        PandasEngine --> FinMetrics[Ratios: Margins, ROE, ROA, D/E, YoY Growth, OCF]
    end

    subgraph PathB [Path B: Transparent ESG Engine]
        Router --> ESGDB[(Disclosed ESG Indicators)]
        ESGDB --> ESGScorer[Transparent ESG Scorer: E 30%, S 30%, G 40%]
        ESGScorer --> ESGMetrics[Pillar Scores & Coverage %]
    end

    subgraph PathC [Path C: Automated Ingestion & Hybrid RAG]
        Sources[SEC EDGAR / Exchanges / IR / PDF Upload] --> DocParser[PyMuPDF Structure Parser]
        DocParser --> Chunker[Structure-Aware Chunker]
        Chunker --> VectorStore[(Qdrant Vector DB: BAAI/bge-small)]
        Chunker --> BM25[(BM25 Keyword Index)]
        
        Router --> HybridSearch[Parallel Dense + BM25 Search]
        VectorStore -.-> HybridSearch
        BM25 -.-> HybridSearch
        HybridSearch --> RRF[Reciprocal Rank Fusion k=60]
        RRF --> Reranker[Cross-Encoder Reranker]
        Reranker --> TopEvidence[Top Relevant Evidence Passages]
    end

    FinMetrics --> SynthesisEngine[Reasoning Synthesis Engine]
    ESGMetrics --> SynthesisEngine
    TopEvidence --> SynthesisEngine
    
    SynthesisEngine --> LLM[LLM Abstraction: Gemini / OpenAI / Deterministic Fallback]
    LLM --> GroundedResponse[Grounded Analytical Answer]
    TopEvidence --> Citations[Verifiable Source Citations Page X, Section]
    
    GroundedResponse --> Dashboard
    Citations --> Dashboard
    SynthesisEngine --> ReportGen[ReportLab PDF & HTML Dossier Generator]
    ReportGen --> DownloadableReports[Downloadable Audit-Grade Reports]
```

---

## 2. Key Architecture Pillars

### A. Deterministic Financial Analysis Engine (Zero-Hallucination Arithmetic)
- **Principle**: Quantitative financial metrics are **never calculated by an LLM**. All metrics are computed deterministically using standard formulas in Python and Pandas.
- **Formulas Computed**:
  - **Revenue Growth (%)**: `((Current Revenue - Previous Revenue) / Previous Revenue) * 100`
  - **Operating Profit Margin (%)**: `(Operating Income / Revenue) * 100`
  - **Net Profit Margin (%)**: `(Net Income / Revenue) * 100`
  - **Gross Profit Margin (%)**: `(Gross Profit / Revenue) * 100`
  - **Return on Equity (ROE %)**: `(Net Income / Average Shareholders' Equity) * 100`
  - **Return on Assets (ROA %)**: `(Net Income / Total Assets) * 100`
  - **Debt-to-Equity**: `Total Debt / Shareholders' Equity`
  - **Current Ratio**: `Current Assets / Current Liabilities`
  - **Quality of Earnings Ratio**: `Operating Cash Flow / Net Income`
  - **Free Cash Flow**: `Operating Cash Flow - Capital Expenditures`
- **Integrity Rules**:
  - Missing values are explicitly preserved as `None` (never silently converted to zero).
  - Division by zero and negative denominators are trapped with explicit warnings.

### B. Automated Financial & Document Collection Pipeline
- **Company Catalog & Search**: Instant lookup for major corporations (e.g., Apple Inc. `AAPL`, Microsoft `MSFT`, Infosys `INFY`, Tata Consultancy Services `TCS`, Reliance `RELIANCE`).
- **SEC EDGAR Connector**: Official integration with `data.sec.gov/api/xbrl/companyfacts/` and `data.sec.gov/submissions/` using SEC Fair-Access compliant User-Agent headers. Automatically extracts audited GAAP/IFRS facts and discovers official 10-K filings.
- **Exchange & IR Connector**: Captures verified corporate filings, audited results, and Business Responsibility and Sustainability Reports (BRSR) for Indian exchange-listed corporations.
- **Data Validation & Reconciliation**: Validates data types, units, currencies, reporting periods, and balance sheet identity (`Assets ≈ Liabilities + Shareholders' Equity`).

### C. Structure-Aware Hybrid RAG with Cross-Encoder Reranking
- **Document Parsing**: Utilizes `pymupdf` to parse financial statements, tables, and section headings while strictly preserving 1-indexed page numbers.
- **Structure-Aware Chunking**: Chunks narrative paragraphs and financial tables into 300–400 word windows with 50-word overlap, attaching permanent metadata (`company_id`, `fiscal_year`, `document_title`, `section`, `page_number`, `chunk_id`).
- **Qdrant Vector Database**: Stores 384-dimensional dense vectors generated via `BAAI/bge-small-en-v1.5` (quantized ONNX runtime) in a persistent local or client-server collection.
- **BM25 Keyword Retrieval**: Exact lexical matching using `rank_bm25` for financial terms, regulatory phrases, and acronyms.
- **Reciprocal Rank Fusion (RRF)**: Merges dense and lexical results using `RRF_score = 1 / (60 + rank)`.
- **Cross-Encoder Reranker**: Computes passage relevance, query term proximity, and financial section weighting to select top evidence passages.
- **Grounded Citations**: Formats citations with document title, section, and page number: e.g. `[TCS Integrated Annual Report FY2024, Page 2, Section: Management Discussion & Analysis]`.

### D. Transparent Project-Specific ESG Scoring Engine
- **Methodology**: Evaluates disclosures across Environmental (30%), Social (30%), and Governance (40%) pillars.
- **Zero-Penalty Non-Disclosure**: Undisclosed metrics are recorded as `UNDISCLOSED` and omitted from pillar averages rather than penalized as zero.
- **Coverage Gate**: Requires at least 30% core data coverage before issuing an overall composite score.
- **Academic Disclaimer**: Clearly disclaims that the model is an internal educational score and not an official MSCI or Sustainalytics rating.

### E. Audit-Grade Report Generation
- **ReportLab PDF Engine**: Generates multi-page institutional research dossiers with headers, page numbers (`NumberedCanvas`), financial ratio tables, ESG breakdowns, and qualitative citations.
- **Responsive HTML Dossier**: Generates standalone HTML reports with Tailwind CSS formatting.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, Recharts, Lucide Icons |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Uvicorn |
| **Numerical Engine** | Pandas, NumPy, OpenPyXL |
| **Vector DB** | Qdrant (`qdrant-client` local persistent embedded storage or server mode) |
| **Embeddings & Search** | `fastembed` (`BAAI/bge-small-en-v1.5` ONNX), `rank_bm25` (BM25Okapi) |
| **Document Processing** | PyMuPDF (`fitz`), Structure-Aware Chunker, SHA-256 deduplication |
| **Report Generation** | ReportLab (PDF), HTML5 / CSS |
| **Database** | SQLite (with WAL mode & foreign keys enabled) or PostgreSQL |
| **LLM Inference** | Configurable: Google Gemini, OpenAI, Groq, Ollama, or Deterministic Engine |

---

## 4. Project Directory Structure

```
llm_project/
├── backend/
│   ├── app/
│   │   ├── config.py                   # Pydantic environment settings
│   │   ├── database.py                 # SQLAlchemy engine & session factory
│   │   ├── main.py                     # FastAPI application & lifespan events
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schema_models.py        # Company, FinancialData, ESGData, Document, Report models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── pydantic_schemas.py     # Request/response validation schemas
│   │   ├── collectors/
│   │   │   ├── company_catalog.py      # Benchmark company directory (TCS, AAPL, INFY, MSFT)
│   │   │   ├── sec_edgar_connector.py  # SEC EDGAR XBRL & submissions connector
│   │   │   ├── exchange_connector.py   # Indian stock exchange & IR filings connector
│   │   │   ├── data_validator.py       # Balance sheet & unit reconciliation
│   │   │   └── collection_orchestrator.py # Automated background collection pipeline
│   │   ├── engine/
│   │   │   ├── financial_calculator.py # Deterministic ratio & trend engine
│   │   │   └── esg_scorer.py           # Transparent 30/30/40 ESG scoring engine
│   │   ├── rag/
│   │   │   ├── document_parser.py      # PyMuPDF page & table extraction
│   │   │   ├── chunker.py              # Structure-aware chunking with metadata
│   │   │   ├── vector_store.py         # Qdrant client & BGE-small embeddings
│   │   │   ├── bm25_search.py          # BM25 lexical search engine
│   │   │   ├── hybrid_retriever.py     # RRF fusion of dense + lexical search
│   │   │   ├── reranker.py             # Cross-encoder relevance reranker
│   │   │   ├── llm_service.py          # Multi-provider LLM & deterministic reasoning
│   │   │   └── sample_document_generator.py # Authentic report PDF generator
│   │   ├── report_generator/
│   │   │   ├── pdf_generator.py        # ReportLab institutional PDF dossier generator
│   │   │   └── html_generator.py       # Standalone HTML report generator
│   │   └── routes/
│   │       ├── companies.py            # Company CRUD & catalog discovery
│   │       ├── financials.py           # Financial data & ratio analysis endpoints
│   │       ├── documents.py            # PDF upload, chunking, and download
│   │       ├── esg.py                  # ESG data & score breakdown endpoints
│   │       ├── collectors.py           # Automated data collection pipeline triggers
│   │       ├── chat.py                 # RAG AI Analyst conversational query endpoint
│   │       ├── reports.py              # PDF/HTML report generation and download
│   │       └── settings.py             # System health & LLM diagnostics
│   ├── tests/
│   │   ├── test_financial_engine.py    # Unit tests for ratio formulas & edge cases
│   │   ├── test_esg_scoring.py         # Tests for ESG weighting & coverage gate
│   │   ├── test_hybrid_rag.py          # Tests for BM25, RRF, and reranking
│   │   ├── test_api_endpoints.py       # Integration tests for FastAPI endpoints
│   │   └── test_end_to_end.py          # Full 10-step lifecycle integration test
│   ├── seed_data.py                    # Database population script with real company data
│   └── requirements.txt                # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── api/client.ts               # Axios client for all backend endpoints
│   │   ├── components/
│   │   │   ├── Navbar.tsx              # Top navigation & active company switcher
│   │   │   └── Sidebar.tsx             # Module navigation sidebar
│   │   ├── pages/
│   │   │   ├── OverviewDashboard.tsx   # Financial overview, charts, and key ratios
│   │   │   ├── DataCollectionDashboard.tsx # Automated data collection & source discovery
│   │   │   ├── CompanyManagement.tsx   # Company CRUD and catalog search
│   │   │   ├── FinancialAnalysis.tsx   # Structured tables, CSV upload, and ratios
│   │   │   ├── DocumentManagement.tsx  # Document upload, chunk viewer, and PDF download
│   │   │   ├── AIAssistantChat.tsx     # Hybrid RAG conversational interface with citations
│   │   │   ├── ESGAnalysis.tsx         # Transparent ESG indicator decomposition
│   │   │   ├── CompanyComparison.tsx   # Peer benchmarking and comparative charts
│   │   │   ├── ReportsManagement.tsx   # PDF & HTML report generation and library
│   │   │   └── SystemSettings.tsx      # System health, Qdrant status, and LLM setup
│   │   ├── types.ts                    # TypeScript interface definitions
│   │   ├── App.tsx                     # Main layout & router container
│   │   └── main.tsx                    # React DOM entry point
│   ├── package.json
│   ├── vite.config.ts                  # Vite config with backend proxy
│   └── tailwind.config.js
├── data/
│   ├── uploads/                        # Uploaded and generated PDF reports
│   ├── reports/                        # Exported PDF and HTML research reports
│   └── qdrant_storage/                 # Persistent Qdrant vector database
├── docker-compose.yml                  # Multi-container Docker deployment
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example                        # Template environment variables file
├── pytest.ini                          # Test configuration
└── run.py                              # Backend startup entry point
```

---

## 5. Getting Started & Running Locally

### Prerequisites
- Python 3.11+
- Node.js v18+ and npm
- (Optional) Docker and Docker Compose

### Step 1: Clone & Set Up Backend
```bash
# Navigate to project directory
cd /home/vivek/Projects/llm_project

# Activate Python virtual environment
source .venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt
```

### Step 2: Seed Initial Benchmark Data
Populate audited financial data, ESG disclosures, and indexed PDF reports for TCS and Apple Inc.:
```bash
python backend/seed_data.py
```

### Step 3: Start the Backend Server
```bash
python run.py
```
The FastAPI backend starts on `http://127.0.0.1:8000`.
- Swagger API Documentation: `http://127.0.0.1:8000/docs`
- Unified Full-Stack Application: `http://127.0.0.1:8000/`

### Step 4: (Optional) Run Frontend in Vite Development Mode
If you wish to make live frontend modifications with Hot Module Replacement (HMR):
```bash
cd frontend
npm run dev
```
The Vite development server runs on `http://localhost:5173` and automatically proxies `/api` calls to the FastAPI backend.

---

## 6. Running with Docker Compose

To deploy the entire production stack (PostgreSQL, Qdrant, FastAPI backend, and Nginx frontend):
```bash
docker-compose up --build
```
- Frontend UI: `http://localhost:5173`
- Backend API: `http://localhost:8000/docs`

---

## 7. Running the Automated Test Suite

All tests can be executed via `pytest`:
```bash
source .venv/bin/activate
pytest backend/tests/ -v
```

### Test Coverage Highlights:
- `test_financial_engine.py`: Validates growth formulas, gross/operating/net margins, ROE, ROA, Debt-to-Equity, zero-denominator safety, and missing-value handling.
- `test_esg_scoring.py`: Tests transparent pillar weighting (30/30/40), indicator normalization, non-disclosure omission, and the < 30% coverage withholding gate.
- `test_hybrid_rag.py`: Verifies BM25 lexical tokenization, Reciprocal Rank Fusion (RRF), and cross-encoder reranking.
- `test_api_endpoints.py`: Tests company listing, catalog search, financial analysis, ESG scoring, chat query, and report downloads.
- `test_end_to_end.py`: Comprehensive 10-step full-lifecycle integration test validating company creation, financial upload, PDF report generation, vector indexing, grounded chat with citations, and PDF output.

---

## 8. Demonstration Workflow for B.Tech Project Viva

1. **Company Discovery & Selection**:
   - Navigate to the **Data Collection** or **Companies** tab.
   - Search for **Tata Consultancy Services (TCS)** or **Apple Inc. (AAPL)**.
   - Observe how SEC CIK (`0000320193`) and NSE Symbol (`TCS`) are registered.

2. **Automated Data Acquisition**:
   - In the **Data Collection** tab, click **"Collect Data"**.
   - Observe live terminal logs showing official SEC EDGAR XBRL facts or Exchange filings being fetched, validated, and reconciled.

3. **Deterministic Financial Analysis**:
   - Switch to **Financial Analysis**.
   - Review historical profitability tables and computed ratios: Operating Margin, Net Margin, ROE, and Debt-to-Equity.
   - Note the data validation notes and accounting reconciliation checks.

4. **Transparent ESG Scoring**:
   - Navigate to **ESG Evaluation**.
   - Inspect the 30% Environmental, 30% Social, and 40% Governance pillar breakdowns.
   - Observe the formula display, data coverage bar, and disclosure indicators.

5. **AI Financial Analyst Chat (Hybrid RAG)**:
   - Go to **AI Analyst Chat**.
   - Click a sample prompt: *"Why did operating margin change in FY2024?"* or *"What are the principal risk factors?"*
   - Review the response: Notice how exact calculated numbers are cited, and click the **[Citation]** badge to inspect the original document title, page number, and section!

6. **Institutional Report Export**:
   - Open **Generated Reports**.
   - Click **"Generate PDF & HTML Report"**.
   - Click **"PDF"** to download the institutional dossier generated via ReportLab with tables, citations, and page numbering.
   - Click **"HTML"** to view the interactive web dossier in a new tab.

---

## 9. Academic Integrity & Project Disclaimers
1. **Financial Arithmetic**: Performed strictly by numerical Python code to guarantee 100% precision with zero LLM calculation errors.
2. **ESG Rating**: Academic project-specific educational model; not an official commercial credit rating.
3. **Evidence Citations**: Claims inferred from qualitative documents are strictly backed by extracted page references from corporate filings.
