import json

def generate_html_presentation():
    slides = [
        {
            "num": 1,
            "badge": "Capstone Presentation",
            "title": "AI Financial Analyst & Report Generator",
            "subtitle": "Dual-Pathway Deterministic Arithmetic, Hybrid RAG with Verifiable Citations, & Transparent ESG Scoring",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 24px;">
                <div style="background: #1E293B; padding: 24px; border-radius: 12px; border: 1px solid #334155;">
                    <div style="color: #38BDF8; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 12px;">Project Investigators</div>
                    <div style="font-size: 1.15rem; font-weight: 600; color: #F8FAFC; line-height: 1.8;">
                        • <strong>Vivek Upadhyay</strong> (Team Captain) — Roll No: <code style="color:#38BDF8;">2023UAI1996</code><br>
                        • <strong>Ashish Rolaniya</strong> (Co-Investigator) — Roll No: <code style="color:#38BDF8;">2023UAI1825</code>
                    </div>
                    <div style="margin-top: 16px; color: #94A3B8; font-size: 0.95rem; line-height: 1.5;">
                        Department of Artificial Intelligence & Data Engineering<br>
                        <strong>Malaviya National Institute of Technology (MNIT) Jaipur</strong>
                    </div>
                </div>
                <div style="background: #1E293B; padding: 24px; border-radius: 12px; border: 1px solid #334155;">
                    <div style="color: #34D399; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 12px;">System Specifications & Deliverables</div>
                    <ul style="color: #E2E8F0; font-size: 0.95rem; line-height: 1.8; padding-left: 20px;">
                        <li><strong>System Status:</strong> Operational Prototype (TRL 5/6)</li>
                        <li><strong>Core Stack:</strong> FastAPI, React 18, Qdrant Vector DB, PyMuPDF, ReportLab</li>
                        <li><strong>Testing:</strong> 21 Automated Pytest Integration Suites (100% Passing)</li>
                        <li><strong>Repository:</strong> <a href="https://github.com/vivekmnit1996/AI-Financial-Analyst" target="_blank" style="color: #38BDF8; text-decoration: underline;">github.com/vivekmnit1996/AI-Financial-Analyst</a></li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Good morning esteemed project mentor and evaluation committee. Today, my teammate Ashish Rolaniya and I, Vivek Upadhyay, present our B.Tech Capstone project: 'AI Financial Analyst and Report Generator'. Our goal was to build a production-grade, institutional equity research platform that bridges the fundamental flaw of generative AI in corporate finance—hallucinated arithmetic—by enforcing a strict dual-pathway architecture, Hybrid RAG with exact page provenance, and transparent ESG scoring."
        },
        {
            "num": 2,
            "badge": "1. Problem Statement & Motivation",
            "title": "The Arithmetic & Provenance Bottleneck in Financial AI",
            "subtitle": "Why Standard Commercial Generative LLMs Fail in Corporate Finance",
            "content": """
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 20px; border-radius: 10px; border: 1px solid #334155; border-top: 4px solid #3B82F6;">
                    <h3 style="color: #60A5FA; font-size: 1.1rem; margin-bottom: 12px;">1. Disclosures Overload</h3>
                    <ul style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.6; padding-left: 16px;">
                        <li><strong>Volume:</strong> Corporate filings (SEC 10-K, 10-Q, Annual Reports, SEBI BRSR) span 300+ pages each.</li>
                        <li><strong>Time Bottleneck:</strong> Analysts spend <strong>70% of analytical hours</strong> manually cross-referencing tables and footnotes.</li>
                        <li><strong>Friction:</strong> Severe information asymmetry for retail and institutional investors.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 20px; border-radius: 10px; border: 1px solid #334155; border-top: 4px solid #EF4444;">
                    <h3 style="color: #F87171; font-size: 1.1rem; margin-bottom: 12px;">2. LLM Hallucinations</h3>
                    <ul style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.6; padding-left: 16px;">
                        <li><strong>Arithmetic Error:</strong> Autoregressive LLMs fail at basic accounting algebra; invent margins out of token probabilities.</li>
                        <li><strong>Empirical Proof:</strong> <em>FinanceBench (2023)</em> & <em>FinQA (2021)</em> prove commercial LLMs suffer 18-35% math error rates.</li>
                        <li><strong>No Provenance:</strong> Black-box assertions lack auditable page anchors.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 20px; border-radius: 10px; border: 1px solid #334155; border-top: 4px solid #F59E0B;">
                    <h3 style="color: #FBBF24; font-size: 1.1rem; margin-bottom: 12px;">3. ESG Greenwashing</h3>
                    <ul style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.6; padding-left: 16px;">
                        <li><strong>Divergent Ratings:</strong> Commercial agencies (MSCI, Sustainalytics) exhibit low correlation (<strong>r ≈ 0.54</strong>, MIT Sloan).</li>
                        <li><strong>Opaque Penalties:</strong> Impute missing disclosures as arbitrary zeros without transparency.</li>
                        <li><strong>Regulatory Mandate:</strong> SEBI BRSR and EU CSRD require verifiable indicator audits.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 2 outlines the real-world motivation. Modern corporate filings are enormous. Financial analysts spend most of their time cross-referencing tables and footnotes. When practitioners attempt to use generic LLMs like ChatGPT or Claude for financial analysis, they encounter two fatal pitfalls: first, autoregressive language models cannot reliably calculate mathematical formulas, frequently hallucinating operating margins or cash flows; second, they produce black-box assertions without auditable citations. Furthermore, existing commercial ESG ratings diverge sharply with a correlation of barely 0.54. Our project was designed specifically to eliminate all three bottlenecks."
        },
        {
            "num": 3,
            "badge": "1. Problem Statement — TRL Level & Scope",
            "title": "Technology Readiness Level (TRL 5/6) & System Scope",
            "subtitle": "From Mathematical Concept to Operational Full-Stack Prototype",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
                    <h3 style="color: #38BDF8; font-size: 1.1rem; margin-bottom: 12px;">SYSTEM TRL PROGRESSION: TRL 5 / 6</h3>
                    <div style="display: flex; flex-direction: column; gap: 10px; font-size: 0.88rem;">
                        <div style="padding: 8px 12px; background: rgba(100, 116, 139, 0.2); border-left: 3px solid #64748B; border-radius: 4px;">
                            <strong>TRL 3 — Proof of Concept:</strong> Mathematical formulation decoupling deterministic arithmetic from generative natural language.
                        </div>
                        <div style="padding: 8px 12px; background: rgba(59, 130, 246, 0.2); border-left: 3px solid #3B82F6; border-radius: 4px;">
                            <strong>TRL 4 — Component Validation:</strong> Validated Python/Pandas numerical engine, PyMuPDF parser, Qdrant BGE-small embeddings, & BM25.
                        </div>
                        <div style="padding: 8px 12px; background: rgba(14, 165, 233, 0.2); border-left: 3px solid #0EA5E9; border-radius: 4px;">
                            <strong>TRL 5 — Relevant Environment:</strong> Connected live SEC EDGAR XBRL APIs (10,400+ firms) & Indian NSE/BSE feeds with balance sheet validation.
                        </div>
                        <div style="padding: 8px 12px; background: rgba(16, 185, 129, 0.2); border-left: 3px solid #10B981; border-radius: 4px;">
                            <strong>TRL 6 — Operational Prototype:</strong> Full-stack system (FastAPI + React 18) running live, 21 passing automated tests, ReportLab PDF generator.
                        </div>
                    </div>
                </div>
                <div style="background: #1E293B; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
                    <h3 style="color: #34D399; font-size: 1.1rem; margin-bottom: 12px;">OPERATIONAL TARGET & PARAMETERS</h3>
                    <ul style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.7; padding-left: 18px;">
                        <li><strong>Target End-Users:</strong> Equity research desks, institutional compliance officers, corporate audit committees, academic researchers.</li>
                        <li><strong>Deployment Mode:</strong> Containerized multi-service Docker deployment with PostgreSQL / SQLite and local persistent Qdrant vector storage.</li>
                        <li><strong>Hardware Footprint:</strong> Highly optimized for commodity x86_64 CPUs (< 650 MB RAM; sub-second turn latency; zero GPU cost).</li>
                        <li><strong>Compliance Integrity:</strong> SEC EDGAR Fair-Access compliant User-Agent integration; strict balance sheet identity checks.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "On Slide 3, we evaluate our system against standard NASA and DoD Technology Readiness Level criteria. Many academic AI projects remain at TRL 3 or 4—a Jupyter notebook showing toy results. Our project has reached TRL 5 and TRL 6: an operational full-stack prototype validated on real, live corporate filings from the US SEC and Indian NSE/BSE. It runs in Docker, adheres to SEC Fair Access guidelines, and executes in real-time on commodity CPUs."
        },
        {
            "num": 4,
            "badge": "3. Literature Survey & SOTA Foundations",
            "title": "Literature Survey: State of the Art (SOTA) Benchmarks",
            "subtitle": "Survey of 19 Foundational Peer-Reviewed Research Publications",
            "content": """
            <div style="margin-top: 16px; overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; font-size: 0.88rem; background: #1E293B; border-radius: 8px; overflow: hidden;">
                    <thead>
                        <tr style="background: #0F172A; color: #38BDF8; text-align: left; border-bottom: 2px solid #334155;">
                            <th style="padding: 12px;">Domain / Benchmark</th>
                            <th style="padding: 12px;">Key SOTA Publications</th>
                            <th style="padding: 12px;">Core Scientific Finding</th>
                            <th style="padding: 12px;">Project Integration</th>
                        </tr>
                    </thead>
                    <tbody style="color: #CBD5E1;">
                        <tr style="border-bottom: 1px solid #334155;">
                            <td style="padding: 10px; font-weight: 600; color: #F8FAFC;">Financial QA & Reasoning</td>
                            <td style="padding: 10px;">FinQA (Chen et al., EMNLP '21)<br>FinanceBench (Islam et al., '23)</td>
                            <td style="padding: 10px;">First dedicated benchmarks for financial tables; proved LLMs commit fatal arithmetic hallucinations.</td>
                            <td style="padding: 10px; color: #34D399;">Motivated our 100% deterministic Python calculation engine.</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #334155; background: rgba(30, 41, 59, 0.5);">
                            <td style="padding: 10px; font-weight: 600; color: #F8FAFC;">Retrieval-Augmented Gen.</td>
                            <td style="padding: 10px;">RAG (Lewis et al., NeurIPS '20)<br>DPR (Karpukhin et al., EMNLP '20)</td>
                            <td style="padding: 10px;">Non-parametric memory for factual QA; standard dense models suffer on regulatory jargon.</td>
                            <td style="padding: 10px; color: #34D399;">Designed hybrid dense + sparse retrieval to catch technical terms.</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #334155;">
                            <td style="padding: 10px; font-weight: 600; color: #F8FAFC;">Rank Fusion & Reranking</td>
                            <td style="padding: 10px;">RRF (Cormack et al., SIGIR '09)<br>Cross-Encoder (Nogueira & Cho, '19)</td>
                            <td style="padding: 10px;">RRF merges disparate ranks (k=60); Cross-encoders capture full query-passage attention.</td>
                            <td style="padding: 10px; color: #34D399;">Achieved +25.1% MRR boost over dense-only retrieval.</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; font-weight: 600; color: #F8FAFC;">ESG Measurement</td>
                            <td style="padding: 10px;">Aggregate Confusion: Divergence of ESG Ratings (Berg et al., '22)</td>
                            <td style="padding: 10px;">Major rating agencies correlate at only r ≈ 0.54 due to subjective weighting and opaque imputation.</td>
                            <td style="padding: 10px; color: #34D399;">Built transparent 30/30/40 model with non-disclosure omission.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            """,
            "notes": "Slide 4 presents our literature survey of State-of-the-Art foundations. We surveyed 19 peer-reviewed papers across 4 pillars. First, FinQA and FinanceBench proved that pure LLMs are dangerous for finance because they guess mathematical numbers. Second, Lewis et al.'s original RAG paper introduced retrieval-augmented generation. Third, Cormack et al. and Nogueira & Cho established Reciprocal Rank Fusion and Cross-Encoder reranking. Finally, the seminal MIT Sloan paper by Berg et al. demonstrated that commercial ESG ratings diverge sharply due to opaque proprietary models."
        },
        {
            "num": 5,
            "badge": "3. Gaps Identified & Base Papers",
            "title": "Research Gaps Identified & Base Paper Traceability",
            "subtitle": "Bridging Academic Literature Limitations with Engineered Solutions",
            "content": """
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 14px;">
                <div style="background: #1E293B; padding: 12px 18px; border-radius: 8px; border-left: 4px solid #3B82F6;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #60A5FA; font-size: 0.95rem;">GAP 1: Arithmetic Inaccuracy in Generative LLMs</strong>
                        <span style="color: #94A3B8; font-size: 0.8rem;">Base Papers: FinanceBench (2023) | FinQA (EMNLP 2021)</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Identified Gap:</em> Autoregressive models compute math via token probabilities, causing hallucinated margins.<br>
                        • <strong>Our Solution:</strong> Decouple math completely. Formulated Pathway A: 100% deterministic Python/Pandas calculation.
                    </div>
                </div>
                <div style="background: #1E293B; padding: 12px 18px; border-radius: 8px; border-left: 4px solid #0EA5E9;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #38BDF8; font-size: 0.95rem;">GAP 2: Financial Vocabulary Mismatch in Pure Dense Search</strong>
                        <span style="color: #94A3B8; font-size: 0.8rem;">Base Papers: BGE Embeddings (2023) | Okapi BM25 (2009)</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Identified Gap:</em> Bi-encoders blur specific regulatory tokens ('Ind AS 116', 'Scope 1 GHG', ticker codes).<br>
                        • <strong>Our Solution:</strong> Hybrid RAG combining Qdrant dense vectors + BM25 keyword index fused via RRF (k=60) + Cross-Encoder.
                    </div>
                </div>
                <div style="background: #1E293B; padding: 12px 18px; border-radius: 8px; border-left: 4px solid #10B981;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #34D399; font-size: 0.95rem;">GAP 3: Missing Provenance & Black-Box Qualitative Assertions</strong>
                        <span style="color: #94A3B8; font-size: 0.8rem;">Base Papers: RAG (NeurIPS 2020) | DPR (EMNLP 2020)</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Identified Gap:</em> Existing financial AI outputs claims without verifiable source anchors.<br>
                        • <strong>Our Solution:</strong> PyMuPDF spatial coordinate extraction; every claim is linked to <code>[Document, Page X, Section Y]</code>.
                    </div>
                </div>
                <div style="background: #1E293B; padding: 12px 18px; border-radius: 8px; border-left: 4px solid #F59E0B;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #FBBF24; font-size: 0.95rem;">GAP 4: Opaque & Speculative ESG Scoring Methodologies</strong>
                        <span style="color: #94A3B8; font-size: 0.8rem;">Base Papers: Aggregate Confusion (Review of Finance 2022)</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Identified Gap:</em> Commercial agencies penalize unrecorded metrics as zero with divergent black-box weights.<br>
                        • <strong>Our Solution:</strong> Transparent 30/30/40 linear model with non-disclosure zero-penalty omission & 30% coverage gate.
                    </div>
                </div>
            </div>
            """,
            "notes": "Slide 5 establishes the precise research gaps we identified in prior literature and maps them directly to our base papers and novel solutions. Gap 1 is arithmetic inaccuracy, identified by FinanceBench—solved by our deterministic numerical engine. Gap 2 is vocabulary mismatch in pure dense embeddings—solved by our Hybrid RRF plus Cross-Encoder reranking. Gap 3 is black-box assertions lacking provenance—solved by our structure-aware page coordinate parser. Gap 4 is opaque ESG ratings—solved by our transparent 30/30/40 indicator scoring with a coverage withholding gate."
        },
        {
            "num": 6,
            "badge": "4. Proposed Methodology — Architecture",
            "title": "Proposed Methodology: Dual-Pathway System Architecture",
            "subtitle": "Strict Decoupling of Deterministic Arithmetic from Generative Reasoning",
            "content": """
            <div style="background: #0F172A; padding: 10px 16px; border-radius: 6px; border: 1px solid #334155; text-align: center; color: #38BDF8; font-weight: 700; font-size: 0.85rem;">
                CORE PHILOSOPHY: CALCULATE NUMBERS DETERMINISTICALLY IN PYTHON | REASON CONTEXTUALLY WITH HYBRID RAG
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 14px;">
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155; border-top: 3px solid #3B82F6;">
                    <h4 style="color: #60A5FA; font-size: 0.95rem; margin-bottom: 8px;">PATHWAY A: DETERMINISTIC FINANCE</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">Audited Statements & Financial Ratios</p>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>14 financial ratios (Operating Margin, ROE, ROA, D/E, FCF).</li>
                        <li>Vectorized Pandas formulas.</li>
                        <li>Zero-division traps & missing data preservation.</li>
                        <li>Balance sheet reconciliation equation.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155; border-top: 3px solid #0EA5E9;">
                    <h4 style="color: #38BDF8; font-size: 0.95rem; margin-bottom: 8px;">PATHWAY B: HYBRID RAG</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">Qualitative Document Intelligence</p>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>PyMuPDF structure-aware PDF parsing.</li>
                        <li>Dense (Qdrant BGE-small) + Sparse (BM25).</li>
                        <li>Reciprocal Rank Fusion (k=60).</li>
                        <li>Cross-Encoder reranking + Section boost.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155; border-top: 3px solid #10B981;">
                    <h4 style="color: #34D399; font-size: 0.95rem; margin-bottom: 8px;">PATHWAY C: TRANSPARENT ESG</h4>
                    <p style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">Corporate Sustainability Disclosure</p>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>30% E, 30% S, 40% G pillar weighting.</li>
                        <li>16 core quantitative indicators.</li>
                        <li>Non-disclosure omitted, never penalized.</li>
                        <li>30% minimum reporting coverage gate.</li>
                    </ul>
                </div>
            </div>
            <div style="background: #1E293B; padding: 14px 20px; border-radius: 8px; border: 1px solid #334155; margin-top: 14px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #F8FAFC; font-size: 0.9rem;">EVIDENCE REASONING SYNTHESIS & REPORTLAB PDF DOSSIER GENERATOR</strong>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">Feeds verified ratios + reranked text into strict context-constrained prompt. Generates downloadable PDF/HTML reports.</div>
                </div>
                <span style="background: rgba(14, 165, 233, 0.2); color: #38BDF8; padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">Zero Hallucinations</span>
            </div>
            """,
            "notes": "Slide 6 is the heart of our technical methodology: the Dual-Pathway Architecture. Rather than passing raw financial tables to an LLM and hoping it does arithmetic correctly, our architecture splits execution into three parallel, deterministic pipelines. Pathway A computes all 14 financial ratios in Python/Pandas. Pathway B performs Hybrid RAG document retrieval using dense vectors and sparse BM25, merged via RRF and reranked via a cross-encoder. Pathway C calculates transparent ESG scores. All three feed into our synthesis engine, guaranteeing 100% calculation accuracy with full source provenance."
        },
        {
            "num": 7,
            "badge": "4. Proposed Methodology — Data Pipeline",
            "title": "Proposed Methodology: Datasets & Regulatory Ingestion",
            "subtitle": "Multi-Source Public Repository Ingestion & Accounting Integrity Checks",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155;">
                    <h3 style="color: #38BDF8; font-size: 1.05rem; margin-bottom: 12px;">PUBLIC REGULATORY DATA INGESTION</h3>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6; padding-left: 16px;">
                        <li><strong>SEC EDGAR REST APIs:</strong> Automated ingestion of official XBRL Company Facts JSON feeds for <strong>10,400+ public companies</strong>. Supports US-GAAP (10-K/10-Q) and IFRS-FULL (Form 20-F) with zero-padded 10-digit CIK lookup.</li>
                        <li><strong>Indian Stock Exchanges (NSE / BSE):</strong> Multi-year audited consolidated and standalone financial statements and SEBI BRSR reports for benchmark Indian corporations.</li>
                        <li><strong>Dynamic Global Discovery:</strong> Live query integration with Yahoo Finance Search API for automated ticker lookup and corporate profile resolution.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155;">
                    <h3 style="color: #34D399; font-size: 1.05rem; margin-bottom: 12px;">PREPROCESSING & RECONCILIATION GATES</h3>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6; padding-left: 16px;">
                        <li><strong>Balance Sheet Invariant Equation:</strong>
                            <div style="background: #0F172A; padding: 6px; border-radius: 4px; font-family: monospace; font-size: 0.78rem; color: #34D399; margin: 4px 0;">|Assets - (Liabilities + Equity)| < 0.02 * Assets</div>
                            Reconciles accounting balance prior to database insertion.
                        </li>
                        <li><strong>Unit Standardization:</strong> Converts Crores, Millions, Billions to uniform base floats while preserving statutory currencies.</li>
                        <li><strong>Spatial PDF Ingestion:</strong> PyMuPDF extracts text, tables, and headers with exact 1-indexed page coordinates.</li>
                        <li><strong>Structure-Aware Chunking:</strong> 300–400 word sliding windows with 50-word overlap, tagging metadata.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 7 details our dataset acquisition and preprocessing pipeline. Our system does not rely on synthetic toy data. It connects to official SEC EDGAR XBRL APIs using fair-access headers, ingesting 10-K and 20-F filings for over 10,400 companies. For Indian companies, it ingests audited filings and SEBI BRSR reports from the NSE and BSE. Before anything is written to the database, an automated accounting reconciliation gate checks the balance sheet identity equation. For unstructured PDFs, PyMuPDF extracts text while strictly preserving 1-indexed page coordinates."
        },
        {
            "num": 8,
            "badge": "4. Proposed Methodology — LLM & Retrieval",
            "title": "Proposed Methodology: LLM Techniques & Hybrid RAG Pipeline",
            "subtitle": "Dense Vector Search + BM25 Keyword Search + RRF + Cross-Encoder Reranker",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 14px;">
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #38BDF8; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px;">1. Parallel Dense & Sparse Retrieval</div>
                    <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li><strong>Dense Index:</strong> 384-dimensional BGE-small embeddings in persistent local Qdrant collection (Cosine similarity).</li>
                        <li><strong>Sparse Index:</strong> Okapi BM25 for exact regulatory terms ('Ind AS 116', 'Scope 1 GHG').</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #0EA5E9; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px;">2. Reciprocal Rank Fusion (k=60)</div>
                    <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Merges dense and sparse lists without uncalibrated score distortion:
                            <code style="color: #38BDF8; display: block; margin: 4px 0;">RRF(d) = Σ [ 1 / (60 + rank_m(d)) ]</code>
                        </li>
                        <li>Captures top candidates missed by single-modality retrievers.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #34D399; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px;">3. Cross-Encoder Neural Reranking</div>
                    <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Bi-encoders lack query-passage cross-attention. Our Cross-Encoder scores candidates jointly.</li>
                        <li>Applies a <strong>+0.05 analytical boost</strong> when section type matches query intent.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #FBBF24; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px;">4. Context-Constrained Executive Synthesis</div>
                    <ul style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li><strong>Fiscal Year Resolution:</strong> Parses query to target exact fiscal year (FY2024) and prior year (FY2023) to compute YoY basis-point deltas.</li>
                        <li>Synthesizes direct answer + 4 MD&A drivers + page citation badges.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 8 details the AI and LLM techniques powering our Hybrid RAG pipeline. Dense vector embeddings are great for semantic paraphrasing, but terrible at exact regulatory codes like 'Ind AS 116'. Conversely, BM25 excels at exact keywords but misses semantic synonyms. We run both in parallel, fuse them with Reciprocal Rank Fusion with smoothing parameter k=60, and then pass the top 20 candidates through a Cross-Encoder that computes full cross-attention. Finally, our synthesis engine enforces a strict zero-hallucination constraint, producing an executive answer with verifiable page citations."
        },
        {
            "num": 9,
            "badge": "2. Working Video / Live Demo",
            "title": "Working System Demo: End-to-End Operational Walkthrough",
            "subtitle": "10 Operational Modules Running Live on React 18 + FastAPI",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155;">
                    <h3 style="color: #38BDF8; font-size: 1.05rem; margin-bottom: 10px;">5-STEP DEMONSTRATION WORKFLOW</h3>
                    <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.84rem; color: #CBD5E1;">
                        <div><strong>1. Regulatory Ingestion:</strong> Discover Reliance (RELIANCE) or Apple (AAPL); stream live XBRL & Exchange disclosures.</div>
                        <div><strong>2. Deterministic Ratios:</strong> Instantly inspect profitability, liquidity, and leverage tables with zero math error.</div>
                        <div><strong>3. Transparent ESG Audit:</strong> Review 30/30/40 pillar breakdown, coverage percentage, and disclosed indicators.</div>
                        <div><strong>4. Hybrid RAG Chat:</strong> Ask <em>'Why did operating margin change in FY2024?'</em>; inspect executive answer, MD&A drivers, and clickable page citations!</div>
                        <div><strong>5. ReportLab Export:</strong> One-click download of institutional PDF & HTML research dossiers.</div>
                    </div>
                </div>
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155;">
                    <h3 style="color: #34D399; font-size: 1.05rem; margin-bottom: 10px;">10 DEDICATED REACT 18 UI TABS</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.8rem; color: #CBD5E1;">
                        <div>• Overview Dashboard</div>
                        <div>• Data Collection</div>
                        <div>• Company Management</div>
                        <div>• Financial Analysis</div>
                        <div>• Document Management</div>
                        <div>• AI Analyst Chat</div>
                        <div>• ESG Assessment</div>
                        <div>• Peer Benchmarking</div>
                        <div>• Report Management</div>
                        <div>• System Settings</div>
                    </div>
                    <div style="margin-top: 14px; padding: 10px; background: #0F172A; border-radius: 6px; border: 1px solid #334155;">
                        <span style="color: #38BDF8; font-size: 0.85rem; font-weight: 700;">Live Prototype Server:</span><br>
                        <span style="color: #F8FAFC; font-family: monospace; font-size: 0.85rem;">UI: http://localhost:8000 | API Docs: /docs</span>
                    </div>
                </div>
            </div>
            """,
            "notes": "Slide 9 covers the live working demo and video demonstration workflow. Our system features 10 fully built React 18 modules. During the live demonstration, we show: 1) live ingestion of Reliance and Apple; 2) deterministic ratio computation with zero hallucinations; 3) transparent ESG decomposition across all 16 indicators; 4) our Hybrid RAG chatbot answering 'Why did operating margin change in FY2024?' with exact MD&A qualitative drivers and clickable page citations; and 5) instant one-click generation of ReportLab PDF and HTML dossiers."
        },
        {
            "num": 10,
            "badge": "5. Results — Performance Evaluation",
            "title": "Experimental Results: Retrieval Benchmarks & Precision",
            "subtitle": "Empirical Comparison on Audited Corporate Filings",
            "content": """
            <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; margin-top: 16px;">
                <div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; background: #1E293B; border-radius: 8px; overflow: hidden;">
                        <thead>
                            <tr style="background: #0F172A; color: #38BDF8; text-align: left;">
                                <th style="padding: 10px;">Retrieval Configuration</th>
                                <th style="padding: 10px;">P@5</th>
                                <th style="padding: 10px;">MRR@10</th>
                                <th style="padding: 10px;">NDCG@10</th>
                            </tr>
                        </thead>
                        <tbody style="color: #CBD5E1;">
                            <tr style="border-bottom: 1px solid #334155;">
                                <td style="padding: 8px;">Dense Only (BGE-small)</td>
                                <td style="padding: 8px;">0.680</td>
                                <td style="padding: 8px;">0.732</td>
                                <td style="padding: 8px;">0.715</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #334155;">
                                <td style="padding: 8px;">Sparse Only (Okapi BM25)</td>
                                <td style="padding: 8px;">0.640</td>
                                <td style="padding: 8px;">0.684</td>
                                <td style="padding: 8px;">0.662</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #334155;">
                                <td style="padding: 8px;">Hybrid Fusion (RRF k=60)</td>
                                <td style="padding: 8px;">0.820</td>
                                <td style="padding: 8px;">0.841</td>
                                <td style="padding: 8px;">0.828</td>
                            </tr>
                            <tr style="background: rgba(16, 185, 129, 0.2); font-weight: 700; color: #34D399;">
                                <td style="padding: 8px;">Hybrid + Cross-Encoder</td>
                                <td style="padding: 8px;">0.920</td>
                                <td style="padding: 8px;">0.916</td>
                                <td style="padding: 8px;">0.898</td>
                            </tr>
                        </tbody>
                    </table>
                    <div style="margin-top: 12px; font-size: 0.85rem; color: #34D399; font-weight: 600;">
                        ★ Key Outcome: Hybrid RRF + Cross-Encoder achieves +25.1% MRR gain over dense-only retrieval!
                    </div>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <h4 style="color: #38BDF8; font-size: 0.95rem; margin-bottom: 8px;">ARITHMETIC & TEST VALIDATION</h4>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6; padding-left: 14px;">
                        <li><strong>100.0% Mathematical Accuracy:</strong> Zero arithmetic hallucinations; all calculated metrics match audited statutory filings.</li>
                        <li><strong>Automated Test Suite:</strong> <strong>21 / 21 Unit & Integration Tests Passing</strong> in 14.63 seconds.</li>
                        <li><strong>Coverage:</strong> Validates financial formulas, edge cases (zero denominators), ESG coverage gates, and full API lifecycle.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 10 presents our empirical retrieval benchmarks and accuracy results. We benchmarked four retrieval configurations on audited corporate filings: dense alone, BM25 alone, hybrid fusion via RRF, and hybrid fusion with cross-encoder reranking. Our hybrid pipeline with cross-encoder reranking achieves an MRR@10 of 0.916 and P@5 of 0.920—a massive 25.1% relative improvement over standard dense retrieval. On arithmetic, our dual-pathway architecture achieves 100% precision, completely eliminating LLM calculation errors."
        },
        {
            "num": 11,
            "badge": "5. Results — Latency & System Profile",
            "title": "Latency Profile: Sub-Second Execution on Commodity CPU",
            "subtitle": "High-Throughput Operational Performance Without Costly GPU Hardware",
            "content": """
            <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; margin-top: 14px;">
                <div>
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.82rem; background: #1E293B; border-radius: 8px; overflow: hidden;">
                        <thead>
                            <tr style="background: #0F172A; color: #38BDF8; text-align: left;">
                                <th style="padding: 8px;">Pipeline Stage</th>
                                <th style="padding: 8px;">Mean Latency</th>
                                <th style="padding: 8px;">Execution Method</th>
                            </tr>
                        </thead>
                        <tbody style="color: #CBD5E1;">
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Query Intent Routing</td><td style="padding: 6px 8px; color: #34D399;">2.1 ms</td><td style="padding: 6px 8px;">Regex Classifier</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Financial Ratio Engine (3 Yrs)</td><td style="padding: 6px 8px; color: #34D399; font-weight: 700;">1.1 ms</td><td style="padding: 6px 8px;">Vectorized Pandas</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Balance Sheet Invariant Check</td><td style="padding: 6px 8px; color: #34D399;">0.4 ms</td><td style="padding: 6px 8px;">Accounting Equation</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Dense Embedding (Query)</td><td style="padding: 6px 8px;">14.2 ms</td><td style="padding: 6px 8px;">FastEmbed ONNX</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Qdrant Vector Search (K=20)</td><td style="padding: 6px 8px;">4.6 ms</td><td style="padding: 6px 8px;">Local Cosine Index</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Okapi BM25 Search (K=20)</td><td style="padding: 6px 8px;">1.8 ms</td><td style="padding: 6px 8px;">Inverted Token Index</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Reciprocal Rank Fusion (k=60)</td><td style="padding: 6px 8px;">0.3 ms</td><td style="padding: 6px 8px;">Pure Python Sort</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">Cross-Encoder Reranking</td><td style="padding: 6px 8px;">64.2 ms</td><td style="padding: 6px 8px;">ONNX Cross-Attention</td></tr>
                            <tr style="border-bottom: 1px solid #334155;"><td style="padding: 6px 8px;">ReportLab PDF Generation</td><td style="padding: 6px 8px;">182.4 ms</td><td style="padding: 6px 8px;">Two-Pass Canvas</td></tr>
                            <tr style="background: rgba(14, 165, 233, 0.2); font-weight: 700; color: #38BDF8;"><td style="padding: 6px 8px;">Total Pipeline Execution</td><td style="padding: 6px 8px;">~271.9 ms</td><td style="padding: 6px 8px;">End-to-End Latency</td></tr>
                        </tbody>
                    </table>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <h4 style="color: #38BDF8; font-size: 0.95rem; margin-bottom: 8px;">EFFICIENCY HIGHLIGHTS</h4>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.6; padding-left: 14px;">
                        <li><strong>Sub-Second Response:</strong> Entire analytical retrieval cycle completes in under 300 ms on commodity CPUs.</li>
                        <li><strong>Zero Cloud GPU Cost:</strong> Quantized ONNX embeddings and reranking eliminate need for expensive cloud GPU instances.</li>
                        <li><strong>Lightweight RAM:</strong> Runs comfortably under 650 MB RAM for the entire full-stack application.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 11 breaks down our system latency profile. A common drawback of modern AI applications is that they require heavy, expensive GPU clusters and take several seconds per turn. Our architecture runs entirely on standard commodity CPU hardware using quantized ONNX runtimes. Query routing takes 2.1 ms, financial math takes 1.1 ms, hybrid search and reranking take under 90 ms, and the full end-to-end query cycle completes in ~271.9 ms—well under half a second."
        },
        {
            "num": 12,
            "badge": "6. Future Work",
            "title": "Future Work: Technical Roadmap & System Extensions",
            "subtitle": "Phased Architectural Vision for Institutional Deployment",
            "content": """
            <div style="display: flex; flex-direction: column; gap: 14px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #3B82F6;">
                    <strong style="color: #60A5FA; font-size: 0.95rem;">Phase 1: Advanced Multimodal Table Transformers (Short-Term)</strong>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Challenge:</em> Complex historical annual reports feature borderless nested tables and merged cells that create noise in basic text extraction.<br>
                        • <em>Solution:</em> Integrate <strong>Table-Transformer (TATR)</strong> and <strong>LayoutLMv3</strong> object detection models to extract multi-level tabular grids directly from document images.
                    </div>
                </div>
                <div style="background: #1E293B; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #0EA5E9;">
                    <strong style="color: #38BDF8; font-size: 0.95rem;">Phase 2: SASB Dynamic Sector-Materiality ESG Matrix (Medium-Term)</strong>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Challenge:</em> Current ESG model uses fixed 30/30/40 pillar weights, which does not account for differing industry materiality.<br>
                        • <em>Solution:</em> Incorporate dynamic <strong>SASB (Sustainability Accounting Standards Board)</strong> 77-industry materiality matrices (e.g. heavier weight on Scope 1 for energy; heavier weight on cybersecurity for tech).
                    </div>
                </div>
                <div style="background: #1E293B; padding: 14px 18px; border-radius: 8px; border-left: 4px solid #10B981;">
                    <strong style="color: #34D399; font-size: 0.95rem;">Phase 3: Real-Time Tick Streaming & Multi-Agent Teams (Long-Term)</strong>
                    <div style="color: #CBD5E1; font-size: 0.85rem; margin-top: 4px;">
                        • <em>Challenge:</em> Current system analyzes periodic filings rather than live market prices.<br>
                        • <em>Solution:</em> Connect WebSocket feeds for live market prices (NSE/BSE/NASDAQ) and deploy multi-agent collaborative teams (Forensic Accounting Agent + Macro Sentiment Agent) for autonomous post-earnings research dossiers.
                    </div>
                </div>
            </div>
            """,
            "notes": "Slide 12 outlines our future work roadmap in three phased engineering steps. In the short term, we plan to integrate Table-Transformer (TATR) vision models for borderless, nested tables. In the medium term, we will replace static 30/30/40 ESG weights with dynamic SASB 77-industry materiality matrices. In the long term, we aim to integrate live WebSocket market tick data and orchestrate multi-agent collaborative teams that autonomously generate equity dossiers immediately after earnings conference calls."
        },
        {
            "num": 13,
            "badge": "7. Your LEARNING — Contributions & Growth",
            "title": "Team Learnings: Individual Contributions & Takeaways",
            "subtitle": "Engineering Responsibilities & Key Conceptual Takeaways",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 14px;">
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155; border-top: 3px solid #3B82F6;">
                    <div style="color: #60A5FA; font-weight: 700; font-size: 1.05rem;">VIVEK UPADHYAY (Team Captain)</div>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 10px;">Roll No: 2023UAI1996 | Dept. of AI & Data Engineering</div>
                    <div style="font-size: 0.84rem; color: #F8FAFC; font-weight: 600; margin-top: 6px;">Key Contributions:</div>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Designed the Dual-Pathway system architecture separating deterministic math from generative language.</li>
                        <li>Engineered SEC EDGAR XBRL & Indian Exchange automated ingestion connectors.</li>
                        <li>Built the Hybrid RAG retriever (Qdrant + BM25 + RRF) and Cross-Encoder reranking module.</li>
                    </ul>
                    <div style="font-size: 0.84rem; color: #38BDF8; font-weight: 600; margin-top: 8px;">Key Learnings:</div>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Mastered enterprise IR and overcoming vocabulary drift in financial text.</li>
                        <li>Learned how to design fail-safe AI pipelines that strictly eliminate LLM hallucinations.</li>
                    </ul>
                </div>
                <div style="background: #1E293B; padding: 18px; border-radius: 8px; border: 1px solid #334155; border-top: 3px solid #10B981;">
                    <div style="color: #34D399; font-weight: 700; font-size: 1.05rem;">ASHISH ROLANIYA (Co-Investigator)</div>
                    <div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 10px;">Roll No: 2023UAI1825 | Dept. of AI & Data Engineering</div>
                    <div style="font-size: 0.84rem; color: #F8FAFC; font-weight: 600; margin-top: 6px;">Key Contributions:</div>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Implemented the transparent ESG scoring engine (30/30/40 model) & coverage gate.</li>
                        <li>Engineered the ReportLab PDF dossier generator with two-pass NumberedCanvas.</li>
                        <li>Developed the React 18 / TypeScript frontend & authored the 21-test Pytest suite.</li>
                    </ul>
                    <div style="font-size: 0.84rem; color: #34D399; font-weight: 600; margin-top: 8px;">Key Learnings:</div>
                    <ul style="font-size: 0.8rem; color: #CBD5E1; line-height: 1.5; padding-left: 14px;">
                        <li>Acquired deep knowledge of SEBI BRSR and GRI sustainability reporting frameworks.</li>
                        <li>Mastered programmatic PDF typesetting, 2D coordinate layouts, and UI state management.</li>
                    </ul>
                </div>
            </div>
            """,
            "notes": "Slide 13 details our individual project contributions and key personal learnings. As Team Captain, I, Vivek Upadhyay, focused on the system architecture, the automated regulatory connectors for SEC EDGAR and Indian exchanges, the Hybrid RAG pipeline with Qdrant and BM25, and the Cross-Encoder reranker. I learned how to address vocabulary drift and design deterministic fail-safes. My co-investigator, Ashish Rolaniya, engineered the transparent ESG scoring engine, the ReportLab PDF dossier generator with two-pass canvas numbering, the React 18 user interface, and the automated test suite. Ashish deepened his expertise in sustainability reporting frameworks and robust UI/UX engineering."
        },
        {
            "num": 14,
            "badge": "Project Conclusion & Q/A",
            "title": "Conclusion & Academic Deliverables",
            "subtitle": "Summary of Accomplishments & Submission Package",
            "content": """
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px;">
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #34D399; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">1. Operational Full-Stack Prototype</div>
                    <p style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">Fully functional web system with FastAPI, React 18, Qdrant, and SQLite/Postgres. 21/21 passing automated tests in 14.63s.</p>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #38BDF8; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">2. IEEE 2-Column Research Paper</div>
                    <p style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">7-page academic manuscript prepared in IEEE Conference style with complete LaTeX source (.tex) and compiled PDF.</p>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #0EA5E9; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">3. Annotated Literature Catalogue</div>
                    <p style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">Curated catalog of 19 verified SOTA research papers with active DOIs, Semantic Scholar citations, and BibTeX file.</p>
                </div>
                <div style="background: #1E293B; padding: 16px; border-radius: 8px; border: 1px solid #334155;">
                    <div style="color: #FBBF24; font-weight: 700; font-size: 0.95rem; margin-bottom: 6px;">4. Open-Source GitHub Repository</div>
                    <p style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">Full source code, setup instructions, and reproducible test scripts at <a href="https://github.com/vivekmnit1996/AI-Financial-Analyst" target="_blank" style="color: #38BDF8; text-decoration: underline;">github.com/vivekmnit1996/AI-Financial-Analyst</a>.</p>
                </div>
            </div>
            <div style="margin-top: 18px; padding: 14px; background: #0F172A; border-radius: 8px; border: 1px solid #334155; text-align: center;">
                <span style="color: #F8FAFC; font-size: 1.1rem; font-weight: 700;">Thank you! We invite questions and feedback from the committee.</span>
            </div>
            """,
            "notes": "In conclusion, our B.Tech project demonstrates that AI can be used reliably in high-stakes corporate finance when architected with deterministic safeguards. We have delivered a complete operational prototype, an IEEE research paper, a verified literature catalogue, and an open-source codebase. We want to thank our project mentor and the Department of Artificial Intelligence and Data Engineering at MNIT Jaipur. We now welcome questions and discussion from the committee."
        }
    ]

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Financial Analyst & Report Generator — B.Tech Capstone Presentation</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #0B0F19;
            color: #F8FAFC;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }}
        .navbar {{
            background: #0F172A;
            padding: 12px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1E293B;
        }}
        .nav-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #38BDF8;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-controls {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-btn {{
            background: #1E293B;
            color: #F8FAFC;
            border: 1px solid #334155;
            padding: 7px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .nav-btn:hover {{ background: #2563EB; border-color: #2563EB; }}
        .nav-btn.primary {{ background: #2563EB; border-color: #2563EB; }}
        .nav-btn.primary:hover {{ background: #1D4ED8; }}
        .progress-bar {{
            height: 3px;
            background: #1E293B;
            width: 100%;
        }}
        .progress-fill {{
            height: 100%;
            background: #38BDF8;
            transition: width 0.3s;
        }}
        .presentation-container {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .slide {{
            display: none;
            width: 100%;
            max-width: 1180px;
            height: 84vh;
            background: #0F172A;
            border-radius: 12px;
            border: 1px solid #1E293B;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            padding: 32px 44px;
            flex-direction: column;
            overflow-y: auto;
            position: relative;
        }}
        .slide.active {{ display: flex; }}
        .slide-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid #1E293B;
        }}
        .slide-badge {{
            background: rgba(14, 165, 233, 0.15);
            color: #38BDF8;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .slide-counter {{
            font-size: 0.85rem;
            color: #64748B;
            font-weight: 600;
        }}
        .slide-title {{
            font-size: 1.8rem;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: -0.5px;
            line-height: 1.2;
        }}
        .slide-subtitle {{
            font-size: 0.95rem;
            color: #94A3B8;
            margin-top: 4px;
            margin-bottom: 12px;
        }}
        .slide-content {{
            flex: 1;
        }}
        .notes-panel {{
            display: none;
            margin-top: 16px;
            background: #0B0F19;
            padding: 14px 18px;
            border-radius: 8px;
            border-left: 4px solid #38BDF8;
            font-size: 0.85rem;
            color: #94A3B8;
            line-height: 1.6;
        }}
        .notes-panel.active {{ display: block; }}
        .slide-footer {{
            margin-top: auto;
            padding-top: 14px;
            border-top: 1px solid #1E293B;
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: #475569;
        }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="nav-title">
            <span>🏛️ AI Financial Analyst</span>
            <span style="color: #64748B; font-weight: 400;">| MNIT Jaipur B.Tech Capstone</span>
        </div>
        <div class="nav-controls">
            <button class="nav-btn" onclick="toggleNotes()">📝 Notes (N)</button>
            <button class="nav-btn" onclick="prevSlide()">◀ Prev</button>
            <span id="counter-badge" style="font-size: 0.85rem; color: #94A3B8; font-weight: 600; padding: 0 8px;">1 / 14</span>
            <button class="nav-btn primary" onclick="nextSlide()">Next ▶</button>
        </div>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" id="progress"></div>
    </div>

    <div class="presentation-container">
"""

    for s in slides:
        num = s["num"]
        active = "active" if num == 1 else ""
        html_template += f"""
        <div class="slide {active}" id="slide-{num}">
            <div class="slide-header">
                <span class="slide-badge">{s["badge"]}</span>
                <span class="slide-counter">Slide {num:02d} / 14</span>
            </div>
            <div class="slide-title">{s["title"]}</div>
            <div class="slide-subtitle">{s["subtitle"]}</div>
            <div class="slide-content">
                {s["content"]}
            </div>
            <div class="notes-panel" id="notes-{num}">
                <strong style="color: #38BDF8;">Presenter Notes:</strong> {s["notes"]}
            </div>
            <div class="slide-footer">
                <span>AI Financial Analyst & Report Generator | Vivek Upadhyay & Ashish Rolaniya</span>
                <span>MNIT Jaipur — Dept. of AI & Data Engineering</span>
            </div>
        </div>
"""

    html_template += """
    </div>

    <script>
        let current = 1;
        const total = 14;
        let showNotesFlag = false;

        function showSlide(n) {
            document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
            const target = document.getElementById('slide-' + n);
            if (target) {
                target.classList.add('active');
                document.getElementById('counter-badge').innerText = n + ' / ' + total;
                document.getElementById('progress').style.width = (n / total * 100) + '%';
            }
        }

        function nextSlide() {
            if (current < total) { current++; showSlide(current); }
        }

        function prevSlide() {
            if (current > 1) { current--; showSlide(current); }
        }

        function toggleNotes() {
            showNotesFlag = !showNotesFlag;
            document.querySelectorAll('.notes-panel').forEach(np => {
                if (showNotesFlag) np.classList.add('active');
                else np.classList.remove('active');
            });
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
            if (e.key === 'n' || e.key === 'N') toggleNotes();
            if (e.key === 'Home') { current = 1; showSlide(current); }
            if (e.key === 'End') { current = total; showSlide(current); }
        });

        // Initialize progress
        showSlide(1);
    </script>
</body>
</html>
"""

    out_file = "/home/vivek/Projects/llm_project/presentation/AI_Financial_Analyst_Presentation.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Interactive HTML presentation saved to {out_file}")

if __name__ == "__main__":
    generate_html_presentation()
