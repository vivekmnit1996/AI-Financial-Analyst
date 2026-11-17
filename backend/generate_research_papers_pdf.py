import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.config import settings
from backend.app.rag.sample_document_generator import NumberedCanvas

def generate_papers_pdf():
    output_dir = settings.REPORTS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / "Research_Papers_Reference_Dossier.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=44,
        bottomMargin=44
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )
    category_style = ParagraphStyle(
        "CategoryHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=14,
        spaceAfter=6
    )
    paper_title_style = ParagraphStyle(
        "PaperTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2
    )
    meta_style = ParagraphStyle(
        "PaperMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=3
    )
    link_style = ParagraphStyle(
        "PaperLink",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1D4ED8"),
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "PaperBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=8
    )
    impl_style = ParagraphStyle(
        "PaperImpl",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#047857"),
        spaceAfter=8
    )

    story = []

    # Title & Header
    story.append(Paragraph("THEORETICAL FOUNDATIONS & RESEARCH PAPERS DOSSIER", title_style))
    story.append(Paragraph(
        "<b>Project:</b> AI Financial Analyst & Report Generator (B.Tech AI & Data Engineering)<br/>"
        "<b>Core Architecture:</b> Hybrid RAG (Dense + BM25) • Reciprocal Rank Fusion • Cross-Encoder Reranking • "
        "Deterministic Financial Modeling • Transparent ESG Indicators",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=0, spaceAfter=12))

    papers = [
        # ========================================================
        # Category 1: Retrieval-Augmented Generation (RAG)
        # ========================================================
        {
            "category": "1. Retrieval-Augmented Generation (RAG) Architecture",
            "items": [
                {
                    "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
                    "authors": "Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela",
                    "venue": "Advances in Neural Information Processing Systems (NeurIPS 2020)",
                    "url": "https://arxiv.org/abs/2005.11401",
                    "summary": "The seminal paper proposing the RAG framework, combining pre-trained parametric memory (neural LLM) with non-parametric retrieval memory. Shows that hybrid conditioning drastically reduces factual hallucination and enables dynamic external knowledge indexing.",
                    "impl": "Project Mapping: Forms the foundational design pattern of the AI Analyst. Non-parametric memory is realized via Qdrant and BM25 indexers; parametric synthesis is performed in backend/app/rag/llm_service.py."
                },
                {
                    "title": "Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)",
                    "authors": "Luyu Gao, Xueguang Ma, Jimmy Lin, Jamie Callan",
                    "venue": "Annual Meeting of the Association for Computational Linguistics (ACL 2023)",
                    "url": "https://arxiv.org/abs/2212.10496",
                    "summary": "Introduces Hypothetical Document Embeddings (HyDE), investigating the semantic divergence between short user financial queries and verbose document passages, highlighting the importance of dense-lexical alignment.",
                    "impl": "Project Mapping: Informs query transformation and semantic expansion in backend/app/rag/hybrid_retriever.py to ensure short queries ('operating margin decline') match long corporate disclosures."
                }
            ]
        },

        # ========================================================
        # Category 2: Lexical, Dense & Hybrid Retrieval
        # ========================================================
        {
            "category": "2. Lexical & Dense Retrieval Foundations",
            "items": [
                {
                    "title": "The Probabilistic Relevance Framework: BM25 and Beyond",
                    "authors": "Stephen Robertson, Hugo Zaragoza",
                    "venue": "Foundations and Trends in Information Retrieval, Vol. 3, No. 4 (2009)",
                    "url": "https://www.nowpublishers.com/article/Details/INR-019",
                    "summary": "Establishes the theoretical derivations of Okapi BM25, term frequency non-linear saturation, document length normalization (b parameter), and inverse document frequency (IDF) for exact lexical matching.",
                    "impl": "Project Mapping: Implemented in backend/app/rag/bm25_search.py via rank_bm25. Crucial for exact corporate financial terminology ('EBITDA', 'Ind AS', 'Scope 1', 'LTIR') where dense embeddings alone experience semantic drift."
                },
                {
                    "title": "C-Pack: Packaged Resources to Advance General Chinese and English Embeddings (BGE)",
                    "authors": "Shitao Xiao, Zheng Liu, Peitian Zhang, Niklas Muennighoff",
                    "venue": "arXiv preprint arXiv:2309.07597 (2023)",
                    "url": "https://arxiv.org/abs/2309.07597",
                    "summary": "Presents BAAI General Embedding (BGE) models trained with multi-task contrastive learning, establishing top-tier performance on the Massive Text Embedding Benchmark (MTEB). Demonstrates superior cross-entropy discrimination on dense retrieval.",
                    "impl": "Project Mapping: Deployed via fastembed (BAAI/bge-small-en-v1.5) in backend/app/rag/vector_store.py as our primary 384-dimensional dense semantic embedding engine."
                },
                {
                    "title": "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
                    "authors": "Nils Reimers, Iryna Gurevych",
                    "venue": "Conference on Empirical Methods in Natural Language Processing (EMNLP 2019)",
                    "url": "https://arxiv.org/abs/1908.10084",
                    "summary": "Proposes Siamese and triplet network structures to generate semantically meaningful fixed-size sentence vectors, reducing cosine similarity search from hours to milliseconds for production vector databases.",
                    "impl": "Project Mapping: Underpins the vector geometry indexed inside our persistent Qdrant collection (backend/app/rag/vector_store.py)."
                }
            ]
        },

        # ========================================================
        # Category 3: Rank Fusion & Cross-Encoder Reranking
        # ========================================================
        {
            "category": "3. Rank Aggregation & Cross-Encoder Reranking",
            "items": [
                {
                    "title": "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods",
                    "authors": "Gordon V. Cormack, Charles L. A. Clarke, Stefan Büttcher",
                    "venue": "ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2009)",
                    "url": "https://dl.acm.org/doi/10.1145/1571941.1572114",
                    "summary": "Introduces Reciprocal Rank Fusion (RRF), proving that combining rankings by RRF(d) = sum(1 / (k + rank(d))) with constant k=60 yields monotonic, parameter-free superiority over Condorcet voting and score normalization.",
                    "impl": "Project Mapping: Directly implemented in backend/app/rag/hybrid_retriever.py with settings.RRF_K = 60 to fuse parallel Qdrant dense vector hits and BM25 lexical hits."
                },
                {
                    "title": "Passage Re-ranking with BERT",
                    "authors": "Rodrigo Nogueira, Kyunghyun Cho",
                    "venue": "arXiv preprint arXiv:1901.04085 (2019)",
                    "url": "https://arxiv.org/abs/1901.04085",
                    "summary": "Demonstrates that feeding query and candidate passages jointly into cross-attention layers allows full token-to-token cross-attention, drastically outperforming dual-encoder bi-encoders for reranking top-k candidates.",
                    "impl": "Project Mapping: Deployed in backend/app/rag/reranker.py using fastembed TextCrossEncoder (BAAI/bge-reranker-base) combined with section proximity boost to surface final citations."
                }
            ]
        },

        # ========================================================
        # Category 4: Financial NLP & Deterministic Calculations
        # ========================================================
        {
            "category": "4. Financial Natural Language Processing & Domain Models",
            "items": [
                {
                    "title": "BloombergGPT: A Large Language Model for Finance",
                    "authors": "Shijie Wu, Ozan Irsoy, Steven Lu, Vadim Dabravolski, Mark Dredze, Sebastian Gehrmann, Prabhanjan Kambadur, David Rosenberg, Gideon Mann",
                    "venue": "arXiv preprint arXiv:2303.17564 (Bloomberg, 2023)",
                    "url": "https://arxiv.org/abs/2303.17564",
                    "summary": "Presents a 50-billion parameter language model trained on a curated financial dataset. Crucially analyzes financial numerical reasoning and highlights LLM limitations with arithmetic precision, establishing why deterministic engines are mandatory.",
                    "impl": "Project Mapping: Validates our core architectural rule: Financial metrics (ROE, margins, growth) MUST be computed by Python/Pandas (backend/app/engine/financial_calculator.py) rather than generated by an LLM."
                },
                {
                    "title": "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models",
                    "authors": "Dogu Araci",
                    "venue": "arXiv preprint arXiv:1908.10063 (2019)",
                    "url": "https://arxiv.org/abs/1908.10063",
                    "summary": "Demonstrates domain adaptation of transformer models for corporate disclosures, analyzing Management Discussion & Analysis (MD&A) sections and shareholder reports.",
                    "impl": "Project Mapping: Guided the section recognition regex and classification patterns in backend/app/rag/document_parser.py."
                },
                {
                    "title": "FinGPT: Open-Source Financial Large Language Models",
                    "authors": "Hongyang Yang, Xiao-Yang Liu, Christina Dan Wang",
                    "venue": "FinLLM Symposium, IJCAI (2023)",
                    "url": "https://arxiv.org/abs/2306.06031",
                    "summary": "Outlines open-source workflows for automated financial data collection from SEC EDGAR, stock exchange filings, and financial news, highlighting data pipeline reconciliation techniques.",
                    "impl": "Project Mapping: Influenced the SEC EDGAR XBRL connector (backend/app/collectors/sec_edgar_connector.py) and data validation engine (backend/app/collectors/data_validator.py)."
                }
            ]
        },

        # ========================================================
        # Category 5: ESG Disclosures & Rating Divergence
        # ========================================================
        {
            "category": "5. ESG Disclosures & Rating Transparency",
            "items": [
                {
                    "title": "Aggregate Confusion: The Divergence of ESG Ratings",
                    "authors": "Florian Berg, Julian F. Kölbel, Roberto Rigobon",
                    "venue": "Review of Finance, Vol. 26, Issue 6, Oxford University Press (2022)",
                    "url": "https://academic.oup.com/rof/article/26/6/1315/6590242",
                    "summary": "Landmark MIT Sloan study demonstrating that commercial ESG ratings (MSCI, Sustainalytics, S&P) correlate at only 0.54 due to scope divergence, measurement divergence, and black-box weightings. Concludes that transparent, indicator-level decomposition is necessary.",
                    "impl": "Project Mapping: Directly inspired backend/app/engine/esg_scorer.py. Eliminates black-box scoring by providing full formula disclosure, separate pillar visibility (E: 30%, S: 30%, G: 40%), and never penalizing missing indicators as zeros."
                },
                {
                    "title": "ClimateBERT: A Pretrained Language Model for Climate-Related Text",
                    "authors": "Nicolas Webersinke, Mathias Kraus, Julia Anna Bingler, Markus Leippold",
                    "venue": "arXiv preprint arXiv:2110.12010 / AAAI (2021)",
                    "url": "https://arxiv.org/abs/2110.12010",
                    "summary": "Analyzes corporate environmental disclosures under TCFD and BRSR frameworks, emphasizing the distinction between disclosed quantitative indicators (Scope 1/2 GHG emissions) and qualitative commitments.",
                    "impl": "Project Mapping: Utilized in the environmental indicator extraction and validation schema in backend/app/collectors/exchange_connector.py and backend/app/engine/esg_scorer.py."
                }
            ]
        }
    ]

    for cat in papers:
        story.append(Paragraph(cat["category"], category_style))
        for p in cat["items"]:
            entry = [
                Paragraph(f"<b>{p['title']}</b>", paper_title_style),
                Paragraph(f"<b>Authors:</b> {p['authors']}", meta_style),
                Paragraph(f"<b>Venue / Publication:</b> {p['venue']}", meta_style),
                Paragraph(f"<b>Official Paper Link / DOI:</b> <a href='{p['url']}' color='#1D4ED8'><u>{p['url']}</u></a>", link_style),
                Paragraph(f"<b>Theoretical Contribution:</b> {p['summary']}", body_style),
                Paragraph(f"<b>System Implementation:</b> {p['impl']}", impl_style),
                Spacer(1, 4)
            ]
            story.append(KeepTogether(entry))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    return str(pdf_path)

if __name__ == "__main__":
    path = generate_papers_pdf()
    print(f"Generated Research Papers Dossier PDF: {path}")
