import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Institutional Color Palette
    C_NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
    C_NAVY_CARD = RGBColor(30, 41, 59)      # #1E293B
    C_BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB
    C_CYAN_ACCENT = RGBColor(14, 165, 233)  # #0EA5E9
    C_EMERALD = RGBColor(16, 185, 129)      # #10B981
    C_WHITE = RGBColor(255, 255, 255)
    C_LIGHT_GRAY = RGBColor(241, 245, 249)  # #F1F5F9
    C_TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
    C_TEXT_DARK = RGBColor(15, 23, 42)
    C_BORDER = RGBColor(226, 232, 240)      # #E2E8F0
    C_GOLD = RGBColor(245, 158, 11)         # #F59E0B

    def add_header(slide, title, category, slide_num):
        # Top banner background
        top_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(1.15))
        top_box.fill.solid()
        top_box.fill.fore_color.rgb = C_NAVY_DARK
        top_box.line.color.rgb = C_NAVY_DARK

        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(6.0), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(10.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Slide Number Badge
        num_box = slide.shapes.add_textbox(Inches(12.0), Inches(0.35), Inches(0.8), Inches(0.4))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.text = f"{slide_num:02d} / 14"
        p_num.font.size = Pt(12)
        p_num.font.bold = True
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.color.rgb = C_TEXT_MUTED

    def add_footer(slide):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = "AI Financial Analyst & Report Generator | MNIT Jaipur B.Tech Project | Dual-Pathway Deterministic Architecture & Hybrid RAG"
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(100, 116, 139)

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY_DARK
    bg1.line.color.rgb = C_NAVY_DARK

    # Accent bar
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = C_CYAN_ACCENT
    bar1.line.color.rgb = C_CYAN_ACCENT

    # Title box
    tbox1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "B.TECH PROJECT CAPSTONE PRESENTATION | TRL 5/6 OPERATIONAL PROTOTYPE"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = C_CYAN_ACCENT

    p_main = tf1.add_paragraph()
    p_main.text = "AI Financial Analyst &\nReport Generator"
    p_main.font.size = Pt(36)
    p_main.font.bold = True
    p_main.font.color.rgb = C_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = "Dual-Pathway Deterministic Arithmetic, Hybrid RAG with Verifiable Citations, & Transparent ESG Scoring"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = C_LIGHT_GRAY

    # Metadata cards
    # Card 1: Team
    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.8), Inches(5.2), Inches(2.2))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_NAVY_CARD
    c1.line.color.rgb = RGBColor(51, 65, 85)
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "PROJECT INVESTIGATORS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf_c1.add_paragraph()
    p.text = "• Vivek Upadhyay (Team Captain) — Roll No: 2023UAI1996\n• Ashish Rolaniya (Co-Investigator) — Roll No: 2023UAI1825"
    p.font.size = Pt(13)
    p.font.color.rgb = C_WHITE

    p = tf_c1.add_paragraph()
    p.text = "Dept. of Artificial Intelligence & Data Engineering\nMalaviya National Institute of Technology (MNIT) Jaipur"
    p.font.size = Pt(11)
    p.font.color.rgb = C_TEXT_MUTED

    # Card 2: System Spec & Code
    c2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.8), Inches(5.4), Inches(2.2))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_NAVY_CARD
    c2.line.color.rgb = RGBColor(51, 65, 85)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "KEY SPECIFICATIONS & REPOSITORY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf_c2.add_paragraph()
    p.text = "• Stack: FastAPI, React 18, Qdrant, PyMuPDF, ReportLab\n• Test Suite: 21 Passed Pytest Automated Suites (100% Pass)\n• Open-Source GitHub Repository:"
    p.font.size = Pt(12)
    p.font.color.rgb = C_WHITE

    p = tf_c2.add_paragraph()
    p.text = "https://github.com/vivekmnit1996/AI-Financial-Analyst"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    set_notes(s1, "Good morning esteemed project mentor and evaluation committee. Today, my teammate Ashish Rolaniya and I, Vivek Upadhyay, present our B.Tech Capstone project: 'AI Financial Analyst and Report Generator'. Our goal was to build a production-grade, institutional equity research platform that bridges the fundamental flaw of generative AI in corporate finance—hallucinated arithmetic—by enforcing a strict dual-pathway architecture, Hybrid RAG with exact page provenance, and transparent ESG scoring.")

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement: The Arithmetic & Provenance Bottleneck", "1. Problem Statement & Motivation", 2)
    add_footer(s2)

    # 3 Column Cards
    col_w = Inches(3.7)
    cards_data = [
        ("1. Disclosures Overload", C_BLUE_ACCENT, [
            "Massive Document Volume: Corporate filings (SEC 10-K, 10-Q, Indian Annual Reports, SEBI BRSR) exceed 300+ pages each.",
            "Manual Time Drain: Financial analysts dedicate up to 70% of analytical hours to manual table lookup and cross-referencing.",
            "Severe Information Asymmetry: Retail and institutional investors struggle to rapidly cross-audit multi-year statements."
        ]),
        ("2. LLM Hallucinations", RGBColor(220, 38, 38), [
            "Arithmetic Inaccuracy: Commercial autoregressive LLMs (GPT-4, Gemini) fail on accounting algebra and invent margins.",
            "Empirical Evidence: BloombergGPT (2023) and FinanceBench (2023) show commercial LLMs suffer high error rates on ratios.",
            "Absence of Provenance: Standard LLMs produce plausible-sounding narratives without auditable page-level citations."
        ]),
        ("3. ESG Greenwashing", C_GOLD, [
            "Divergent Black-Box Scores: Commercial ESG ratings (MSCI, Sustainalytics) exhibit low correlation (r ≈ 0.54, MIT Sloan).",
            "Lack of Transparency: Proprietary imputation penalizes unrecorded disclosures as zero without explaining assumptions.",
            "Regulatory Mandates: SEBI BRSR and EU CSRD demand verifiable, indicator-level audit trails rather than opaque scores."
        ])
    ]

    for i, (head, col, bullets) in enumerate(cards_data):
        cx = Inches(0.8 + i * 4.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.5), col_w, Inches(5.2))
        card.fill.solid()
        card.fill.fore_color.rgb = C_LIGHT_GRAY
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = head
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = col

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_before = Pt(8)

    set_notes(s2, "Slide 2 outlines the real-world motivation. Modern corporate filings are enormous—often 300 to 500 pages per company per year. Analysts spend 70% of their working hours cross-referencing footnotes. While people turn to LLMs like ChatGPT or Claude, they fail in two fatal ways: first, autoregressive next-token prediction cannot do deterministic financial math; second, they cannot cite exact audited page numbers. In addition, existing ESG scores suffer from what MIT Sloan termed 'Aggregate Confusion', where commercial agencies correlate at only 0.54. Our project directly solves all three problems.")

    # =========================================================================
    # SLIDE 3: TECHNOLOGY READINESS LEVEL (TRL) & SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Technology Readiness Level (TRL 5/6) & System Scope", "1. Problem Statement — TRL Level & Deployment", 3)
    add_footer(s3)

    # Left: TRL Ladder
    trl_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    trl_card.fill.solid()
    trl_card.fill.fore_color.rgb = C_LIGHT_GRAY
    trl_card.line.color.rgb = C_BORDER
    tf_trl = trl_card.text_frame
    tf_trl.word_wrap = True
    p = tf_trl.paragraphs[0]
    p.text = "SYSTEM TRL STATUS: TRL 5 / 6"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT

    trl_levels = [
        ("TRL 3: Analytical Proof of Concept", "Formulated dual-pathway mathematical decoupling of deterministic math and generative language.", RGBColor(100, 116, 139)),
        ("TRL 4: Component Validation in Lab", "Validated Python/Pandas financial ratio engine, PyMuPDF parser, Qdrant BGE-small embeddings, and BM25 index.", RGBColor(71, 85, 105)),
        ("TRL 5: System Integrated in Relevant Env", "Integrated live SEC EDGAR XBRL parser (10,400+ companies) & Indian Exchange (NSE/BSE) feeds with balance sheet validation.", C_BLUE_ACCENT),
        ("TRL 6: Operational Prototype Demonstrated", "Full-stack application running live with FastAPI, React 18 dashboard, Hybrid RAG chat with page citations, and ReportLab PDF generator.", C_EMERALD)
    ]

    for title, desc, color in trl_levels:
        p_t = tf_trl.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = color
        p_t.space_before = Pt(8)

        p_d = tf_trl.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    # Right: Operational Scope & Deployment Environment
    scope_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    scope_card.fill.solid()
    scope_card.fill.fore_color.rgb = C_LIGHT_GRAY
    scope_card.line.color.rgb = C_BORDER
    tf_scope = scope_card.text_frame
    tf_scope.word_wrap = True

    p = tf_scope.paragraphs[0]
    p.text = "OPERATIONAL TARGET ENVIRONMENT & METRICS"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_DARK

    items = [
        ("Target End-Users", "Equity research analysts, compliance officers, audit committees, and academic finance researchers."),
        ("Deployment Setup", "Deployable via Docker Compose across on-premise secure servers or cloud containers without proprietary cloud dependencies."),
        ("Hardware Footprint", "Runs seamlessly on commodity CPU hardware (sub-second query response; no $10k GPU required)."),
        ("Compliance & Fair Access", "Adheres to SEC EDGAR Fair Access policy with declared User-Agent; zero unauthorized scraping."),
        ("Reproducibility", "100% deterministic arithmetic testable via 21 automated pytest integration scripts.")
    ]

    for label, val in items:
        p_l = tf_scope.add_paragraph()
        p_l.text = f"• {label}: "
        p_l.font.size = Pt(11)
        p_l.font.bold = True
        p_l.font.color.rgb = C_BLUE_ACCENT
        p_l.space_before = Pt(8)
        run = p_l.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = C_TEXT_DARK

    set_notes(s3, "On Slide 3, we evaluate our system against standard NASA and DoD Technology Readiness Level criteria. Many academic AI projects stop at TRL 3 or 4—a Jupyter notebook showing toy results. Our project has achieved TRL 5 and TRL 6: an operational full-stack prototype validated on real, live corporate filings from the US SEC and Indian NSE/BSE. It runs in Docker, adheres to SEC Fair Access guidelines, and executes in real-time on commodity CPUs.")

    # =========================================================================
    # SLIDE 4: LITERATURE SURVEY & STATE OF THE ART (SOTA)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Literature Survey: State of the Art (SOTA) Benchmarks", "3. Literature Survey & SOTA Foundations", 4)
    add_footer(s4)

    # Table of papers
    rows, cols = 5, 4
    left = Inches(0.8)
    top = Inches(1.5)
    width = Inches(11.733)
    height = Inches(5.2)

    table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.2)
    table.columns[2].width = Inches(4.3)
    table.columns[3].width = Inches(2.033)

    headers = ["Domain / Benchmark", "Key SOTA Publication", "Core Contribution / Finding", "Limitation Addressed in Project"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    sota_data = [
        ("Financial QA & Reasoning", "FinQA (Chen et al., EMNLP 2021) &\nFinanceBench (Islam et al., 2023)", "First dedicated benchmarks testing LLM numerical reasoning over financial tables & 10-K reports.", "Showed that commercial LLMs hallucinate calculations; motivated our 100% deterministic math engine."),
        ("Retrieval-Augmented Generation", "RAG (Lewis et al., NeurIPS 2020) &\nDPR (Karpukhin et al., EMNLP 2020)", "Established parametric + non-parametric memory for open-domain question answering.", "Standard DPR fails on financial jargon; addressed by combining sparse BM25 + dense BGE."),
        ("Rank Fusion & Reranking", "Reciprocal Rank Fusion (Cormack, SIGIR '09) &\nCross-Encoder (Nogueira & Cho, 2019)", "RRF merges disparate rank lists (k=60); Cross-encoders compute full query-document cross-attention.", "Implemented RRF + Cross-Encoder to achieve +25.1% MRR boost over single-modality dense retrieval."),
        ("ESG Measurement & Ratings", "Aggregate Confusion: Divergence of ESG Ratings\n(Berg et al., Review of Finance 2022)", "Proved top ESG rating agencies correlate at only r ≈ 0.54 due to measurement & weighting divergence.", "Overcame black-box divergence by designing a fully transparent 30/30/40 indicator model.")
    ]

    for i, row in enumerate(sota_data):
        for j, val in enumerate(row):
            cell = table.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_LIGHT_GRAY if i % 2 == 0 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = C_TEXT_DARK
            if j == 0:
                p.font.bold = True

    set_notes(s4, "Slide 4 presents our literature survey of State-of-the-Art foundations. We surveyed 19 peer-reviewed papers across 4 pillars. First, FinQA and FinanceBench proved that pure LLMs are dangerous for finance because they guess mathematical numbers. Second, Lewis et al.'s original RAG paper introduced retrieval-augmented generation. Third, Cormack et al. and Nogueira & Cho established Reciprocal Rank Fusion and Cross-Encoder reranking. Finally, the seminal MIT Sloan paper by Berg et al. demonstrated that commercial ESG ratings diverge sharply due to opaque proprietary models.")

    # =========================================================================
    # SLIDE 5: RESEARCH GAPS IDENTIFIED & BASE PAPERS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Research Gaps Identified & Base Paper Traceability", "3. Gaps Identified & Base Papers", 5)
    add_footer(s5)

    gaps = [
        ("GAP 1: Arithmetic Inaccuracy in Generative LLMs", "Base Papers: FinanceBench (Islam et al., 2023) | FinQA (Chen et al., EMNLP 2021)", [
            "Identified Gap: Autoregressive language models attempt arithmetic inside token embeddings, resulting in rounding errors, hallucinated ratios, and sign errors in balance sheets.",
            "Our Architectural Solution: Decouple math completely. Formulated Pathway A: a 100% deterministic Python/Pandas numerical engine with division-by-zero traps."
        ]),
        ("GAP 2: Financial Vocabulary Mismatch in Pure Dense Search", "Base Papers: BGE Embeddings (Xiao et al., 2023) | Okapi BM25 (Robertson & Zaragoza, 2009)", [
            "Identified Gap: Bi-encoder dense vectors struggle with exact regulatory terminology, accounting standard codes (e.g., 'Ind AS 116'), ticker symbols, and specific numerical keys.",
            "Our Architectural Solution: Implemented Hybrid Retrieval (Dense Qdrant + Sparse BM25 fused via RRF k=60) followed by Cross-Encoder neural reranking."
        ]),
        ("GAP 3: Missing Provenance & Black-Box Qualitative Assertions", "Base Papers: RAG (Lewis et al., NeurIPS 2020) | Dense Passage Retrieval (Karpukhin et al., 2020)", [
            "Identified Gap: Existing financial AI tools generate claims without auditable page provenance, rendering them inadmissible for institutional regulatory compliance.",
            "Our Architectural Solution: Spatial coordinate PDF parsing with PyMuPDF; every claim is strictly bound to [Document Title, Page X, Section Y] citation badges."
        ]),
        ("GAP 4: Opaque & Speculative ESG Scoring Methodologies", "Base Papers: Aggregate Confusion (Berg et al., Review of Finance 2022)", [
            "Identified Gap: Commercial ESG providers fabricate proxy numbers for missing disclosures or assign arbitrary zero scores, obscuring real corporate sustainability.",
            "Our Architectural Solution: Transparent 30/30/40 linear model with non-disclosure zero-penalty omission and a mandatory 30% reporting coverage gate."
        ])
    ]

    card_h = Inches(1.22)
    for i, (g_title, g_base, g_bullets) in enumerate(gaps):
        gy = Inches(1.45 + i * 1.35)
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), gy, Inches(11.733), card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = C_LIGHT_GRAY
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = g_title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK

        p_b = tf.add_paragraph()
        p_b.text = g_base
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_BLUE_ACCENT

        for b in g_bullets:
            p_desc = tf.add_paragraph()
            p_desc.text = "• " + b
            p_desc.font.size = Pt(10)
            p_desc.font.color.rgb = C_TEXT_DARK

    set_notes(s5, "Slide 5 establishes the precise research gaps we identified in prior literature and maps them directly to our base papers and novel solutions. Gap 1 is arithmetic inaccuracy, identified by FinanceBench—solved by our deterministic numerical engine. Gap 2 is vocabulary mismatch in pure dense embeddings—solved by our Hybrid RRF plus Cross-Encoder reranking. Gap 3 is black-box assertions lacking provenance—solved by our structure-aware page coordinate parser. Gap 4 is opaque ESG ratings—solved by our transparent 30/30/40 indicator scoring with a coverage withholding gate.")

    # =========================================================================
    # SLIDE 6: PROPOSED METHODOLOGY: DUAL-PATHWAY ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Proposed Methodology: Dual-Pathway System Architecture", "4. Proposed Methodology — Architecture", 6)
    add_footer(s6)

    # Core philosophy banner
    ph_banner = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.5))
    ph_banner.fill.solid()
    ph_banner.fill.fore_color.rgb = C_NAVY_DARK
    tf_ph = ph_banner.text_frame
    p_ph = tf_ph.paragraphs[0]
    p_ph.text = "CORE PHILOSOPHY: STRICT SEPARATION OF DETERMINISTIC ARITHMETIC FROM GENERATIVE REASONING"
    p_ph.font.size = Pt(11)
    p_ph.font.bold = True
    p_ph.font.color.rgb = C_CYAN_ACCENT
    p_ph.alignment = PP_ALIGN.CENTER

    # 3 Parallel Pipeline Cards
    pipe_w = Inches(3.7)
    pipes = [
        ("PATHWAY A: DETERMINISTIC FINANCE", C_BLUE_ACCENT, [
            "Data Input: Audited Balance Sheets & P&L statements (XBRL / Exchange feeds).",
            "Computation: Handled strictly in Python / Pandas (14 standard financial ratios).",
            "Zero-Hallucination: Operating Margin, ROE, ROA, D/E, FCF computed vectorially.",
            "Integrity Guards: Balance sheet reconciliation identity (Assets ≈ Liab + Equity)."
        ]),
        ("PATHWAY B: HYBRID RAG INTELLIGENCE", C_CYAN_ACCENT, [
            "Document Ingestion: PyMuPDF parses corporate 10-K & Annual Report PDFs.",
            "Chunking: Structure-aware sliding window (300-400 words) with metadata.",
            "Retrieval: Parallel Dense (Qdrant BGE-small) + Sparse (Okapi BM25).",
            "Fusion & Rerank: Reciprocal Rank Fusion (k=60) + Cross-Encoder reranking."
        ]),
        ("PATHWAY C: TRANSPARENT ESG ENGINE", C_EMERALD, [
            "Pillar Weights: Environmental (30%), Social (30%), Governance (40%).",
            "Disclosure Rules: Evaluates 16 core quantitative indicators from SEBI BRSR.",
            "Zero-Penalty Rule: Undisclosed metrics omitted from averages (not set to zero).",
            "Coverage Gate: Withholds composite rating if disclosure coverage is < 30%."
        ])
    ]

    for i, (p_title, p_col, p_points) in enumerate(pipes):
        px = Inches(0.8 + i * 4.0)
        p_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, Inches(2.1), pipe_w, Inches(3.3))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = C_LIGHT_GRAY
        p_card.line.color.rgb = C_BORDER
        tf = p_card.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = p_title
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = p_col

        for pt in p_points:
            p_pt = tf.add_paragraph()
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(10.5)
            p_pt.font.color.rgb = C_TEXT_DARK
            p_pt.space_before = Pt(6)

    # Synthesis Bottom Card
    synth_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.2))
    synth_card.fill.solid()
    synth_card.fill.fore_color.rgb = C_NAVY_CARD
    synth_card.line.color.rgb = C_CYAN_ACCENT
    tf_syn = synth_card.text_frame
    tf_syn.word_wrap = True

    p = tf_syn.paragraphs[0]
    p.text = "EVIDENCE REASONING SYNTHESIS & INSTITUTIONAL REPORT LAB OUTPUT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf_syn.add_paragraph()
    p.text = "Pre-calculated financial metrics + top-5 reranked evidence passages are passed to the Context-Constrained Synthesis Engine.\nOutputs verifiable executive answers with clickable [Page X, Section Y] citation badges and downloads audit-grade PDF & HTML dossiers."
    p.font.size = Pt(10)
    p.font.color.rgb = C_TEXT_MUTED

    set_notes(s6, "Slide 6 is the heart of our technical methodology: the Dual-Pathway Architecture. Rather than passing raw financial tables to an LLM and hoping it does arithmetic correctly, our architecture splits execution into three parallel, deterministic pipelines. Pathway A computes all 14 financial ratios in Python/Pandas. Pathway B performs Hybrid RAG document retrieval using dense vectors and sparse BM25, merged via RRF and reranked via a cross-encoder. Pathway C calculates transparent ESG scores. All three feed into our synthesis engine, guaranteeing 100% calculation accuracy with full source provenance.")

    # =========================================================================
    # SLIDE 7: PROPOSED METHODOLOGY: DATASET & INGESTION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Proposed Methodology: Datasets & Regulatory Ingestion", "4. Proposed Methodology — Data Pipeline", 7)
    add_footer(s7)

    # 2 Column Cards
    col_w7 = Inches(5.7)

    # Left: Data Sources
    d_card1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w7, Inches(5.2))
    d_card1.fill.solid()
    d_card1.fill.fore_color.rgb = C_LIGHT_GRAY
    d_card1.line.color.rgb = C_BORDER
    tf1 = d_card1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "REGULATORY DATA SOURCES & REPOSITORIES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT

    sources = [
        ("SEC EDGAR XBRL Data Feeds", "Connects to official data.sec.gov APIs with SEC-compliant User-Agent. Ingests Company Facts across both US-GAAP (10-K/10-Q) and IFRS-FULL (Form 20-F) for 10,400+ publicly traded corporations."),
        ("Indian Stock Exchange Filings (NSE / BSE)", "Ingests verified annual audited statements and SEBI BRSR sustainability disclosures for benchmark Indian corporations (TCS, Reliance, Infosys, HDFC Bank, Tata Motors)."),
        ("Dynamic Live Discovery via Yahoo Finance", "Integrated query2.finance.yahoo.com API for real-time global ticker lookup and corporate profile resolution with automated CIK mapping.")
    ]

    for title, desc in sources:
        p_t = tf1.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK
        p_t.space_before = Pt(8)
        p_d = tf1.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    # Right: Preprocessing & Validation
    d_card2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), col_w7, Inches(5.2))
    d_card2.fill.solid()
    d_card2.fill.fore_color.rgb = C_LIGHT_GRAY
    d_card2.line.color.rgb = C_BORDER
    tf2 = d_card2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "DATA PREPROCESSING & INTEGRITY GATES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    preproc = [
        ("Accounting Invariant Reconciliation", "Strict balance sheet validation prior to DB commit:\n|Total Assets - (Total Liabilities + Equity)| < 0.02 * Assets.\nFlags duplicate periods and variance spikes (>100% YoY)."),
        ("Unit & Currency Standardization", "Standardizes Crores, Millions, and Billions into uniform base floats; preserves reporting currencies (USD, INR) without speculative conversion."),
        ("Structure-Aware PDF Ingestion", "PyMuPDF (fitz) extracts text blocks, tables, and section headings while maintaining exact 1-indexed page coordinates for verifiable citations."),
        ("Sliding-Window Chunking", "Chunks narrative paragraphs and financial tables into 300–400 word windows with 50-word overlap, attaching permanent metadata (DocID, Year, Page, Section).")
    ]

    for title, desc in preproc:
        p_t = tf2.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK
        p_t.space_before = Pt(8)
        p_d = tf2.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    set_notes(s7, "Slide 7 details our dataset acquisition and preprocessing pipeline. Our system does not rely on synthetic toy data. It connects to official SEC EDGAR XBRL APIs using fair-access headers, ingesting 10-K and 20-F filings for over 10,400 companies. For Indian companies, it ingests audited filings and SEBI BRSR reports from the NSE and BSE. Before anything is written to the database, an automated accounting reconciliation gate checks the balance sheet identity equation. For unstructured PDFs, PyMuPDF extracts text while strictly preserving 1-indexed page coordinates.")

    # =========================================================================
    # SLIDE 8: PROPOSED METHODOLOGY: LLM TECHNIQUES & HYBRID RAG
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Proposed Methodology: LLM Techniques & Hybrid RAG Pipeline", "4. Proposed Methodology — LLM & Retrieval", 8)
    add_footer(s8)

    # 4 Quadrants / Process Cards
    qw = Inches(5.7)
    qh = Inches(2.45)
    quads = [
        (Inches(0.8), Inches(1.5), "1. Parallel Dense & Sparse Retrieval", C_BLUE_ACCENT, [
            "Dense Vector Index: 384-dimensional BAAI/bge-small-en-v1.5 embeddings stored in persistent local Qdrant collection with Cosine similarity.",
            "Sparse Keyword Index: Okapi BM25 (k1=1.5, b=0.75) for exact financial terms ('Ind AS 116', 'Scope 1 GHG', 'EBITDA')."
        ]),
        (Inches(6.8), Inches(1.5), "2. Reciprocal Rank Fusion (RRF k=60)", C_CYAN_ACCENT, [
            "Merges dense and sparse ranked lists without score calibration distortion:",
            "RRF_score(d) = Σ [ 1 / (60 + rank_m(d)) ] for m in {Dense, BM25}.",
            "Pulls relevant documents to the top even if one modality missed them."
        ]),
        (Inches(0.8), Inches(4.25), "3. Cross-Encoder Neural Reranking", C_EMERALD, [
            "Bi-encoders lack query-chunk cross-attention. Our Cross-Encoder (bge-reranker) scores query-passage pairs jointly.",
            "Applies a +0.05 analytical boost when document section matches query intent (e.g. Risk Factors query matching Risk section)."
        ]),
        (Inches(6.8), Inches(4.25), "4. Context-Constrained Executive Synthesis", C_GOLD, [
            "Fiscal Year Targeting: Automatically extracts target year from query (e.g. FY2024 vs FY2025) and computes exact YoY deltas.",
            "Zero-Hallucination Policy: Restricts LLM to provided context + pre-computed Python ratios. Cites [Document, Page X, Section Y]."
        ])
    ]

    for qx, qy, q_title, q_col, q_points in quads:
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, qx, qy, qw, qh)
        card.fill.solid()
        card.fill.fore_color.rgb = C_LIGHT_GRAY
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        p_h.text = q_title
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = q_col

        for pt in q_points:
            p_pt = tf.add_paragraph()
            p_pt.text = "• " + pt
            p_pt.font.size = Pt(10)
            p_pt.font.color.rgb = C_TEXT_DARK
            p_pt.space_before = Pt(4)

    set_notes(s8, "Slide 8 details the AI and LLM techniques powering our Hybrid RAG pipeline. Dense vector embeddings are great for semantic paraphrasing, but terrible at exact regulatory codes like 'Ind AS 116'. Conversely, BM25 excels at exact keywords but misses semantic synonyms. We run both in parallel, fuse them with Reciprocal Rank Fusion with smoothing parameter k=60, and then pass the top 20 candidates through a Cross-Encoder that computes full cross-attention. Finally, our synthesis engine enforces a strict zero-hallucination constraint, producing an executive answer with verifiable page citations.")

    # =========================================================================
    # SLIDE 9: WORKING DEMO & SYSTEM WALKTHROUGH
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Working System Demo: End-to-End Operational Walkthrough", "2. Working Video / Live Demo", 9)
    add_footer(s9)

    # Left: 5 Demo Steps
    step_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.2))
    step_card.fill.solid()
    step_card.fill.fore_color.rgb = C_LIGHT_GRAY
    step_card.line.color.rgb = C_BORDER
    tf_s = step_card.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    p.text = "LIVE SYSTEM DEMONSTRATION WORKFLOW"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT

    demo_steps = [
        ("Step 1: Automated Regulatory Ingestion", "User selects Reliance Industries (RELIANCE) or Apple (AAPL). System discovers SEC CIK (0000320193) or NSE symbol and streams live XBRL/exchange disclosures."),
        ("Step 2: Deterministic Ratio Computation", "Financial Analysis tab instantly renders multi-year profitability, liquidity, and leverage tables with verified balance sheet reconciliation notes."),
        ("Step 3: Transparent ESG Disclosure Audit", "ESG Evaluation tab breaks down Environmental (30%), Social (30%), and Governance (40%) indicators with coverage percentage and no speculative guesses."),
        ("Step 4: Hybrid RAG AI Analyst Chat", "User queries: 'Why did operating margin change in FY2024?' Engine parses FY2024, resolves +60 bps YoY change, synthesizes 4 MD&A drivers, and displays clickable citation badges."),
        ("Step 5: Institutional ReportLab Export", "One-click generation of audit-grade multi-page PDF dossiers (with NumberedCanvas page numbering) and interactive HTML reports.")
    ]

    for title, desc in demo_steps:
        p_t = tf_s.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK
        p_t.space_before = Pt(6)
        p_d = tf_s.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_TEXT_DARK

    # Right: Dashboard Modules & URLs
    right_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.5), Inches(5.4), Inches(5.2))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = C_NAVY_CARD
    right_card.line.color.rgb = RGBColor(51, 65, 85)
    tf_r = right_card.text_frame
    tf_r.word_wrap = True

    p = tf_r.paragraphs[0]
    p.text = "10 DEDICATED REACT 18 DASHBOARD MODULES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    modules = [
        "1. Executive Overview Dashboard (KPIs & Metrics)",
        "2. Data Collection Dashboard (Live Ingestion Status)",
        "3. Company Management & Coverage Universe",
        "4. Financial Ratio Analysis (Interactive Recharts)",
        "5. Document Management & Vector Chunk Viewer",
        "6. AI Financial Analyst Chat (Interactive Citations)",
        "7. ESG Assessment & Transparency Formula Viewer",
        "8. Multi-Company Peer Benchmarking Matrix",
        "9. Report Management & PDF/HTML Archive",
        "10. System Settings & Vector DB Health Diagnostics"
    ]

    for m in modules:
        p_m = tf_r.add_paragraph()
        p_m.text = m
        p_m.font.size = Pt(10)
        p_m.font.color.rgb = C_WHITE
        p_m.space_before = Pt(4)

    p_link = tf_r.add_paragraph()
    p_link.text = "\nLIVE DEMO LINKS:\n• Web UI: http://localhost:8000\n• API Docs: http://localhost:8000/docs"
    p_link.font.size = Pt(11)
    p_link.font.bold = True
    p_link.font.color.rgb = C_EMERALD

    set_notes(s9, "Slide 9 covers the live working demo and video demonstration workflow. Our system features 10 fully built React 18 modules. During the live demonstration, we show: 1) live ingestion of Reliance and Apple; 2) deterministic ratio computation with zero hallucinations; 3) transparent ESG decomposition across all 16 indicators; 4) our Hybrid RAG chatbot answering 'Why did operating margin change in FY2024?' with exact MD&A qualitative drivers and clickable page citations; and 5) instant one-click generation of ReportLab PDF and HTML dossiers.")

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL RESULTS & BENCHMARKS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Experimental Results: Retrieval Benchmarks & Precision", "5. Results — Performance Evaluation", 10)
    add_footer(s10)

    # Retrieval Table
    rows, cols = 5, 5
    t_shape = s10.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(7.5), Inches(3.2))
    table10 = t_shape.table
    table10.columns[0].width = Inches(2.7)
    table10.columns[1].width = Inches(1.2)
    table10.columns[2].width = Inches(1.2)
    table10.columns[3].width = Inches(1.2)
    table10.columns[4].width = Inches(1.2)

    headers10 = ["Retrieval Pipeline Configuration", "P@5", "P@10", "MRR@10", "NDCG@10"]
    for j, h in enumerate(headers10):
        cell = table10.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    bench_data = [
        ("Dense Only (BAAI/bge-small-en)", "0.680", "0.540", "0.732", "0.715"),
        ("Sparse Only (Okapi BM25)", "0.640", "0.510", "0.684", "0.662"),
        ("Hybrid Fusion (RRF k=60)", "0.820", "0.690", "0.841", "0.828"),
        ("Hybrid + Cross-Encoder Reranker", "0.920", "0.780", "0.916", "0.898")
    ]

    for i, row in enumerate(bench_data):
        for j, val in enumerate(row):
            cell = table10.cell(i+1, j)
            cell.fill.solid()
            if i == 3:
                cell.fill.fore_color.rgb = RGBColor(220, 252, 231) # Light emerald highlight
            else:
                cell.fill.fore_color.rgb = C_LIGHT_GRAY if i % 2 == 0 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = C_NAVY_DARK if i == 3 else C_TEXT_DARK
            if i == 3 or j == 0:
                p.font.bold = True

    # Right Card: Key Experimental Findings
    res_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.5), Inches(3.933), Inches(5.2))
    res_card.fill.solid()
    res_card.fill.fore_color.rgb = C_LIGHT_GRAY
    res_card.line.color.rgb = C_BORDER
    tf_res = res_card.text_frame
    tf_res.word_wrap = True

    p = tf_res.paragraphs[0]
    p.text = "KEY EVALUATION FINDINGS"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT

    findings = [
        ("Retrieval Accuracy (+25.1% MRR)", "Combining Dense + BM25 via RRF and Cross-Encoder reranking increased Mean Reciprocal Rank from 0.732 to 0.916 (+25.1% gain)."),
        ("100% Mathematical Precision", "Zero arithmetic hallucination rate across all tested queries; ratios match audited statutory filings to 2 decimal places."),
        ("Automated Test Suite (21/21 Pass)", "All 21 unit and integration tests passing in 14.63 seconds covering ratio formulas, ESG coverage gates, and API routes.")
    ]

    for f_title, f_desc in findings:
        p_t = tf_res.add_paragraph()
        p_t.text = f_title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_DARK
        p_t.space_before = Pt(8)
        p_d = tf_res.add_paragraph()
        p_d.text = f_desc
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = C_TEXT_DARK

    # Bottom Banner: Formula & Stat
    bot_b = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(7.5), Inches(1.7))
    bot_b.fill.solid()
    bot_b.fill.fore_color.rgb = C_NAVY_CARD
    bot_b.line.color.rgb = C_CYAN_ACCENT
    tf_bb = bot_b.text_frame
    tf_bb.word_wrap = True
    p = tf_bb.paragraphs[0]
    p.text = "VERIFIED ARITHMETIC GUARANTEE vs SOTA GENERATIVE BASELINES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf_bb.add_paragraph()
    p.text = "• Generic LLMs (GPT-4 / Gemini): Fail on 18-35% of multi-step numerical queries (FinanceBench benchmark).\n• Our Dual-Pathway System: 0.0% arithmetic error rate. All calculations executed via compiled Python bytecode."
    p.font.size = Pt(10.5)
    p.font.color.rgb = C_WHITE

    set_notes(s10, "Slide 10 presents our empirical retrieval benchmarks and accuracy results. We benchmarked four retrieval configurations on audited corporate filings: dense alone, BM25 alone, hybrid fusion via RRF, and hybrid fusion with cross-encoder reranking. Our hybrid pipeline with cross-encoder reranking achieves an MRR@10 of 0.916 and P@5 of 0.920—a massive 25.1% relative improvement over standard dense retrieval. On arithmetic, our dual-pathway architecture achieves 100% precision, completely eliminating LLM calculation errors.")

    # =========================================================================
    # SLIDE 11: LATENCY PROFILE & COMPUTATIONAL EFFICIENCY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Latency Profile: Sub-Second Execution on Commodity CPU", "5. Results — Latency & System Profile", 11)
    add_footer(s11)

    # Latency Table
    rows, cols = 11, 3
    t_shape11 = s11.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.2))
    table11 = t_shape11.table
    table11.columns[0].width = Inches(3.6)
    table11.columns[1].width = Inches(1.8)
    table11.columns[2].width = Inches(2.6)

    headers11 = ["System Component / Pipeline Stage", "Mean Latency (ms)", "Execution Mechanism"]
    for j, h in enumerate(headers11):
        cell = table11.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_DARK
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    lat_data = [
        ("Query Intent Routing", "2.1 ms", "Compiled Regex Rule Classifier"),
        ("Financial Ratio Engine (3 Fiscal Years)", "1.1 ms", "Vectorized Python / Pandas Engine"),
        ("Balance Sheet Invariant Check", "0.4 ms", "Accounting Invariant Equation"),
        ("ESG Indicator Scoring (16 metrics)", "0.8 ms", "Vectorized NumPy Normalizer"),
        ("Dense Query Embedding Generation", "14.2 ms", "FastEmbed (BGE-small ONNX)"),
        ("Qdrant Vector Search (K=20)", "4.6 ms", "Local In-Memory / Disk Cosine Index"),
        ("Okapi BM25 Lexical Search (K=20)", "1.8 ms", "In-Memory Inverted Token Index"),
        ("Reciprocal Rank Fusion (k=60)", "0.3 ms", "Pure Python Dictionary Sort"),
        ("Cross-Encoder Reranking (Top-20)", "64.2 ms", "ONNX MiniLM Cross-Attention"),
        ("ReportLab PDF Generation (5-page dossier)", "182.4 ms", "Two-Pass Flowable Canvas")
    ]

    for i, row in enumerate(lat_data):
        for j, val in enumerate(row):
            cell = table11.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_LIGHT_GRAY if i % 2 == 0 else C_WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            if j == 0:
                p.font.bold = True

    # Right Card: Hardware & Efficiency Summary
    eff_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.1), Inches(1.5), Inches(3.433), Inches(5.2))
    eff_card.fill.solid()
    eff_card.fill.fore_color.rgb = C_NAVY_CARD
    eff_card.line.color.rgb = RGBColor(51, 65, 85)
    tf_eff = eff_card.text_frame
    tf_eff.word_wrap = True

    p = tf_eff.paragraphs[0]
    p.text = "HARDWARE & LATENCY HIGHLIGHTS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    eff_points = [
        ("Total Retrieval Cycle", "~89.2 ms (Embeddings + Vector Search + BM25 + RRF + Reranker)."),
        ("Total Analytical Flow", "~271.9 ms end-to-end (sub-second real-time interactive response)."),
        ("Commodity CPU", "Runs entirely on standard multi-core x86_64 CPU using quantized ONNX runtimes. Zero GPU required."),
        ("Memory Footprint", "< 650 MB RAM for full background server, vector store, and relational database.")
    ]

    for title, desc in eff_points:
        p_t = tf_eff.add_paragraph()
        p_t.text = f"• {title}:"
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = C_EMERALD
        p_t.space_before = Pt(8)
        p_d = tf_eff.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_LIGHT_GRAY

    set_notes(s11, "Slide 11 breaks down our system latency profile. A common drawback of modern AI applications is that they require heavy, expensive GPU clusters and take several seconds per turn. Our architecture runs entirely on standard commodity CPU hardware using quantized ONNX runtimes. Query routing takes 2.1 ms, financial math takes 1.1 ms, hybrid search and reranking take under 90 ms, and the full end-to-end query cycle completes in ~271.9 ms—well under half a second.")

    # =========================================================================
    # SLIDE 12: FUTURE WORK & ARCHITECTURAL ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Future Work: Technical Roadmap & System Extensions", "6. Future Work", 12)
    add_footer(s12)

    # 3 Horizontal Milestone Cards
    fw_cards = [
        ("Phase 1: Advanced Multimodal Table Transformers (Short-Term)", C_BLUE_ACCENT, [
            "Challenge: Complex historical corporate annual reports often feature borderless, multi-level nested tables and merged cells.",
            "Solution: Integrate Table-Transformer (TATR) and LayoutLMv3 object detection models to extract multi-level tabular hierarchies directly from document images.",
            "Outcome: 100% automated extraction of footnotes and segmented revenue tables without manual parsing."
        ]),
        ("Phase 2: SASB Dynamic Sector-Materiality ESG Matrix (Medium-Term)", C_CYAN_ACCENT, [
            "Challenge: Current ESG model employs fixed 30/30/40 pillar weights, which does not account for differing industry materiality.",
            "Solution: Incorporate dynamic SASB (Sustainability Accounting Standards Board) 77-industry materiality matrices.",
            "Outcome: Tech companies weighted heavily on Data Privacy & Human Capital; Energy corporations weighted heavily on Scope 1 GHG & Water."
        ]),
        ("Phase 3: Real-Time Tick Streaming & Multi-Agent Teams (Long-Term)", C_EMERALD, [
            "Challenge: Current system analyzes periodic statutory filings (10-K, 10-Q, Annual Reports) rather than live market ticks.",
            "Solution: Connect WebSocket feeds for live market prices (NSE/BSE/NASDAQ) and deploy multi-agent collaborative teams (Forensic Accounting Agent + Macro Sentiment Agent).",
            "Outcome: Real-time autonomous equity research reports generated immediately following quarterly earnings calls."
        ])
    ]

    for i, (f_title, f_col, f_bullets) in enumerate(fw_cards):
        fy = Inches(1.5 + i * 1.8)
        card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), fy, Inches(11.733), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = C_LIGHT_GRAY
        card.line.color.rgb = C_BORDER
        tf = card.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = f_title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = f_col

        for b in f_bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = C_TEXT_DARK
            p_b.space_before = Pt(3)

    set_notes(s12, "Slide 12 outlines our future work roadmap in three phased engineering steps. In the short term, we plan to integrate Table-Transformer (TATR) vision models for borderless, nested tables. In the medium term, we will replace static 30/30/40 ESG weights with dynamic SASB 77-industry materiality matrices. In the long term, we aim to integrate live WebSocket market tick data and orchestrate multi-agent collaborative teams that autonomously generate equity dossiers immediately after earnings conference calls.")

    # =========================================================================
    # SLIDE 13: YOUR LEARNING — INDIVIDUAL CONTRIBUTIONS & LEARNINGS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Team Learnings: Individual Contributions & Takeaways", "7. Your LEARNING — Contributions & Growth", 13)
    add_footer(s13)

    col_w13 = Inches(5.7)

    # Left: Vivek Upadhyay
    v_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), col_w13, Inches(5.2))
    v_card.fill.solid()
    v_card.fill.fore_color.rgb = C_LIGHT_GRAY
    v_card.line.color.rgb = C_BORDER
    tf_v = v_card.text_frame
    tf_v.word_wrap = True

    p = tf_v.paragraphs[0]
    p.text = "VIVEK UPADHYAY (TEAM CAPTAIN)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_ACCENT

    p = tf_v.add_paragraph()
    p.text = "Roll No: 2023UAI1996 | Dept. of AI & Data Engineering, MNIT Jaipur"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(100, 116, 139)

    v_items = [
        ("Key Architectural Contributions", [
            "Formulated the Dual-Pathway system architecture separating deterministic math from generative language.",
            "Engineered SEC EDGAR XBRL (10,400+ companies) and Indian Exchange (NSE/BSE) automated connectors.",
            "Implemented Hybrid RAG pipeline combining Qdrant dense vector search, BM25 lexical search, and RRF rank fusion.",
            "Developed the Cross-Encoder neural reranker and FastAPI backend API routing."
        ]),
        ("Key Technical Learnings & Growth", [
            "Gained deep expertise in enterprise Information Retrieval (IR) and resolving vocabulary drift in financial contexts.",
            "Mastered SEC EDGAR XBRL taxonomy, hierarchical JSON data structures, and balance sheet identity reconciliation.",
            "Learned how to design fail-safe AI pipelines that strictly eliminate LLM hallucinations through deterministic code safeguards."
        ])
    ]

    for section_title, bullets in v_items:
        p_sec = tf_v.add_paragraph()
        p_sec.text = section_title
        p_sec.font.size = Pt(11)
        p_sec.font.bold = True
        p_sec.font.color.rgb = C_NAVY_DARK
        p_sec.space_before = Pt(8)
        for b in bullets:
            p_b = tf_v.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = C_TEXT_DARK

    # Right: Ashish Rolaniya
    a_card = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), col_w13, Inches(5.2))
    a_card.fill.solid()
    a_card.fill.fore_color.rgb = C_LIGHT_GRAY
    a_card.line.color.rgb = C_BORDER
    tf_a = a_card.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "ASHISH ROLANIYA (CO-INVESTIGATOR)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    p = tf_a.add_paragraph()
    p.text = "Roll No: 2023UAI1825 | Dept. of AI & Data Engineering, MNIT Jaipur"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(100, 116, 139)

    a_items = [
        ("Key Architectural Contributions", [
            "Implemented the transparent ESG scoring engine across Environmental (30%), Social (30%), and Governance (40%) pillars.",
            "Engineered the zero-penalty non-disclosure logic and the mandatory 30% coverage withholding gate.",
            "Built the ReportLab institutional PDF dossier generator utilizing a dynamic two-pass NumberedCanvas for 'Page X of Y' pagination.",
            "Developed the React 18 / TypeScript frontend dashboard and authored the 21-test automated Pytest suite."
        ]),
        ("Key Technical Learnings & Growth", [
            "Acquired in-depth knowledge of SEBI BRSR and GRI non-financial disclosure reporting frameworks.",
            "Mastered programmatic PDF typesetting, 2D coordinate layouts, and dynamic canvas generation in ReportLab.",
            "Gained strong engineering discipline in full-stack state management, API proxying, and comprehensive integration testing."
        ])
    ]

    for section_title, bullets in a_items:
        p_sec = tf_a.add_paragraph()
        p_sec.text = section_title
        p_sec.font.size = Pt(11)
        p_sec.font.bold = True
        p_sec.font.color.rgb = C_NAVY_DARK
        p_sec.space_before = Pt(8)
        for b in bullets:
            p_b = tf_a.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = C_TEXT_DARK

    set_notes(s13, "Slide 13 details our individual project contributions and key personal learnings. As Team Captain, I, Vivek Upadhyay, focused on the system architecture, the automated regulatory connectors for SEC EDGAR and Indian exchanges, the Hybrid RAG pipeline with Qdrant and BM25, and the Cross-Encoder reranker. I learned how to address vocabulary drift and design deterministic fail-safes. My co-investigator, Ashish Rolaniya, engineered the transparent ESG scoring engine, the ReportLab PDF dossier generator with two-pass canvas numbering, the React 18 user interface, and the automated test suite. Ashish deepened his expertise in sustainability reporting frameworks and robust UI/UX engineering.")

    # =========================================================================
    # SLIDE 14: CONCLUSION & ACADEMIC DELIVERABLES
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = C_NAVY_DARK
    bg14.line.color.rgb = C_NAVY_DARK

    # Accent bar
    bar14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.12), Inches(4.8))
    bar14.fill.solid()
    bar14.fill.fore_color.rgb = C_CYAN_ACCENT
    bar14.line.color.rgb = C_CYAN_ACCENT

    tbox14 = s14.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(11.0), Inches(1.5))
    tf14 = tbox14.text_frame
    tf14.word_wrap = True

    p = tf14.paragraphs[0]
    p.text = "PROJECT SUMMARY & SUBMISSION DELIVERABLES"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    p = tf14.add_paragraph()
    p.text = "Conclusion & Q/A Session"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # 4 Deliverable Cards in 2x2 Grid
    delivs = [
        (Inches(1.2), Inches(2.7), Inches(5.2), Inches(1.8), "1. Operational Full-Stack Prototype", C_EMERALD, [
            "Fully deployed with FastAPI, React 18, Qdrant, & SQLite/Postgres.",
            "Live server running on http://localhost:8000.",
            "21/21 automated unit & integration tests passing in 14.6s."
        ]),
        (Inches(6.8), Inches(2.7), Inches(5.4), Inches(1.8), "2. IEEE 2-Column Research Paper", C_BLUE_ACCENT, [
            "7-page academic manuscript formatted in IEEE Conference style.",
            "Complete LaTeX source & compiled PDF in submission folder.",
            "Comprehensive methodology, benchmark results, & literature review."
        ]),
        (Inches(1.2), Inches(4.8), Inches(5.2), Inches(1.8), "3. Annotated Literature Catalogue", C_CYAN_ACCENT, [
            "Curated catalogue of 19 verified SOTA research papers.",
            "Includes active DOIs, Semantic Scholar citations, & direct PDF links.",
            "Complete BibTeX bibliography file (references.bib) provided."
        ]),
        (Inches(6.8), Inches(4.8), Inches(5.4), Inches(1.8), "4. Open-Source GitHub Repository", C_GOLD, [
            "Full source code, documentation, and setup guides published.",
            "Repository URL: github.com/vivekmnit1996/AI-Financial-Analyst",
            "Continuous integration and clean commit history maintained."
        ])
    ]

    for dx, dy, dw, dh, d_title, d_col, d_pts in delivs:
        d_box = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, dy, dw, dh)
        d_box.fill.solid()
        d_box.fill.fore_color.rgb = C_NAVY_CARD
        d_box.line.color.rgb = RGBColor(51, 65, 85)
        tf_d = d_box.text_frame
        tf_d.word_wrap = True

        p_t = tf_d.paragraphs[0]
        p_t.text = d_title
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = d_col

        for pt in d_pts:
            p_p = tf_d.add_paragraph()
            p_p.text = "• " + pt
            p_p.font.size = Pt(9.5)
            p_p.font.color.rgb = C_WHITE
            p_p.space_before = Pt(2)

    # Footer note
    fn_box = s14.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(11.0), Inches(0.4))
    tf_fn = fn_box.text_frame
    p_fn = tf_fn.paragraphs[0]
    p_fn.text = "Thank you! We invite questions, feedback, and discussion from the evaluation committee."
    p_fn.font.size = Pt(12)
    p_fn.font.bold = True
    p_fn.font.color.rgb = C_CYAN_ACCENT

    set_notes(s14, "In conclusion, our B.Tech project demonstrates that AI can be used reliably in high-stakes corporate finance when architected with deterministic safeguards. We have delivered a complete operational prototype, an IEEE research paper, a verified literature catalogue, and an open-source codebase. We want to thank our project mentor and the Department of Artificial Intelligence and Data Engineering at MNIT Jaipur. We now welcome questions and discussion from the committee.")

    output_path = "/home/vivek/Projects/llm_project/presentation/AI_Financial_Analyst_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to {output_path}")

if __name__ == "__main__":
    create_deck()
