# Academic Submission: AI Financial Analyst & Report Generator

**Course / Degree:** Bachelor of Technology (B.Tech) in Artificial Intelligence and Data Engineering  
**Project Title:** AI Financial Analyst & Report Generator: An Integrated Framework for Financial Analytics, ESG Assessment and Evidence-Grounded Report Generation Using Hybrid RAG  
**Institutional Affiliation:** Department of Artificial Intelligence and Data Engineering, Malaviya National Institute of Technology (MNIT) Jaipur, Rajasthan, India  

### Project Investigators:
1. **Vivek Upadhyay** — *Team Captain* — Roll No. `2023UAI1996` (Email: `2023uai1996@mnit.ac.in`)
2. **Ashish Rolaniya** — *Co-Investigator* — Roll No. `2023UAI1825` (Email: `2023uai1825@mnit.ac.in`)

---

## 1. Directory & Deliverables Overview

This submission package contains the complete academic deliverables, verified research paper literature catalog, traceability matrices, and compile-ready source files prepared for project mentor review:

```
AI_Financial_Analyst_Academic_Submission/
├── AI_Financial_Analyst_IEEE_Research_Paper.pdf     # Primary academic manuscript in IEEE two-column format
├── AI_Financial_Analyst_IEEE_Research_Paper.tex     # Full LaTeX source code for the research manuscript
├── references.bib                                   # Verified BibTeX bibliography with 19 peer-reviewed citations
├── AI_Financial_Analyst_Research_Literature_and_Links.pdf # Literature catalogue with clickable DOIs and OA PDFs
├── Research_to_Implementation_Mapping.pdf           # Traceability matrix mapping system code to literature
├── Research_Papers_Metadata.csv                     # Machine-readable inventory of all 19 verified papers
├── README.md                                        # This documentation file
├── figures/                                         # High-resolution architectural and benchmark figures
│   ├── system_architecture.png                      # Multi-tier end-to-end architecture diagram
│   └── retrieval_benchmark.png                      # Empirical retrieval performance benchmark chart
└── Research_Paper_Source_Files/                     # Clean archive of all TeX sources, bibs, and assets
```

---

## 2. Research Verification & Literature Summary

Every research paper included in this work has been systematically cross-referenced and verified against official academic APIs (**Crossref** and **arXiv**). No citations, DOIs, authors, or publication venues were fabricated.

- **Total Papers Reviewed & Verified:** 19
- **Direct Open-Access PDF Links:** 16 (84.2%)
- **Verified DOIs:** 11 (Crossref indexed)
- **Official arXiv Preprints:** 8 (arXiv official API indexed)
- **Peer-Reviewed Venues:** NeurIPS, ACL, EMNLP, SIGIR, KDD, CVPR, COLING, Review of Finance (Oxford University Press), Foundations and Trends in Information Retrieval.

### Research Domains Covered:
1. **Financial Question Answering & Numerical Reasoning:** FinQA (Chen et al., EMNLP '21), TAT-QA (Zhu et al., ACL '21), FinanceBench (Islam et al., '23).
2. **Retrieval-Augmented Generation (RAG):** Original RAG (Lewis et al., NeurIPS '20), Dense Passage Retrieval (Karpukhin et al., EMNLP '20), HyDE (Gao et al., ACL '23).
3. **Hybrid Information Retrieval:** Okapi BM25 (Robertson & Zaragoza, '09), Sentence-BERT (Reimers & Gurevych, EMNLP '19), BGE Embeddings (Xiao et al., '23).
4. **Rank Aggregation & Reranking:** Reciprocal Rank Fusion (Cormack et al., SIGIR '09), Passage Reranking with BERT (Nogueira & Cho, '19).
5. **Document Layout & Table Extraction:** LayoutLM (Xu et al., KDD '20), PubTables-1M (Smock et al., CVPR '22), DocBank (Li et al., COLING '20).
6. **Financial Domain NLP:** BloombergGPT (Wu et al., '23), FinBERT (Araci, '19), FinGPT (Yang et al., IJCAI '23).
7. **ESG Analysis & Rating Transparency:** Aggregate Confusion (Berg et al., Review of Finance '22), ClimateBERT (Webersinke et al., '21).

---

## 3. Core Architectural Principles Implemented in Code

1. **Deterministic Financial Arithmetic:**  
   As proven in BloombergGPT and FinanceBench, standard LLMs suffer from severe arithmetic errors and hallucinated calculations. In our implementation, all 14 financial ratios (Gross/Operating/Net Margins, ROE, ROA, Debt-to-Equity, Current Ratio, Cash Flow Conversion, Revenue Growth) are executed deterministically using vectorized Python/Pandas in `backend/app/engine/financial_calculator.py`.

2. **Structure-Aware Document Ingestion & Hybrid RAG:**  
   Unstructured corporate filings (Annual Reports, 10-Ks, BRSR filings) are ingested with PyMuPDF/pdfplumber, retaining physical page coordinates and table alignments. Retrieval executes parallel queries across a 384-dimensional dense Qdrant vector index (`BAAI/bge-small-en-v1.5`) and an in-memory sparse Okapi BM25 index, fused via Reciprocal Rank Fusion ($k=60$) and reranked using a Cross-Encoder (`BAAI/bge-reranker-base`).

3. **Transparent, Coverage-Gated ESG Engine:**  
   To eliminate the 50% rating divergence identified in MIT Sloan's "Aggregate Confusion", our system assesses 10 verifiable quantitative indicators across E (30%), S (30%), and G (40%). Missing disclosures are normalized without penalizing non-disclosures as zero, and an explicit 30% reporting coverage gate prevents speculative scoring.

4. **100% Page-Anchored Citation Traceability:**  
   Every synthesized qualitative finding is cited using strict bracketed anchors: `[Document Title, Page X, Section Y]`.

---

## 4. Compilation & Verification Instructions

To re-compile the IEEE research paper from source using the standalone `tectonic` engine:

```bash
cd AI_Financial_Analyst_Academic_Submission
../bin/tectonic AI_Financial_Analyst_IEEE_Research_Paper.tex -o .
```

To run the automated backend test suite:

```bash
source .venv/bin/activate
pytest backend/tests/ -v
```
*(All 15 automated tests pass with 100% success).*
