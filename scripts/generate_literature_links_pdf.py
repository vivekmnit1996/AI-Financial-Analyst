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

def generate_literature_pdf():
    out_dir = Path("AI_Financial_Analyst_Academic_Submission")
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = out_dir / "AI_Financial_Analyst_Research_Literature_and_Links.pdf"

    # Load verified papers
    with open(out_dir / "verified_papers.json", "r", encoding="utf-8") as f:
        papers = json.load(f)

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
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=10
    )
    cat_header_style = ParagraphStyle(
        "CatHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=6
    )
    paper_title_style = ParagraphStyle(
        "PaperTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=2
    )
    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=2
    )
    link_style = ParagraphStyle(
        "LinkStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1D4ED8"),
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
    impl_style = ParagraphStyle(
        "ImplStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#047857"),
        spaceAfter=6
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#1E293B")
    )
    table_header = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("AI FINANCIAL ANALYST & REPORT GENERATOR", doc_title_style))
    story.append(Paragraph(
        "<b>RESEARCH LITERATURE & OFFICIAL PAPER LINKS CATALOGUE</b><br/>"
        "<b>Project:</b> B.Tech Major Project in Artificial Intelligence & Data Engineering<br/>"
        "<b>Student Team:</b> Vivek Upadhyay (Team Captain — Roll: 2023UAI1996) &bull; Ashish Rolaniya (Roll: 2023UAI1825)<br/>"
        "<b>Purpose:</b> Comprehensive academic verification of peer-reviewed foundations, official publisher links, DOIs, and open-access repositories underpinning the system's dual-pathway architecture.",
        doc_sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=0, spaceAfter=10))

    # Introduction / Purpose
    intro_p = Paragraph(
        "<b>Executive Summary of Academic Foundation:</b><br/>"
        "Modern financial decision-making requires reconciling structured accounting statements with rich unstructured corporate disclosures. "
        "Standard generative Large Language Models suffer from well-documented arithmetic hallucination and lack source-traceable grounding. "
        "This project resolves these challenges through a dual-engine architecture: a deterministic Python/Pandas calculation engine for numerical precision, "
        "and a Hybrid Retrieval-Augmented Generation (Dense BGE + Lexical BM25 + Reciprocal Rank Fusion + Cross-Encoder Reranking) pipeline for factual evidence extraction. "
        "This catalogue establishes the literature foundation across 7 research domains, verifying 19 peer-reviewed publications via Crossref and arXiv official APIs.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    # Group papers by category
    categories = {}
    for p in papers:
        cat = p["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    for cat_name, cat_papers in categories.items():
        story.append(Paragraph(cat_name, cat_header_style))
        for p in cat_papers:
            entry = []
            entry.append(Paragraph(f"<b>[{p['id']}] {p['title']}</b> ({p['year']})", paper_title_style))
            entry.append(Paragraph(f"<b>Authors:</b> {p['authors']}", meta_style))
            entry.append(Paragraph(f"<b>Venue / Container:</b> {p['venue']} | <b>Publisher:</b> {p['publisher']}", meta_style))

            # Clickable Links
            links_text = ""
            if p.get("doi"):
                doi_url = f"https://doi.org/{p['doi']}" if not p['doi'].startswith("http") else p['doi']
                links_text += f"<b>DOI:</b> <a href='{doi_url}' color='#1D4ED8'><u>{p['doi']}</u></a> &nbsp;&nbsp;|&nbsp;&nbsp; "
            if p.get("publisher_url"):
                links_text += f"<b>Publisher:</b> <a href='{p['publisher_url']}' color='#1D4ED8'><u>Link</u></a> &nbsp;&nbsp;|&nbsp;&nbsp; "
            if p.get("oa_url"):
                links_text += f"<b>Open Access PDF:</b> <a href='{p['oa_url']}' color='#059669'><u>Direct PDF</u></a>"
            
            entry.append(Paragraph(links_text, link_style))
            
            if p.get("abstract"):
                abs_snippet = p['abstract'][:350] + ("..." if len(p['abstract']) > 350 else "")
                entry.append(Paragraph(f"<b>Abstract Summary:</b> {abs_snippet}", body_style))
            
            entry.append(Paragraph(f"<b>Relevance & Role:</b> {p['relevance']} (<i>{p['component_role']}</i>)", impl_style))
            entry.append(Spacer(1, 4))
            story.append(KeepTogether(entry))

    # Page Break for Traceability Table
    story.append(PageBreak())
    story.append(Paragraph("RESEARCH PAPER TO PROJECT COMPONENT TRACEABILITY MATRIX", cat_header_style))
    story.append(Paragraph(
        "The following matrix summarizes the exact mapping between each research publication, the affected project component, and its functional deployment role.",
        doc_sub_style
    ))
    story.append(Spacer(1, 6))

    # Table of 19 papers
    table_data = [
        [
            Paragraph("Paper Title", table_header),
            Paragraph("Authors & Year", table_header),
            Paragraph("Project Component", table_header),
            Paragraph("Nature of Usage & System Role", table_header)
        ]
    ]

    for p in papers:
        short_title = p['title'][:45] + ("..." if len(p['title']) > 45 else "")
        short_authors = p['authors'].split(',')[0] + " et al. (" + p['year'] + ")"
        table_data.append([
            Paragraph(f"<b>{short_title}</b>", table_cell),
            Paragraph(short_authors, table_cell),
            Paragraph(p['category'].split('. ')[-1], table_cell),
            Paragraph(f"<b>{p['component_role']}:</b> {p['relevance'][:140]}...", table_cell)
        ])

    table = Table(table_data, colWidths=[140, 95, 105, 190])
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
    generate_literature_pdf()
