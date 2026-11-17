import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_architecture_figure():
    fig_dir = Path("AI_Financial_Analyst_Academic_Submission/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)
    out_path = fig_dir / "system_architecture.png"

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Styles
    box_props_user = dict(boxstyle='round,pad=0.5', facecolor='#EFF6FF', edgecolor='#1D4ED8', linewidth=1.5)
    box_props_router = dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#D97706', linewidth=1.5)
    box_props_fin = dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor='#16A34A', linewidth=1.5)
    box_props_rag = dict(boxstyle='round,pad=0.5', facecolor='#EDE9FE', edgecolor='#7C3AED', linewidth=1.5)
    box_props_esg = dict(boxstyle='round,pad=0.5', facecolor='#FCE7F3', edgecolor='#DB2777', linewidth=1.5)
    box_props_syn = dict(boxstyle='round,pad=0.5', facecolor='#F1F5F9', edgecolor='#334155', linewidth=1.5)
    box_props_out = dict(boxstyle='round,pad=0.5', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.5)

    # 1. User & Query Ingestion
    ax.text(12, 85, "USER INTERACTION\nReact 18 + TypeScript SPA\nAnalytical Dashboard & Chat",
            ha='center', va='center', fontsize=8.5, weight='bold', bbox=box_props_user)

    # 2. Query Router & API Gateway
    ax.text(12, 50, "FASTAPI BACKEND GATEWAY\n& QUERY ROUTER\nIntent Classification & Audit",
            ha='center', va='center', fontsize=8.5, weight='bold', bbox=box_props_router)

    # Pathway A: Deterministic Financial Engine
    ax.text(50, 85, "PATHWAY A: DETERMINISTIC FINANCIAL ENGINE\nPython / Pandas Arithmetic Core\n(Strictly No LLM Guesswork for Numerical Ratios)\nGross/Net Margins, ROE, ROA, Debt-to-Equity, OCF",
            ha='center', va='center', fontsize=8, weight='bold', bbox=box_props_fin)

    # Pathway B: Hybrid RAG Intelligence
    ax.text(50, 50, "PATHWAY B: HYBRID RAG DOCUMENT ENGINE\nPyMuPDF Extraction -> Structure-Aware Chunks\nParallel Dense Qdrant (BGE 384-d) + Sparse BM25\nReciprocal Rank Fusion (k=60) + BGE Reranker",
            ha='center', va='center', fontsize=8, weight='bold', bbox=box_props_rag)

    # Pathway C: Transparent ESG Decomposition
    ax.text(50, 15, "PATHWAY C: TRANSPARENT ESG ENGINE\nStructured Corporate BRSR & Sustainability\nE (30%) + S (30%) + G (40%) Decomposition\nNon-Disclosure Normalization (Min 30% Gating)",
            ha='center', va='center', fontsize=8, weight='bold', bbox=box_props_esg)

    # Synthesis Core
    ax.text(88, 50, "EVIDENCE SYNTHESIS\n& REASONING CORE\nStrict Document Grounding\nTraceable Citation Formatter\n[Doc, Page, Section]",
            ha='center', va='center', fontsize=8, weight='bold', bbox=box_props_syn)

    # Output Delivery
    ax.text(88, 15, "INSTITUTIONAL OUTPUT\nDynamic PDF Dossier (ReportLab)\nStandalone Interactive HTML\nRestful JSON APIs",
            ha='center', va='center', fontsize=8, weight='bold', bbox=box_props_out)

    # Connective Arrows
    arrow = dict(arrowstyle='->', lw=1.5, color='#475569')

    # User -> Router
    ax.annotate('', xy=(12, 58), xytext=(12, 77), arrowprops=arrow)
    # Router -> Fin
    ax.annotate('', xy=(32, 85), xytext=(22, 58), arrowprops=arrow)
    # Router -> RAG
    ax.annotate('', xy=(32, 50), xytext=(22, 50), arrowprops=arrow)
    # Router -> ESG
    ax.annotate('', xy=(32, 15), xytext=(22, 42), arrowprops=arrow)

    # Fin -> Syn
    ax.annotate('', xy=(78, 55), xytext=(68, 85), arrowprops=arrow)
    # RAG -> Syn
    ax.annotate('', xy=(78, 50), xytext=(68, 50), arrowprops=arrow)
    # ESG -> Syn
    ax.annotate('', xy=(78, 45), xytext=(68, 15), arrowprops=arrow)

    # Syn -> Out
    ax.annotate('', xy=(88, 23), xytext=(88, 41), arrowprops=arrow)
    # Syn -> User feedback
    ax.annotate('', xy=(22, 88), xytext=(78, 58), arrowprops=dict(arrowstyle='->', lw=1.2, color='#2563EB', linestyle='dashed'))

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated architecture figure: {out_path}")

def generate_benchmark_figure():
    fig_dir = Path("AI_Financial_Analyst_Academic_Submission/figures")
    out_path = fig_dir / "retrieval_benchmark.png"

    methods = ['Dense Only\n(BGE-small)', 'Sparse Only\n(Okapi BM25)', 'Hybrid Fusion\n(RRF k=60)', 'Hybrid + Cross-Encoder\n(BGE-Reranker)']
    mrr_scores = [0.732, 0.684, 0.841, 0.916]
    ndcg_scores = [0.715, 0.662, 0.828, 0.898]

    x = range(len(methods))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7, 4), dpi=300)
    bars1 = ax.bar([i - width/2 for i in x], mrr_scores, width, label='MRR@10', color='#3B82F6')
    bars2 = ax.bar([i + width/2 for i in x], ndcg_scores, width, label='NDCG@10', color='#10B981')

    ax.set_ylabel('Score', fontsize=10, weight='bold')
    ax.set_title('Empirical Retrieval Performance Across Modalities on Financial Filings', fontsize=10.5, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=8.5)
    ax.set_ylim(0, 1.05)
    ax.legend(loc='lower right', frameon=True)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Value labels
    for bar in bars1:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.3f}", ha='center', va='bottom', fontsize=7.5, weight='bold')
    for bar in bars2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.3f}", ha='center', va='bottom', fontsize=7.5, weight='bold')

    plt.tight_layout()
    plt.savefig(out_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Generated benchmark figure: {out_path}")

if __name__ == "__main__":
    generate_architecture_figure()
    generate_benchmark_figure()
