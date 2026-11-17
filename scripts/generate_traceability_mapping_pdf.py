import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.rag.sample_document_generator import NumberedCanvas

def generate_traceability_pdf():
    out_dir = Path("AI_Financial_Analyst_Academic_Submission")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "Research_to_Implementation_Mapping.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    doc_title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    doc_sub_style = ParagraphStyle(
        "DocSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )
    cat_header_style = ParagraphStyle(
        "CatHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=4
    )
    comp_header_style = ParagraphStyle(
        "CompHeader",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=6,
        spaceAfter=2
    )
    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=4
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=10.5,
        textColor=colors.white
    )

    story = []

    # Title & Header
    story.append(Paragraph("AI FINANCIAL ANALYST & REPORT GENERATOR", doc_title_style))
    story.append(Paragraph(
        "<b>RESEARCH-TO-IMPLEMENTATION TRACEABILITY MATRIX & ARCHITECTURAL MAPPING</b><br/>"
        "<b>Academic Context:</b> B.Tech Major Project in Artificial Intelligence & Data Engineering<br/>"
        "<b>Student Investigators:</b> Vivek Upadhyay (Team Captain — Roll: 2023UAI1996) &bull; Ashish Rolaniya (Roll: 2023UAI1825)<br/>"
        "<b>Purpose:</b> Explicitly delineates the formal relationship between every system module and its supporting academic literature. "
        "Strictly categorizes whether each paper: (1) Provides Theoretical Foundation, (2) Is Directly Implemented, (3) Methodologically Inspired the Component, or (4) Serves as an Evaluation Benchmark.",
        doc_sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=0, spaceAfter=8))

    # Modules Breakdown
    modules = [
        {
            "id": "MOD-01",
            "name": "Deterministic Financial Ratio & Growth Engine",
            "files": "backend/app/engine/financial_calculator.py",
            "papers": [
                ("BloombergGPT (Wu et al., 2023)", "Theoretical Foundation & Architectural Motivation",
                 "Demonstrates that 50B-parameter LLMs suffer from severe arithmetic inaccuracies, rounding errors, and hallucinated financial figures when performing calculations directly. Proves that important corporate financial ratios (ROE, ROA, Margins, Growth) MUST be computed deterministically."),
                ("FinanceBench (Islam et al., 2023)", "Evaluation Benchmark Motivation",
                 "Documents an 81% failure rate for standalone commercial LLMs on complex numerical ratio questions in 10-K filings. Confirms the architectural necessity of separating calculation logic from text synthesis.")
            ],
            "implementation": "Fully implemented in Python/Pandas. Computes 14 distinct ratios (Gross/Operating/Net Margins, ROE, ROA, Debt-to-Equity, Current Ratio, Cash Flow Conversion) with explicit zero-division traps, negative equity handlers, and trend momentum analysis."
        },
        {
            "id": "MOD-02",
            "name": "Automated Multi-Source Regulatory Ingestion",
            "files": "backend/app/collectors/sec_edgar_connector.py, exchange_connector.py, collection_orchestrator.py",
            "papers": [
                ("FinGPT (Yang et al., 2023)", "Architecture & Pipeline Inspiration",
                 "Introduces open-source financial data collection workflows for SEC EDGAR and market disclosures, demonstrating standard extraction schemas for automated ingestion pipelines.")
            ],
            "implementation": "Directly implemented with live connectors to SEC EDGAR (official XBRL Company Facts JSON API with compliant User-Agent headers) and Indian Stock Exchanges (BSE/NSE audited filings & BRSR disclosures), orchestrated with background asynchronous jobs."
        },
        {
            "id": "MOD-03",
            "name": "Accounting Data Validation & Balance Sheet Identity Reconciliation",
            "files": "backend/app/collectors/data_validator.py",
            "papers": [
                ("FinQA (Chen et al., 2021)", "Foundational Motivation",
                 "Identifies that financial datasets frequently contain reporting inconsistencies, unit ambiguities (thousands vs. millions vs. crores), and missing fields that disrupt downstream reasoning.")
            ],
            "implementation": "Directly implemented deterministic validation engine. Audits accounting invariants: Assets = Liabilities + Equity (flagging discrepancies > 2%), verifies unit/currency normalization, checks period continuity, and marks anomalous spikes (> 100% variance)."
        },
        {
            "id": "MOD-04",
            "name": "Structure-Aware Document Ingestion & Section Parsing",
            "files": "backend/app/rag/document_parser.py, chunker.py",
            "papers": [
                ("LayoutLM (Xu et al., 2020)", "Methodological Inspiration",
                 "Establishes that physical layout, bounding box coordinates, and structural headers carry vital semantic signal in multi-column business reports."),
                ("TAT-QA (Zhu et al., 2021)", "Methodological Inspiration",
                 "Shows that mixed tabular-textual documents require preserving table grid structure rather than flattening into continuous sentences."),
                ("DocBank (Li et al., 2020)", "Methodological Inspiration",
                 "Demonstrates token-level spatial layout benefits for complex corporate filings.")
            ],
            "implementation": "Implemented via PyMuPDF (fitz) and pdfplumber. Extracts page-anchored text and structured tables, applies sliding-window chunking (800 chars / 150 overlap), preserves 1-indexed page coordinates, and annotates chunk metadata with fiscal year and detected section."
        },
        {
            "id": "MOD-05",
            "name": "Dense Vector Embedding & Persistent Vector Index",
            "files": "backend/app/rag/vector_store.py",
            "papers": [
                ("Sentence-BERT (Reimers & Gurevych, 2019)", "Theoretical Foundation",
                 "Forms the mathematical Siamese bi-encoder foundation for generating dense semantic vector embeddings compared via cosine similarity."),
                ("BGE: C-Pack (Xiao et al., 2023)", "Directly Implemented Model",
                 "Presents BAAI General Embeddings trained on multi-task contrastive pairs. Our engine directly instantiates BAAI/bge-small-en-v1.5 (384-dimensional dense vectors) via FastEmbed ONNX runtime."),
                ("DPR (Karpukhin et al., 2020)", "Theoretical Foundation",
                 "Validates dual-encoder dense retrieval for open-domain questions against traditional lexical lookups.")
            ],
            "implementation": "Implemented with Qdrant vector store (`financial_chunks` collection) using cosine distance metric, persistent disk storage with automatic in-memory fallback for test concurrency."
        },
        {
            "id": "MOD-06",
            "name": "Sparse Lexical Retrieval Engine (Okapi BM25)",
            "files": "backend/app/rag/bm25_search.py",
            "papers": [
                ("The Probabilistic Relevance Framework: BM25 and Beyond (Robertson & Zaragoza, 2009)", "Directly Implemented Foundation",
                 "Establishes non-linear term saturation and inverse document frequency (IDF) for exact lexical matching.")
            ],
            "implementation": "Directly implemented using rank_bm25. Crucial for exact regulatory identifiers ('Ind AS 116', 'Section 135', 'Scope 2 GHG', 'LTIR', 'EBITDA') where dense embeddings produce vector drift."
        },
        {
            "id": "MOD-07",
            "name": "Hybrid Retrieval & Reciprocal Rank Fusion (RRF)",
            "files": "backend/app/rag/hybrid_retriever.py",
            "papers": [
                ("Reciprocal Rank Fusion (Cormack et al., 2009)", "Directly Implemented Algorithm",
                 "Proves that RRF(d) = sum(1 / (k + rank(d))) with k=60 outperforms score normalization and Condorcet voting across heterogeneous ranked lists."),
                ("HyDE (Gao et al., 2023)", "Technique Inspiration",
                 "Informs query decomposition to expand short user queries into disclosures-matching search representations.")
            ],
            "implementation": "Directly implemented in hybrid_retriever.py with settings.RRF_K = 60. Executes parallel queries against Qdrant dense index and BM25 sparse index, combines candidate rankings, and selects the top-K merged candidates."
        },
        {
            "id": "MOD-08",
            "name": "Cross-Encoder Reranking & Section Optimization",
            "files": "backend/app/rag/reranker.py",
            "papers": [
                ("Passage Re-ranking with BERT (Nogueira & Cho, 2019)", "Directly Implemented Architecture",
                 "Demonstrates cross-encoder joint attention outperforming dual-encoder bi-encoders for scoring candidate relevance.")
            ],
            "implementation": "Directly implemented using BAAI/bge-reranker-base cross-encoder. Computes joint token-level query-document cross-attention scores and applies a contextual section bonus for MD&A, Risk Factors, and ESG disclosures."
        },
        {
            "id": "MOD-09",
            "name": "Evidence-Grounded Synthesis & Query Routing",
            "files": "backend/app/rag/llm_service.py",
            "papers": [
                ("RAG (Lewis et al., 2020)", "Foundational Architecture",
                 "The seminal architectural framework combining parametric LLM reasoning with non-parametric retrieved document chunks."),
                ("FinBERT (Araci, 2019)", "Domain Foundation",
                 "Validates financial-specific sentiment and linguistic patterns in annual report MD&A narratives.")
            ],
            "implementation": "Implemented with query intent classifier, multi-provider abstraction (OpenAI, Gemini, Local ONNX / Deterministic Fallback), and mandatory citation formatting: [Document Title, Page X, Section]."
        },
        {
            "id": "MOD-10",
            "name": "Transparent ESG Indicator Decomposition & Scoring",
            "files": "backend/app/engine/esg_scorer.py",
            "papers": [
                ("Aggregate Confusion: ESG Rating Divergence (Berg et al., 2022)", "Theoretical Foundation & Problem Formulation",
                 "MIT Sloan benchmark showing commercial ratings diverge severely (r=0.54) due to black-box weighting. Calls for transparent indicator-level scoring."),
                ("ClimateBERT (Webersinke et al., 2021)", "Methodological Inspiration",
                 "Distinguishes between verifiable quantitative indicators (GHG Scope 1/2) and promotional text in BRSR/TCFD disclosures.")
            ],
            "implementation": "Fully implemented rule-based transparent engine. Decomposes ESG into E (30%), S (30%), G (40%). Requires minimum 30% disclosure threshold; missing indicators are never penalized as zero. Publishes full mathematical breakdown."
        },
        {
            "id": "MOD-11",
            "name": "Multi-Format Institutional Report Generation",
            "files": "backend/app/report_generator/pdf_generator.py, html_generator.py",
            "papers": [
                ("FinQA & TAT-QA (Chen et al., 2021; Zhu et al., 2021)", "Presentation Motivation",
                 "Emphasizes the necessity of presenting side-by-side numerical ratio tables, trend visualizations, and cited textual justifications.")
            ],
            "implementation": "Implemented with ReportLab (publication PDF with running NumberedCanvas, charts, and ratio cards) and standalone HTML dossiers with responsive CSS styling."
        }
    ]

    for m in modules:
        entry = [
            Paragraph(f"<b>[{m['id']}] {m['name']}</b>", comp_header_style),
            Paragraph(f"<b>System Files:</b> {m['files']}", meta_style)
        ]
        for p_title, p_role, p_desc in m["papers"]:
            entry.append(Paragraph(f"&bull; <b>{p_title}</b> &mdash; <i>[{p_role}]</i>: {p_desc}", body_style))
        entry.append(Paragraph(f"<b>Implementation Status:</b> {m['implementation']}", ParagraphStyle("Imp", parent=body_style, fontName="Helvetica-Bold", textColor=colors.HexColor("#047857"))))
        entry.append(Spacer(1, 4))
        story.append(KeepTogether(entry))

    # Comprehensive Matrix Table
    story.append(PageBreak())
    story.append(Paragraph("SUMMARY TRACEABILITY MATRIX", cat_header_style))
    story.append(Paragraph("Systematic taxonomy of research literature relationships across all project components.", doc_sub_style))

    table_data = [
        [
            Paragraph("Module ID & Component", table_header),
            Paragraph("Supporting Literature", table_header),
            Paragraph("Formal Relationship Role", table_header),
            Paragraph("Technical Justification", table_header)
        ]
    ]

    matrix_rows = [
        ("MOD-01: Financial Calculator", "BloombergGPT (Wu '23), FinanceBench (Islam '23)", "Theoretical Foundation & Benchmark Motivation", "LLM arithmetic hallucinations make deterministic calculation mandatory for ratios."),
        ("MOD-02: Data Acquisition", "FinGPT (Yang '23)", "Architecture & Pipeline Inspiration", "Automated regulatory ingestion workflows for SEC EDGAR and stock exchange filings."),
        ("MOD-03: Accounting Validator", "FinQA (Chen '21)", "Foundational Motivation", "Identifies unit discrepancies and enforces Balance Sheet identity reconciliation."),
        ("MOD-04: Document Ingestion", "LayoutLM (Xu '20), TAT-QA (Zhu '21), DocBank (Li '20)", "Methodological Inspiration", "Preserves table grids, spatial headers, and page coordinates in multi-column PDFs."),
        ("MOD-05: Dense Vector Store", "Sentence-BERT (Reimers '19), BGE (Xiao '23), DPR (Karpukhin '20)", "Directly Implemented Model & Theory", "BAAI/bge-small-en-v1.5 dense vectors (384-d) indexed in Qdrant with cosine metric."),
        ("MOD-06: Sparse BM25 Search", "Robertson & Zaragoza (2009)", "Directly Implemented Algorithm", "Okapi BM25 term frequency saturation for exact financial ticker and metric lookups."),
        ("MOD-07: Hybrid Fusion", "Reciprocal Rank Fusion (Cormack '09), HyDE (Gao '23)", "Directly Implemented Algorithm", "RRF (k=60) fuses dense and sparse rankings without uncalibrated score normalization."),
        ("MOD-08: Reranker", "Passage Re-ranking with BERT (Nogueira '19)", "Directly Implemented Architecture", "Cross-encoder joint query-document cross-attention using bge-reranker-base."),
        ("MOD-09: LLM Reasoning", "RAG (Lewis '20), FinBERT (Araci '19)", "Foundational Architecture", "Retrieved context grounding, query routing, and verified page-level citations."),
        ("MOD-10: ESG Scorer", "Aggregate Confusion (Berg '22), ClimateBERT (Webersinke '21)", "Theoretical Foundation & Problem Formulation", "Eliminates black-box divergence by publishing open indicator weights (30/30/40)."),
        ("MOD-11: Report Generation", "FinQA (Chen '21), TAT-QA (Zhu '21)", "Presentation Motivation", "Generates dual-modality institutional PDF dossiers combining tables and citations.")
    ]

    for mid, lit, role, just in matrix_rows:
        table_data.append([
            Paragraph(f"<b>{mid}</b>", table_cell),
            Paragraph(lit, table_cell),
            Paragraph(f"<i>{role}</i>", table_cell),
            Paragraph(just, table_cell)
        ])

    table = Table(table_data, colWidths=[120, 115, 110, 185])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {pdf_path}")
    return str(pdf_path)

if __name__ == "__main__":
    generate_traceability_pdf()
