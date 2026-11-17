import os
from pathlib import Path
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.config import settings
from backend.app.rag.sample_document_generator import NumberedCanvas

class PDFReportGenerator:
    """
    Generates institutional-grade AI Financial & ESG Analytical PDF Reports.
    Distinguishes deterministically calculated metrics from qualitative citations and LLM insights.
    """

    @classmethod
    def generate_report(
        cls,
        company,
        fiscal_year: int,
        ratios_data: list,
        insights: list,
        esg_breakdown: dict,
        citations: list,
        ai_summary: str,
        output_filename: str
    ) -> str:
        out_path = settings.REPORTS_DIR / output_filename

        doc = SimpleDocTemplate(
            str(out_path),
            pagesize=letter,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "RepTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=6
        )
        sub_style = ParagraphStyle(
            "RepSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#475569"),
            spaceAfter=12
        )
        h2_style = ParagraphStyle(
            "RepH2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "RepBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155"),
            spaceAfter=6
        )
        box_style = ParagraphStyle(
            "RepBox",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=4
        )

        story = []

        now_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

        # Header Block
        story.append(Paragraph(f"AI FINANCIAL & ESG RESEARCH DOSSIER", title_style))
        story.append(Paragraph(
            f"<b>Company:</b> {company.name} ({company.ticker}) | <b>Fiscal Year:</b> FY{fiscal_year} | "
            f"<b>Generated:</b> {now_str}", sub_style
        ))
        story.append(Spacer(1, 8))

        # Executive Summary Box
        story.append(Paragraph("1. Executive Summary & Analytical Insights", h2_style))
        if insights:
            for ins in insights[:5]:
                story.append(Paragraph(f"• {ins}", body_style))
        if ai_summary:
            story.append(Spacer(1, 4))
            story.append(Paragraph(f"<b>Synthesized Analysis:</b><br/>{ai_summary}", body_style))

        story.append(Spacer(1, 8))

        # Financial Performance Table
        story.append(Paragraph("2. Deterministic Financial Metrics & Ratio Analysis", h2_style))
        story.append(Paragraph("<i>Note: All quantitative metrics computed deterministically via Python/Pandas numerical engine.</i>", body_style))

        if ratios_data:
            table_rows = [
                ["Fiscal Year", "Revenue", "YoY Growth", "Operating Margin", "Net Margin", "ROE", "Debt/Equity", "OCF"]
            ]
            u = company.units
            c = company.currency
            for r in ratios_data:
                rev_str = f"{c} {r.get('revenue'):,.1f} {u}" if r.get('revenue') is not None else "-"
                growth_str = f"{r.get('revenue_growth_pct'):+.1f}%" if r.get('revenue_growth_pct') is not None else "-"
                op_margin_str = f"{r.get('operating_profit_margin_pct'):.1f}%" if r.get('operating_profit_margin_pct') is not None else "-"
                net_margin_str = f"{r.get('net_profit_margin_pct'):.1f}%" if r.get('net_profit_margin_pct') is not None else "-"
                roe_str = f"{r.get('return_on_equity_pct'):.1f}%" if r.get('return_on_equity_pct') is not None else "-"
                dte_str = f"{r.get('debt_to_equity'):.2f}" if r.get('debt_to_equity') is not None else "-"
                ocf_str = f"{c} {r.get('operating_cash_flow'):,.1f}" if r.get('operating_cash_flow') is not None else "-"

                table_rows.append([
                    f"FY{r.get('fiscal_year')}",
                    rev_str,
                    growth_str,
                    op_margin_str,
                    net_margin_str,
                    roe_str,
                    dte_str,
                    ocf_str
                ])

            t = Table(table_rows, colWidths=[55, 85, 65, 75, 65, 55, 60, 72])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
                ('FONTSIZE', (0, 1), (-1, -1), 7.5),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t)

        story.append(Spacer(1, 10))

        # ESG Analysis Section
        story.append(Paragraph("3. Transparent ESG Performance Evaluation", h2_style))
        if esg_breakdown:
            cov = esg_breakdown.get("data_coverage_pct", 0)
            overall = esg_breakdown.get("overall_esg_score", "N/A")
            e_sc = esg_breakdown.get("environmental_score", "N/A")
            s_sc = esg_breakdown.get("social_score", "N/A")
            g_sc = esg_breakdown.get("governance_score", "N/A")

            esg_summary_text = (
                f"<b>Overall ESG Composite Score:</b> {overall} / 100 | "
                f"<b>Data Coverage:</b> {cov:.1f}%<br/>"
                f"• Environmental Pillar (30% weight): <b>{e_sc}</b> / 100<br/>"
                f"• Social Pillar (30% weight): <b>{s_sc}</b> / 100<br/>"
                f"• Governance Pillar (40% weight): <b>{g_sc}</b> / 100<br/>"
                f"<i>Formula: {esg_breakdown.get('formula_explanation', '')}</i>"
            )
            story.append(Paragraph(esg_summary_text, body_style))

            if esg_breakdown.get("methodology_limitations"):
                story.append(Spacer(1, 4))
                story.append(Paragraph("<b>Methodology & Transparency Disclaimers:</b>", box_style))
                for lim in esg_breakdown["methodology_limitations"][:3]:
                    story.append(Paragraph(f"- {lim}", box_style))
        else:
            story.append(Paragraph("No structured ESG disclosures recorded for this reporting period.", body_style))

        story.append(Spacer(1, 10))

        # Qualitative Evidence & Citations
        story.append(Paragraph("4. Retrieved Qualitative Document Evidence & Verified Citations", h2_style))
        if citations:
            for idx, cit in enumerate(citations[:5], 1):
                p_text = (
                    f"<b>[{idx}] {cit.get('document_title', 'Report')} (FY{cit.get('fiscal_year', 'N/A')}), "
                    f"Page {cit.get('page_number', 'N/A')} [{cit.get('section', 'General')}]:</b><br/>"
                    f"<i>\"{cit.get('snippet', '')}\"</i>"
                )
                story.append(Paragraph(p_text, body_style))
                story.append(Spacer(1, 3))
        else:
            story.append(Paragraph("No qualitative citations queried for this generation.", body_style))

        # Build PDF
        doc.build(story, canvasmaker=NumberedCanvas)
        return str(out_path)
