import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

# 19 Selected Research Papers across 7 Categories
CANDIDATE_PAPERS = [
    # A. Financial Question Answering & Benchmarks
    {
        "id": "chen2021finqa",
        "category": "A. Financial Question Answering",
        "title": "FinQA: A Dataset of Numerical Reasoning over Financial Data",
        "doi": "10.18653/v1/2021.emnlp-main.300",
        "arxiv": "2109.00122",
        "relevance": "Underpins the critical need for hybrid textual and numerical reasoning in financial disclosures. Inspires our dual-pathway approach separating structured calculations from document reasoning.",
        "component_role": "Benchmark & Architectural Motivation"
    },
    {
        "id": "zhu2021tatqa",
        "category": "A. Financial Question Answering",
        "title": "TAT-QA: A Question Answering Benchmark on a Hybrid of Text and Table",
        "doi": "10.18653/v1/2021.acl-long.254",
        "arxiv": "2105.07624",
        "relevance": "Demonstrates that tabular financial facts require specialized extraction and cannot be treated as flat prose. Direct motivation for structured table extraction in PyMuPDF/pdfplumber pipeline.",
        "component_role": "Theoretical Foundation & Benchmark Motivation"
    },
    {
        "id": "islam2023financebench",
        "category": "A. Financial Question Answering",
        "title": "FinanceBench: A New Benchmark for Evaluating Financial LLMs on Complex Financial Reasoning",
        "doi": "",
        "arxiv": "2311.11944",
        "relevance": "Evaluates commercial LLMs on real 10-K filings, revealing high hallucination rates on calculation tasks and justifying our strict deterministic calculation rule.",
        "component_role": "Evaluation Benchmark & Problem Motivation"
    },

    # B. Retrieval-Augmented Generation (RAG)
    {
        "id": "lewis2020rag",
        "category": "B. Retrieval-Augmented Generation",
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "doi": "10.48550/arXiv.2005.11401",
        "arxiv": "2005.11401",
        "relevance": "Seminal foundation combining non-parametric retrieval memory with parametric generator. Core design architecture of our backend RAG system.",
        "component_role": "Foundational Concept & Architecture"
    },
    {
        "id": "karpukhin2020dpr",
        "category": "B. Retrieval-Augmented Generation",
        "title": "Dense Passage Retrieval for Open-Domain Question Answering",
        "doi": "10.18653/v1/2020.emnlp-main.550",
        "arxiv": "2004.04906",
        "relevance": "Proves superiority of dual-encoder dense representations over classic TF-IDF for semantic question-answering across large document corpora.",
        "component_role": "Theoretical Foundation"
    },
    {
        "id": "gao2023hyde",
        "category": "B. Retrieval-Augmented Generation",
        "title": "Precise Zero-Shot Dense Retrieval without Relevance Labels",
        "doi": "10.18653/v1/2023.acl-short.32",
        "arxiv": "2212.10496",
        "relevance": "Hypothetical Document Embeddings (HyDE) technique that bridges the vocabulary gap between short user prompts and verbose annual report disclosures.",
        "component_role": "Query Expansion Technique"
    },

    # C. Hybrid Information Retrieval
    {
        "id": "robertson2009bm25",
        "category": "C. Hybrid Information Retrieval",
        "title": "The Probabilistic Relevance Framework: BM25 and Beyond",
        "doi": "10.1561/1500000019",
        "arxiv": "",
        "relevance": "Provides probabilistic derivation of BM25 term weighting with non-linear saturation, implemented in backend/app/rag/bm25_search.py for exact ticker/metric lookups.",
        "component_role": "Directly Implemented Component"
    },
    {
        "id": "reimers2019sbert",
        "category": "C. Hybrid Information Retrieval",
        "title": "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
        "doi": "10.18653/v1/D19-1410",
        "arxiv": "1908.10084",
        "relevance": "Forms mathematical basis of bi-encoder dense sentence vectors indexed into Qdrant for fast cosine similarity nearest-neighbor search.",
        "component_role": "Theoretical Foundation & Deployed Model Structure"
    },
    {
        "id": "xiao2023bge",
        "category": "C. Hybrid Information Retrieval",
        "title": "C-Pack: Packaged Resources to Advance General Chinese and English Embeddings",
        "doi": "10.48550/arXiv.2309.07597",
        "arxiv": "2309.07597",
        "relevance": "Introduces BGE embedding models; BAAI/bge-small-en-v1.5 is the exact default embedding engine used in our Qdrant vector store.",
        "component_role": "Directly Implemented Model"
    },

    # D. Rank Aggregation & Cross-Encoder Reranking
    {
        "id": "cormack2009rrf",
        "category": "D. Rank Aggregation & Reranking",
        "title": "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods",
        "doi": "10.1145/1571941.1572114",
        "arxiv": "",
        "relevance": "Introduces Reciprocal Rank Fusion (RRF k=60). Directly implemented in backend/app/rag/hybrid_retriever.py to combine dense Qdrant and sparse BM25 scores.",
        "component_role": "Directly Implemented Algorithm"
    },
    {
        "id": "nogueira2019passage",
        "category": "D. Rank Aggregation & Reranking",
        "title": "Passage Re-ranking with BERT",
        "doi": "10.48550/arXiv.1901.04085",
        "arxiv": "1901.04085",
        "relevance": "Establishes cross-attention reranking architecture over top-k retrieved candidates, implemented in backend/app/rag/reranker.py using bge-reranker.",
        "component_role": "Directly Implemented Architecture"
    },

    # E. Financial Document & Table Processing
    {
        "id": "xu2020layoutlm",
        "category": "E. Financial Document Processing",
        "title": "LayoutLM: Pre-training of Text and Layout for Document Image Understanding",
        "doi": "10.1145/3394486.3403172",
        "arxiv": "1912.13318",
        "relevance": "Demonstrates multimodal coordinate-aware document layout representation. Guided our structure-aware chunking preserving section hierarchy and page numbers.",
        "component_role": "Methodological Inspiration"
    },
    {
        "id": "smock2022pubtables",
        "category": "E. Financial Document Processing",
        "title": "PubTables-1M: Towards Comprehensive Table Extraction from Unstructured Documents",
        "doi": "10.1109/CVPR52688.2022.00458",
        "arxiv": "2110.00061",
        "relevance": "Addresses table boundary detection, row-column grid alignment, and cell spanning in complex financial statements.",
        "component_role": "Methodological Inspiration"
    },
    {
        "id": "li2020docbank",
        "category": "E. Financial Document Processing",
        "title": "DocBank: A Benchmark Dataset for Document Layout Analysis",
        "doi": "10.18653/v1/2020.coling-main.87",
        "arxiv": "2006.01038",
        "relevance": "Highlights importance of bounding-box spatial tokenization for complex multi-column layouts like corporate balance sheets and annual reports.",
        "component_role": "Methodological Inspiration"
    },

    # F. Financial Domain NLP & Models
    {
        "id": "wu2023bloomberggpt",
        "category": "F. Financial NLP & Domain Models",
        "title": "BloombergGPT: A Large Language Model for Finance",
        "doi": "10.48550/arXiv.2303.17564",
        "arxiv": "2303.17564",
        "relevance": "Pioneering financial LLM analyzing domain-specific financial syntax. Critically documents LLM numerical errors on accounting statements, justifying deterministic engine.",
        "component_role": "Theoretical & Architectural Motivation"
    },
    {
        "id": "araci2019finbert",
        "category": "F. Financial NLP & Domain Models",
        "title": "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models",
        "doi": "10.48550/arXiv.1908.10063",
        "arxiv": "1908.10063",
        "relevance": "Demonstrates domain adaptation for financial vocabulary. Informs section parsing and financial terminology detection in document ingestion.",
        "component_role": "Domain Adaptation Foundation"
    },
    {
        "id": "yang2023fingpt",
        "category": "F. Financial NLP & Domain Models",
        "title": "FinGPT: Open-Source Financial Large Language Models",
        "doi": "10.48550/arXiv.2306.06031",
        "arxiv": "2306.06031",
        "relevance": "Outlines open-source workflows for automated financial acquisition from SEC EDGAR and news disclosures. Inspired our multi-source collection orchestrator.",
        "component_role": "Data Pipeline Architecture Inspiration"
    },

    # G. ESG Disclosures & Rating Divergence
    {
        "id": "berg2022aggregate",
        "category": "G. ESG Analysis & Transparency",
        "title": "Aggregate Confusion: The Divergence of ESG Ratings",
        "doi": "10.1093/rof/rfac033",
        "arxiv": "",
        "relevance": "Foundational MIT Sloan study proving commercial ESG ratings diverge widely (r=0.54) due to black-box weighting. Directly inspired our transparent, indicator-level scoring engine.",
        "component_role": "Theoretical Foundation & Problem Formulation"
    },
    {
        "id": "webersinke2021climatebert",
        "category": "G. ESG Analysis & Transparency",
        "title": "ClimateBERT: A Pretrained Language Model for Climate-Related Text",
        "doi": "10.48550/arXiv.2110.12010",
        "arxiv": "2110.12010",
        "relevance": "Distinguishes between quantitative emissions indicators (Scope 1/2) and qualitative corporate claims under TCFD/BRSR frameworks.",
        "component_role": "ESG Extraction Methodology"
    }
]

def verify_paper(paper):
    print(f"\n--- Verifying: {paper['title']} ---")
    doi = paper["doi"]
    result = {
        "id": paper["id"],
        "category": paper["category"],
        "title": paper["title"],
        "doi": doi,
        "arxiv": paper["arxiv"],
        "authors": "",
        "year": "",
        "venue": "",
        "publisher": "",
        "publisher_url": "",
        "oa_url": f"https://arxiv.org/abs/{paper['arxiv']}" if paper["arxiv"] else "",
        "abstract": "",
        "verified": False,
        "relevance": paper["relevance"],
        "component_role": paper["component_role"]
    }

    # Crossref Lookup if DOI exists and is not raw arXiv doi
    if doi and "arXiv" not in doi:
        try:
            req = urllib.request.Request(
                f"https://api.crossref.org/works/{doi}",
                headers={"User-Agent": "AcademicResearchVerifier/1.0 (mailto:academic@research.org)"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                item = data["message"]
                authors_list = []
                for a in item.get("author", []):
                    authors_list.append(f"{a.get('given', '')} {a.get('family', '')}".strip())
                result["authors"] = ", ".join(authors_list) if authors_list else ""
                
                # Year
                issued = item.get("issued", {}).get("date-parts", [[None]])[0][0]
                result["year"] = str(issued) if issued else ""
                
                # Container / Venue
                container = item.get("container-title", [])
                result["venue"] = container[0] if container else ""
                
                # Publisher
                result["publisher"] = item.get("publisher", "")
                result["publisher_url"] = item.get("URL", f"https://doi.org/{doi}")
                result["verified"] = True
                print(f"  [Crossref OK] {result['title']} ({result['year']}) - {result['venue']}")
        except Exception as e:
            print(f"  [Crossref Error] {e}")

    # Fallback to Semantic Scholar or arXiv if not fully verified
    if not result["verified"] or not result["authors"]:
        query_id = f"ARXIV:{paper['arxiv']}" if paper["arxiv"] else (f"DOI:{doi}" if doi else f"TITLE:{urllib.parse.quote(paper['title'])}")
        try:
            url = f"https://api.semanticscholar.org/graph/v1/paper/{query_id}?fields=title,authors,year,venue,publicationVenue,url,openAccessPdf,abstract"
            req = urllib.request.Request(url, headers={"User-Agent": "AcademicResearchVerifier/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                s2_data = json.loads(resp.read().decode())
                if not result["authors"]:
                    result["authors"] = ", ".join([a["name"] for a in s2_data.get("authors", [])])
                if not result["year"] and s2_data.get("year"):
                    result["year"] = str(s2_data["year"])
                if not result["venue"] and s2_data.get("venue"):
                    result["venue"] = s2_data["venue"]
                if not result["publisher_url"] and s2_data.get("url"):
                    result["publisher_url"] = s2_data["url"]
                if s2_data.get("openAccessPdf"):
                    result["oa_url"] = s2_data["openAccessPdf"].get("url", result["oa_url"])
                if s2_data.get("abstract"):
                    result["abstract"] = s2_data["abstract"]
                result["verified"] = True
                print(f"  [SemanticScholar OK] {result['title']} ({result['year']})")
        except Exception as e:
            print(f"  [SemanticScholar Error] {e}")

    return result

if __name__ == "__main__":
    verified_papers = []
    for p in CANDIDATE_PAPERS:
        vp = verify_paper(p)
        verified_papers.append(vp)
    
    out_path = Path("AI_Financial_Analyst_Academic_Submission/verified_papers.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(verified_papers, f, indent=2)
    print(f"\nSaved {len(verified_papers)} verified papers to {out_path}")
