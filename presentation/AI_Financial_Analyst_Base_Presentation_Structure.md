# AI FINANCIAL ANALYST & REPORT GENERATOR
## Master Base Presentation Specification (14 Slides)
### Designed for Academic Project Viva & Claude Presentation Generation

> **Project Title:** AI Financial Analyst & Report Generator: Dual-Pathway Deterministic Financial Analysis, Hybrid RAG with Verifiable Source Citations, and Transparent ESG Disclosure Scoring  
> **Institution:** Department of Artificial Intelligence & Data Engineering, Malaviya National Institute of Technology (MNIT) Jaipur  
> **Team Members:**  
> • **Vivek Upadhyay** — *Team Captain* — Roll No. `2023UAI1996`  
> • **Ashish Rolaniya** — *Co-Investigator* — Roll No. `2023UAI1825`  
> **Project Repository:** [https://github.com/vivekmnit1996/AI-Financial-Analyst](https://github.com/vivekmnit1996/AI-Financial-Analyst)  
> **System Status:** Operational Prototype demonstrated on SEC EDGAR & Indian Stock Exchange filings (**TRL 5 / 6**)  

---

## Instructions for Uploading to Claude / LLMs

```markdown
PROMPT TO CLAUDE:
"Act as a professional presentation designer and academic technical writer.
Below is the complete 14-slide master base specification for our B.Tech Capstone Project
titled 'AI Financial Analyst & Report Generator'. 
Please generate a fully stylized, visually stunning slide deck based on the exact structure,
data tables, diagrams, and speaker notes provided below. Preserve all technical details,
empirical benchmark numbers (MRR 0.916, 21 tests, sub-second latency), and student contributions."
```

---

## Slide-by-Slide Content & Specification

---

### Slide 1: Title Slide & Team Credentials
* **Slide Category:** Project Capstone Presentation
* **Slide Title:** AI Financial Analyst & Report Generator
* **Subtitle:** Dual-Pathway Deterministic Arithmetic, Hybrid RAG with Verifiable Citations, & Transparent ESG Scoring
* **Layout Design:** 
  * Dark Navy Blue institutional background (`#0F172A`).
  * Left-accent electric cyan vertical bar (`#0EA5E9`).
  * Two prominent frosted-glass metadata cards for Project Investigators and System Specifications.
* **Content:**
  * **Card 1 — Project Investigators:**
    * **Vivek Upadhyay (Team Captain)** — Roll No: `2023UAI1996`
    * **Ashish Rolaniya (Co-Investigator)** — Roll No: `2023UAI1825`
    * Department of Artificial Intelligence & Data Engineering
    * Malaviya National Institute of Technology (MNIT) Jaipur
  * **Card 2 — Technical Specifications & Artifacts:**
    * **Architecture:** Dual-Pathway Deterministic Numerical Core + Hybrid RAG
    * **Stack:** Python 3.11+, FastAPI, React 18, Vite, Qdrant Vector DB, PyMuPDF, ReportLab
    * **Validation:** 21 Automated Pytest Integration & Unit Suites (100% Pass)
    * **Open-Source Codebase:** `https://github.com/vivekmnit1996/AI-Financial-Analyst`
* **Speaker / Presenter Notes:**
  > "Good morning esteemed project mentor and evaluation committee members. Today, my teammate Ashish Rolaniya and I, Vivek Upadhyay, present our B.Tech Capstone project: 'AI Financial Analyst and Report Generator'. Our goal was to build a production-grade, institutional equity research platform that bridges the fundamental flaw of generative AI in corporate finance—hallucinated arithmetic—by enforcing a strict dual-pathway architecture, Hybrid RAG with exact page provenance, and transparent ESG scoring."

---

### Slide 2: Problem Statement & Motivation
* **Slide Category:** 1. Problem Statement & Motivation
* **Slide Title:** Problem Statement: The Arithmetic & Provenance Bottleneck
* **Layout Design:** 3-column comparative problem breakdown cards.
* **Content:**
  * **Column 1 — Disclosures Overload (Volume & Time Drain):**
    * Corporate disclosures (SEC 10-K, 10-Q, Indian Annual Reports, SEBI BRSR) regularly exceed **300 to 500+ pages** per corporation per fiscal year.
    * Financial analysts dedicate up to **70% of analytical hours** to manual data gathering, cross-referencing footnotes, and balance sheet reconciliation.
    * Retail and institutional investors suffer from information asymmetry due to the friction of synthesizing multi-year disclosures.
  * **Column 2 — The Generative AI Trap (Hallucinated Arithmetic):**
    * Commercial autoregressive LLMs (GPT-4, Gemini) fail fundamentally on accounting algebra and invent financial ratios out of token probabilities.
    * Empirical benchmarks (*FinanceBench 2023*, *FinQA 2021*) prove commercial LLMs suffer **18% to 35% error rates** on multi-step financial math.
    * Standalone LLMs generate plausible-sounding qualitative narratives without auditable page-level citations, making them legally inadmissible for regulatory compliance.
  * **Column 3 — Opaque ESG Scoring ("Aggregate Confusion"):**
    * Commercial ESG ratings (MSCI, Sustainalytics, S&P) exhibit alarmingly low correlation (**$r \approx 0.54$**, MIT Sloan *Aggregate Confusion* study).
    * Proprietary black-box algorithms penalize unrecorded disclosures as zero without explaining their measurement or imputation logic.
    * SEBI BRSR and EU CSRD regulations demand verifiable, indicator-level audit trails rather than speculative scores.
* **Speaker / Presenter Notes:**
  > "Slide 2 outlines the real-world motivation. Modern corporate filings are enormous. Financial analysts spend most of their time cross-referencing tables and footnotes. When practitioners attempt to use generic LLMs like ChatGPT or Claude for financial analysis, they encounter two fatal pitfalls: first, autoregressive language models cannot reliably calculate mathematical formulas, frequently hallucinating operating margins or cash flows; second, they produce black-box assertions without auditable citations. Furthermore, existing commercial ESG ratings diverge sharply with a correlation of barely 0.54. Our project was designed specifically to eliminate all three bottlenecks."

---

### Slide 3: Technology Readiness Level (TRL) & Operational Scope
* **Slide Category:** 1. Problem Statement — TRL Level & Deployment
* **Slide Title:** Technology Readiness Level (TRL 5/6) & System Scope
* **Layout Design:** Split-panel layout: Left panel showing the NASA/DoD TRL progression ladder; Right panel showing the target deployment environment and operational parameters.
* **Content:**
  * **TRL Status: TRL 5 / 6 (Operational Prototype Validated in Relevant Environment)**
    * **TRL 3 (Analytical Proof of Concept):** Formulated the mathematical decoupling of deterministic arithmetic from generative natural language reasoning.
    * **TRL 4 (Component Validation in Lab):** Validated Python/Pandas numerical engine, PyMuPDF spatial parser, Qdrant vector store with BGE-small embeddings, and BM25 index on historical filings.
    * **TRL 5 (System Integrated in Relevant Environment):** Integrated automated connectors to live SEC EDGAR XBRL APIs (10,400+ companies) and Indian Stock Exchanges (NSE/BSE) with balance sheet reconciliation.
    * **TRL 6 (Operational Prototype Demonstrated):** Full-stack web system running live with React 18, FastAPI backend, live Hybrid RAG chat with page-anchored citations, and ReportLab PDF generator. Validated via 21 automated integration tests.
  * **Target Operational Scope & Deployment Environment:**
    * **Target Users:** Buy-side/sell-side equity research analysts, corporate treasury teams, regulatory compliance officers, and academic finance labs.
    * **Infrastructure Footprint:** Runs locally or in private clouds via Docker Compose on standard commodity x86_64 CPUs (< 650 MB RAM footprint; no high-cost GPUs needed).
    * **Regulatory Compliance:** Adheres to SEC Fair Access guidelines with registered User-Agent headers.
* **Speaker / Presenter Notes:**
  > "On Slide 3, we evaluate our system against standard NASA and DoD Technology Readiness Level criteria. Many academic AI projects remain at TRL 3 or 4—a Jupyter notebook showing toy results. Our project has reached TRL 5 and TRL 6: an operational full-stack prototype validated on real, live corporate filings from the US SEC and Indian NSE/BSE. It runs in Docker, adheres to SEC Fair Access guidelines, and executes in real-time on commodity CPUs."

---

### Slide 4: Literature Survey & State of the Art (SOTA)
* **Slide Category:** 3. Literature Survey & SOTA Foundations
* **Slide Title:** Literature Survey: State of the Art (SOTA) Benchmarks
* **Layout Design:** Structured 4-column academic literature matrix summarizing foundational research.
* **Content:**

| Domain / Benchmark | Key SOTA Publication | Core Contribution & Findings | Project Integration |
| :--- | :--- | :--- | :--- |
| **Financial QA & Reasoning** | **FinQA** (*Chen et al., EMNLP 2021*) & **FinanceBench** (*Islam et al., 2023*) | First open-domain benchmarks testing LLM numerical reasoning over financial tables & 10-K filings. | Proved that commercial LLMs guess math; directly motivated our 100% deterministic Python engine. |
| **Retrieval-Augmented Generation** | **RAG** (*Lewis et al., NeurIPS 2020*) & **DPR** (*Karpukhin et al., EMNLP 2020*) | Established parametric + non-parametric memory for verifiable question answering. | Standard DPR fails on financial jargon; solved by fusing sparse BM25 + dense BGE vectors. |
| **Rank Fusion & Neural Reranking** | **Reciprocal Rank Fusion** (*Cormack et al., SIGIR 2009*) & **Cross-Encoder** (*Nogueira & Cho, 2019*) | RRF merges multi-retriever rank lists ($k=60$); Cross-encoders compute full query-document cross-attention. | Implemented RRF + Cross-Encoder to achieve a **+25.1% MRR boost** over single-modality dense search. |
| **ESG Scoring Methodologies** | **Aggregate Confusion: The Divergence of ESG Ratings** (*Berg et al., Review of Finance 2022*) | Demonstrated that leading ESG rating agencies correlate at only $r \approx 0.54$ due to scope and measurement divergence. | Overcame black-box divergence by designing a transparent 30/30/40 indicator model with coverage gate. |

* **Speaker / Presenter Notes:**
  > "Slide 4 presents our literature survey of State-of-the-Art foundations. We surveyed 19 peer-reviewed papers across 4 pillars. First, FinQA and FinanceBench proved that pure LLMs are dangerous for finance because they guess mathematical numbers. Second, Lewis et al.'s original RAG paper introduced retrieval-augmented generation. Third, Cormack et al. and Nogueira & Cho established Reciprocal Rank Fusion and Cross-Encoder reranking. Finally, the seminal MIT Sloan paper by Berg et al. demonstrated that commercial ESG ratings diverge sharply due to opaque proprietary models."

---

### Slide 5: Research Gaps Identified & Base Papers
* **Slide Category:** 3. Gaps Identified & Base Papers
* **Slide Title:** Research Gaps Identified & Base Paper Traceability
* **Layout Design:** 4 horizontal problem-solution cards with explicit literature tags.
* **Content:**
  * **GAP 1: Arithmetic Inaccuracy in Generative LLMs**
    * *Base Papers:* FinanceBench (*Islam et al., 2023*), FinQA (*Chen et al., EMNLP 2021*)
    * *Identified Gap:* Autoregressive language models attempt arithmetic inside token embeddings, resulting in rounding errors, hallucinated ratios, and sign errors in balance sheets.
    * *Our Solution:* Decouple math completely. Formulated **Pathway A**: a 100% deterministic Python/Pandas numerical engine with division-by-zero traps.
  * **GAP 2: Financial Vocabulary Mismatch in Pure Dense Search**
    * *Base Papers:* BGE Embeddings (*Xiao et al., 2023*), Okapi BM25 (*Robertson & Zaragoza, 2009*)
    * *Identified Gap:* Bi-encoder dense vectors struggle with exact regulatory terminology, accounting standard codes (e.g., 'Ind AS 116'), ticker symbols, and specific numerical keys.
    * *Our Solution:* Implemented **Hybrid Retrieval** (Dense Qdrant + Sparse BM25 fused via RRF $k=60$) followed by Cross-Encoder neural reranking.
  * **GAP 3: Missing Provenance & Black-Box Qualitative Assertions**
    * *Base Papers:* RAG (*Lewis et al., NeurIPS 2020*), Dense Passage Retrieval (*Karpukhin et al., 2020*)
    * *Identified Gap:* Existing financial AI tools generate claims without auditable page provenance, rendering them inadmissible for institutional regulatory compliance.
    * *Our Solution:* Spatial coordinate PDF parsing with PyMuPDF; every claim is strictly bound to `[Document Title, Page X, Section Y]` citation badges.
  * **GAP 4: Opaque & Speculative ESG Scoring Methodologies**
    * *Base Papers:* Aggregate Confusion (*Berg et al., Review of Finance 2022*)
    * *Identified Gap:* Commercial ESG providers fabricate proxy numbers for missing disclosures or assign arbitrary zero scores, obscuring real corporate sustainability.
    * *Our Solution:* Transparent 30/30/40 linear model with non-disclosure zero-penalty omission and a mandatory 30% reporting coverage gate.
* **Speaker / Presenter Notes:**
  > "Slide 5 establishes the precise research gaps we identified in prior literature and maps them directly to our base papers and novel solutions. Gap 1 is arithmetic inaccuracy, identified by FinanceBench—solved by our deterministic numerical engine. Gap 2 is vocabulary mismatch in pure dense embeddings—solved by our Hybrid RRF plus Cross-Encoder reranking. Gap 3 is black-box assertions lacking provenance—solved by our structure-aware page coordinate parser. Gap 4 is opaque ESG ratings—solved by our transparent 30/30/40 indicator scoring with a coverage withholding gate."

---

### Slide 6: Proposed Methodology: Dual-Pathway Architecture
* **Slide Category:** 4. Proposed Methodology — Architecture
* **Slide Title:** Proposed Methodology: Dual-Pathway System Architecture
* **Layout Design:** Flowchart diagram + 3 parallel execution pillars + unified synthesis engine.
* **Architecture Diagram:**
```mermaid
flowchart TD
    User([User / Equity Analyst]) --> Dashboard[React 18 + Vite UI]
    Dashboard --> FastAPI[FastAPI Backend /api/v1]
    FastAPI --> Router[Query Intent Router]
    
    subgraph PathA [Pathway A: Deterministic Financial Core]
        Router --> FinDB[(Relational DB / Cache)]
        FinDB --> PandasEngine[Python / Pandas Engine]
        PandasEngine --> FinMetrics[14 Ratios: Margins, ROE, ROA, D/E, FCF]
    end
    
    subgraph PathB [Pathway B: Hybrid RAG Intelligence]
        Router --> DocIngest[PyMuPDF Page Parser]
        DocIngest --> Chunker[Structure-Aware Chunker]
        Chunker --> Qdrant[(Qdrant Dense BGE-small)]
        Chunker --> BM25[(BM25 Lexical Index)]
        Qdrant & BM25 --> RRF[RRF Fusion k=60]
        RRF --> Reranker[Cross-Encoder Reranker]
        Reranker --> TopEvidence[Top-5 Evidence Passages]
    end
    
    subgraph PathC [Pathway C: Transparent ESG Scorer]
        Router --> ESGDB[(BRSR Indicator Store)]
        ESGDB --> ESGMath[E: 30% | S: 30% | G: 40%]
        ESGMath --> ESGScore[Indicator Score & Coverage Gate]
    end
    
    FinMetrics & TopEvidence & ESGScore --> Synthesis[Context-Constrained Synthesis Engine]
    Synthesis --> Output[Executive Answer + Page Citations + ReportLab PDF]
    Output --> Dashboard
```
* **Core Architectural Components:**
  * **Pathway A (Deterministic Financial Core):** Strict arithmetic computation of 14 ratios (Gross, Operating, Net Margin, ROE, ROA, Debt-to-Equity, Current Ratio, Free Cash Flow).
  * **Pathway B (Hybrid RAG Document Intelligence):** Dual dense/lexical retrieval fused with Reciprocal Rank Fusion ($k=60$) and reranked using cross-encoders.
  * **Pathway C (Transparent ESG Scoring):** Linear scoring over 16 core indicators with a 30% minimum disclosure withholding gate.
* **Speaker / Presenter Notes:**
  > "Slide 6 is the heart of our technical methodology: the Dual-Pathway Architecture. Rather than passing raw financial tables to an LLM and hoping it does arithmetic correctly, our architecture splits execution into three parallel, deterministic pipelines. Pathway A computes all 14 financial ratios in Python/Pandas. Pathway B performs Hybrid RAG document retrieval using dense vectors and sparse BM25, merged via RRF and reranked via a cross-encoder. Pathway C calculates transparent ESG scores. All three feed into our synthesis engine, guaranteeing 100% calculation accuracy with full source provenance."

---

### Slide 7: Proposed Methodology: Datasets & Regulatory Ingestion
* **Slide Category:** 4. Proposed Methodology — Data Pipeline
* **Slide Title:** Proposed Methodology: Datasets & Regulatory Ingestion
* **Layout Design:** Two-column card format: Left column detailing regulatory data sources; Right column detailing preprocessing and reconciliation gates.
* **Content:**
  * **Regulatory Data Sources & Ingestion Connectors:**
    * **SEC EDGAR Official REST APIs:** Ingests audited Company Facts JSON submissions across both **US-GAAP** (Form 10-K, 10-Q) and **IFRS-FULL** (Form 20-F for foreign private issuers) with 10-digit zero-padded CIK lookup across 10,400+ corporations.
    * **Indian Stock Exchange Feeds (NSE / BSE):** Ingests verified multi-year audited annual financial statements and Business Responsibility & Sustainability Reports (BRSR).
    * **Dynamic Global Discovery via Yahoo Finance:** Integrated real-time query interface (`query2.finance.yahoo.com/v1/finance/search`) for automated corporate discovery.
  * **Data Preprocessing & Integrity Invariants:**
    * **Balance Sheet Invariant Reconciliation:** Automated validation prior to database insertion:
      $$|\text{Total Assets} - (\text{Total Liabilities} + \text{Shareholders' Equity})| < 0.02 \times \text{Total Assets}$$
    * **Unit & Currency Standardization:** Standardizes reporting bases (Crores, Millions, USD, INR) without speculative exchange-rate distortion.
    * **Spatial PDF Extraction (PyMuPDF):** Extracts character blocks and table grids while preserving permanent 1-indexed page coordinates.
    * **Structure-Aware Chunking:** 300–400 word sliding windows with 50-word overlap, tagging metadata (`company_id`, `fiscal_year`, `document_title`, `section`, `page_number`).
* **Speaker / Presenter Notes:**
  > "Slide 7 details our dataset acquisition and preprocessing pipeline. Our system does not rely on synthetic toy data. It connects to official SEC EDGAR XBRL APIs using fair-access headers, ingesting 10-K and 20-F filings for over 10,400 companies. For Indian companies, it ingests audited filings and SEBI BRSR reports from the NSE and BSE. Before anything is written to the database, an automated accounting reconciliation gate checks the balance sheet identity equation. For unstructured PDFs, PyMuPDF extracts text while strictly preserving 1-indexed page coordinates."

---

### Slide 8: Proposed Methodology: LLM Techniques & Hybrid RAG Pipeline
* **Slide Category:** 4. Proposed Methodology — LLM & Retrieval
* **Slide Title:** Proposed Methodology: LLM Techniques & Hybrid RAG Pipeline
* **Layout Design:** 4-quadrant process cards explaining the retrieval and reasoning pipeline.
* **Content:**
  * **Quadrant 1 — Parallel Dense & Sparse Retrieval:**
    * *Dense Vector Index:* 384-dimensional dense vectors generated via `BAAI/bge-small-en-v1.5` in persistent Qdrant collection with Cosine similarity. Captures semantic concepts and paraphrases.
    * *Sparse Keyword Index:* Okapi BM25 ($k_1=1.5, b=0.75$) matching exact regulatory terms (`Ind AS 116`, `Scope 1 GHG`, `EBITDA`).
  * **Quadrant 2 — Reciprocal Rank Fusion (RRF $k=60$):**
    * Merges dense and sparse ranked lists without score calibration distortion:
      $$\text{RRF}(d) = \sum_{m \in \{\text{Dense}, \text{BM25}\}} \frac{1}{60 + \text{rank}_m(d)}$$
    * Surfaces documents ranked highly across either or both modalities.
  * **Quadrant 3 — Cross-Encoder Neural Reranking:**
    * Bi-encoders lack query-chunk cross-attention. Our Cross-Encoder (`bge-reranker`) scores query-passage pairs jointly via full cross-attention layers.
    * Incorporates a **+0.05 analytical section boost** when the retrieved chunk matches the query intent (e.g. Risk Factors query matching Risk section).
  * **Quadrant 4 — Context-Constrained Executive Synthesis:**
    * *Fiscal Year Targeting:* Parses prompt to extract target fiscal year (e.g., FY2024 vs FY2025) and computes YoY basis-point deltas.
    * *Zero-Hallucination Prompting:* Restricts LLM to provided context + pre-computed Python ratios. Cites `[Document Title, Page X, Section Y]`.
* **Speaker / Presenter Notes:**
  > "Slide 8 details the AI and LLM techniques powering our Hybrid RAG pipeline. Dense vector embeddings are great for semantic paraphrasing, but terrible at exact regulatory codes like 'Ind AS 116'. Conversely, BM25 excels at exact keywords but misses semantic synonyms. We run both in parallel, fuse them with Reciprocal Rank Fusion with smoothing parameter k=60, and then pass the top 20 candidates through a Cross-Encoder that computes full cross-attention. Finally, our synthesis engine enforces a strict zero-hallucination constraint, producing an executive answer with verifiable page citations."

---

### Slide 9: Working Video & Live System Demo
* **Slide Category:** 2. Working Video / Live Demo
* **Slide Title:** Working System Demo: End-to-End Operational Walkthrough
* **Layout Design:** Left column showing the 5-step live demonstration narrative; Right column displaying the 10 built React 18 dashboard modules and active server URLs.
* **Content:**
  * **Live Demonstration Narrative (5 Steps):**
    * **Step 1: Automated Regulatory Acquisition:** User searches Reliance Industries (`RELIANCE`) or Apple (`AAPL`). System discovers SEC CIK (`0000320193`) or NSE symbol and streams audited disclosures.
    * **Step 2: Deterministic Ratio Computation:** Financial Analysis tab renders multi-year profitability, liquidity, and leverage cards with zero arithmetic errors.
    * **Step 3: Transparent ESG Disclosure Audit:** ESG tab decomposes Environmental (30%), Social (30%), and Governance (40%) indicators with visible formula audit.
    * **Step 4: Hybrid RAG AI Analyst Chat:** User asks: *"Why did operating margin change in FY2024?"* System targets FY2024 (+60 bps YoY), outlines 4 MD&A drivers, and renders clickable citation badges.
    * **Step 5: Institutional ReportLab Export:** Generates downloadable multi-page PDF dossiers (with `NumberedCanvas` "Page X of Y" pagination) and HTML dossiers.
  * **10 Dedicated React 18 UI Modules:**
    1. Executive Overview Dashboard | 2. Data Collection Dashboard | 3. Company Management & Discovery | 4. Financial Ratio Analysis | 5. Document Management & Vector Chunk Viewer | 6. AI Financial Analyst Chat | 7. ESG Assessment & Transparency Viewer | 8. Multi-Company Peer Benchmarking | 9. Report Management & Archive | 10. System Settings & Vector DB Diagnostics.
  * **Live Access URLs:** Web UI: `http://localhost:8000` | API Documentation: `http://localhost:8000/docs`
* **Speaker / Presenter Notes:**
  > "Slide 9 covers the live working demo and video demonstration workflow. Our system features 10 fully built React 18 modules. During the live demonstration, we show: 1) live ingestion of Reliance and Apple; 2) deterministic ratio computation with zero hallucinations; 3) transparent ESG decomposition across all 16 indicators; 4) our Hybrid RAG chatbot answering 'Why did operating margin change in FY2024?' with exact MD&A qualitative drivers and clickable page citations; and 5) instant one-click generation of ReportLab PDF and HTML dossiers."

---

### Slide 10: Experimental Results & Benchmarks
* **Slide Category:** 5. Results — Performance Evaluation
* **Slide Title:** Experimental Results: Retrieval Benchmarks & Precision
* **Layout Design:** Empirical retrieval performance table + experimental takeaways card + zero-hallucination verification banner.
* **Content:**

| Retrieval Pipeline Configuration | P@5 | P@10 | MRR@10 | NDCG@10 |
| :--- | :---: | :---: | :---: | :---: |
| **Dense Only** (`BAAI/bge-small-en-v1.5`) | 0.680 | 0.540 | 0.732 | 0.715 |
| **Sparse Only** (Okapi BM25) | 0.640 | 0.510 | 0.684 | 0.662 |
| **Hybrid Fusion** (RRF $k=60$) | 0.820 | 0.690 | 0.841 | 0.828 |
| **Hybrid + Cross-Encoder Reranker (Our System)** | **0.920** | **0.780** | **0.916** | **0.898** |

  * **Key Experimental Takeaways:**
    * **Retrieval Gain (+25.1% MRR):** Fusing Dense + BM25 via RRF and Cross-Encoder reranking boosted Mean Reciprocal Rank from 0.732 to **0.916** (+25.1% relative gain over dense alone).
    * **100.0% Mathematical Precision:** Zero calculation errors across all queries; numbers match audited statutory filings to 2 decimal places.
    * **Automated Test Validation:** **21/21 Unit and Integration Tests Passing** in 14.63s via Pytest.
* **Speaker / Presenter Notes:**
  > "Slide 10 presents our empirical retrieval benchmarks and accuracy results. We benchmarked four retrieval configurations on audited corporate filings: dense alone, BM25 alone, hybrid fusion via RRF, and hybrid fusion with cross-encoder reranking. Our hybrid pipeline with cross-encoder reranking achieves an MRR@10 of 0.916 and P@5 of 0.920—a massive 25.1% relative improvement over standard dense retrieval. On arithmetic, our dual-pathway architecture achieves 100% precision, completely eliminating LLM calculation errors."

---

### Slide 11: Latency Profile & Computational Efficiency
* **Slide Category:** 5. Results — Latency & System Profile
* **Slide Title:** Latency Profile: Sub-Second Execution on Commodity CPU
* **Layout Design:** 10-row system latency breakdown table + hardware profile card.
* **Content:**

| System Component / Pipeline Stage | Mean Latency (ms) | Execution Mechanism |
| :--- | :---: | :--- |
| **Query Intent Routing** | 2.1 ms | Compiled Regex Classifier |
| **Financial Ratio Engine (3 Years)** | **1.1 ms** | Vectorized Python / Pandas Engine |
| **Balance Sheet Invariant Check** | 0.4 ms | Accounting Invariant Equation |
| **ESG Indicator Scoring (16 metrics)** | 0.8 ms | Vectorized NumPy Normalizer |
| **Dense Query Embedding Generation** | 14.2 ms | FastEmbed (`bge-small-en` ONNX) |
| **Qdrant Vector Search ($K=20$)** | 4.6 ms | Local Cosine Index |
| **Okapi BM25 Lexical Search ($K=20$)** | 1.8 ms | In-Memory Inverted Token Index |
| **Reciprocal Rank Fusion ($k=60$)** | 0.3 ms | Pure Python Dictionary Sort |
| **Cross-Encoder Reranking (Top-20)** | 64.2 ms | ONNX Cross-Attention Transformer |
| **ReportLab PDF Generation (5 Pages)** | 182.4 ms | Flowable Two-Pass Canvas |
| **Total End-to-End Execution** | **~271.9 ms** | **Sub-Second Real-Time Response** |

  * **Hardware & Efficiency Highlights:**
    * **Zero GPU Requirement:** Executes on standard multi-core commodity CPUs using quantized ONNX runtimes.
    * **Memory Footprint:** Operates within `< 650 MB RAM` for the entire server, vector store, and SQLite database.
* **Speaker / Presenter Notes:**
  > "Slide 11 breaks down our system latency profile. A common drawback of modern AI applications is that they require heavy, expensive GPU clusters and take several seconds per turn. Our architecture runs entirely on standard commodity CPU hardware using quantized ONNX runtimes. Query routing takes 2.1 ms, financial math takes 1.1 ms, hybrid search and reranking take under 90 ms, and the full end-to-end query cycle completes in ~271.9 ms—well under half a second."

---

### Slide 12: Future Work & Architectural Roadmap
* **Slide Category:** 6. Future Work
* **Slide Title:** Future Work: Technical Roadmap & System Extensions
* **Layout Design:** 3 phased engineering cards (Short-Term, Medium-Term, Long-Term).
* **Content:**
  * **Phase 1: Advanced Multimodal Table Transformers (Short-Term)**
    * *Challenge:* Complex historical annual reports feature borderless nested tables and merged cells that create noise in basic text extraction.
    * *Engineering Solution:* Integrate Table-Transformer (TATR) and LayoutLMv3 object detection models to extract multi-level tabular grids directly from document images.
  * **Phase 2: SASB Dynamic Sector-Materiality ESG Matrix (Medium-Term)**
    * *Challenge:* Current ESG model uses fixed 30/30/40 pillar weights, which does not account for differing industry materiality.
    * *Engineering Solution:* Incorporate dynamic SASB (Sustainability Accounting Standards Board) 77-industry materiality matrices (e.g. heavier weight on Scope 1 for energy; heavier weight on cybersecurity for tech).
  * **Phase 3: Real-Time Tick Streaming & Multi-Agent Teams (Long-Term)**
    * *Challenge:* Current system analyzes periodic filings rather than live market prices.
    * *Engineering Solution:* Connect WebSocket feeds for live tick-by-tick prices and orchestrate multi-agent teams (Forensic Accounting Agent + Macro Sentiment Agent) for autonomous post-earnings research dossiers.
* **Speaker / Presenter Notes:**
  > "Slide 12 outlines our future work roadmap in three phased engineering steps. In the short term, we plan to integrate Table-Transformer (TATR) vision models for borderless, nested tables. In the medium term, we will replace static 30/30/40 ESG weights with dynamic SASB 77-industry materiality matrices. In the long term, we aim to integrate live WebSocket market tick data and orchestrate multi-agent collaborative teams that autonomously generate equity dossiers immediately after earnings conference calls."

---

### Slide 13: Team Learnings: Individual Contributions & Takeaways
* **Slide Category:** 7. Your LEARNING — Contributions & Growth
* **Slide Title:** Team Learnings: Individual Contributions & Takeaways
* **Layout Design:** Two-column card split between Vivek Upadhyay and Ashish Rolaniya.
* **Content:**
  * **Vivek Upadhyay (Team Captain — Roll No: `2023UAI1996`):**
    * *Architectural Contributions:*
      * Formulated the Dual-Pathway system architecture separating deterministic math from generative language.
      * Engineered SEC EDGAR XBRL (10,400+ companies) and Indian Exchange (NSE/BSE) automated connectors.
      * Implemented Hybrid RAG pipeline combining Qdrant dense vector search, BM25 lexical search, and RRF rank fusion.
      * Developed the Cross-Encoder neural reranker and FastAPI backend API routing.
    * *Key Learnings & Growth:*
      * Gained deep expertise in enterprise Information Retrieval (IR) and resolving vocabulary drift in financial contexts.
      * Mastered SEC EDGAR XBRL taxonomy, hierarchical JSON data structures, and balance sheet identity reconciliation.
      * Learned how to design fail-safe AI pipelines that strictly eliminate LLM hallucinations through deterministic code safeguards.
  * **Ashish Rolaniya (Co-Investigator — Roll No: `2023UAI1825`):**
    * *Architectural Contributions:*
      * Implemented the transparent ESG scoring engine across Environmental (30%), Social (30%), and Governance (40%) pillars.
      * Engineered the zero-penalty non-disclosure logic and the mandatory 30% coverage withholding gate.
      * Built the ReportLab institutional PDF dossier generator utilizing a dynamic two-pass `NumberedCanvas` for "Page X of Y" pagination.
      * Developed the React 18 / TypeScript frontend dashboard and authored the 21-test automated Pytest suite.
    * *Key Learnings & Growth:*
      * Acquired in-depth knowledge of SEBI BRSR and GRI non-financial disclosure reporting frameworks.
      * Mastered programmatic PDF typesetting, 2D coordinate layouts, and dynamic canvas generation in ReportLab.
      * Gained strong engineering discipline in full-stack state management, API proxying, and comprehensive integration testing.
* **Speaker / Presenter Notes:**
  > "Slide 13 details our individual project contributions and key personal learnings. As Team Captain, I, Vivek Upadhyay, focused on the system architecture, the automated regulatory connectors for SEC EDGAR and Indian exchanges, the Hybrid RAG pipeline with Qdrant and BM25, and the Cross-Encoder reranker. I learned how to address vocabulary drift and design deterministic fail-safes. My co-investigator, Ashish Rolaniya, engineered the transparent ESG scoring engine, the ReportLab PDF dossier generator with two-pass canvas numbering, the React 18 user interface, and the automated test suite. Ashish deepened his expertise in sustainability reporting frameworks and robust UI/UX engineering."

---

### Slide 14: Conclusion & Academic Deliverables
* **Slide Category:** Project Conclusion & Q/A
* **Slide Title:** Conclusion & Academic Deliverables
* **Layout Design:** 2x2 grid of final project deliverables + Q&A invitation banner.
* **Content:**
  * **Deliverable 1 — Operational Full-Stack Prototype:**
    * Fully deployed with FastAPI, React 18, Qdrant, and SQLite/PostgreSQL.
    * Live system running on `http://localhost:8000`.
    * 21/21 automated unit and integration tests passing in 14.63s.
  * **Deliverable 2 — IEEE 2-Column Research Paper:**
    * 7-page academic manuscript formatted in IEEE Conference style.
    * Complete LaTeX source (`.tex`) and compiled PDF in academic submission folder.
    * Detailed methodology, retrieval benchmarks, and formal mathematical formulations.
  * **Deliverable 3 — Annotated Literature Catalogue:**
    * Curated catalogue of 19 verified SOTA research papers with active DOIs.
    * Complete BibTeX bibliography file (`references.bib`) provided.
  * **Deliverable 4 — Open-Source GitHub Repository:**
    * Full source code, test suites, and documentation published.
    * URL: `https://github.com/vivekmnit1996/AI-Financial-Analyst`
* **Speaker / Presenter Notes:**
  > "In conclusion, our B.Tech project demonstrates that AI can be used reliably in high-stakes corporate finance when architected with deterministic safeguards. We have delivered a complete operational prototype, an IEEE research paper, a verified literature catalogue, and an open-source codebase. We want to thank our project mentor and the Department of Artificial Intelligence and Data Engineering at MNIT Jaipur. We now welcome questions and discussion from the committee."
